"""Park only active external-audio waits and resume the stopped render job when its voice completes."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess

DEFAULT_GATE = "Locate the verified recording of this script"
STOPPED = {"cancelled", "failure", "timed_out"}
ROOT = Path(__file__).parent


def request(path, post=False):
    cmd = ["gh", "api"]
    if post:
        cmd.extend(["-X", "POST"])
    output = subprocess.check_output([*cmd, "repos/" + os.environ["GH_REPO"] + "/actions/" + path])
    return json.loads(output) if output.strip() else None


def pinned(identity, branch):
    run_id, sha, stem = identity
    run = request(f"runs/{run_id}")
    expected = (sha, f".github/workflows/{stem}.yml", branch, os.environ["GH_REPO"], "push")
    actual = (run["head_sha"], run["path"], run["head_branch"], run["head_repository"]["full_name"], run["event"])
    if actual != expected:
        raise ValueError(f"Run {run_id} does not match its pinned production.")
    return run


def gate_action(voice, render, jobs, gate_name, previously_parked_queued):
    # Actions may list skipped device/release jobs after cancellation.
    render_jobs = [j for j in jobs if j["name"] == "render" or j["name"].startswith("render (")]
    if not jobs and previously_parked_queued and voice.get("conclusion") == "success" and render.get("conclusion") == "cancelled":
        return f'runs/{render["id"]}/rerun'
    if len(render_jobs) != 1:
        return None
    job = render_jobs[0]
    if any(j is not job and (j["status"] == "in_progress" or
               j.get("conclusion") not in {None, "cancelled", "skipped"}) for j in jobs):
        return None
    steps = job.get("steps", [])
    gate = next((s for s in steps if s["name"] == gate_name), None)
    if gate and any(s["number"] > gate["number"] and s["status"] != "queued"
                    and s.get("conclusion") not in {"skipped", "cancelled"}
                    and not s["name"].startswith(("Post ", "Complete job"))
                    for s in steps):
        return None

    if voice.get("conclusion") != "success":
        if render["status"] == "in_progress" and gate and gate["status"] == "in_progress":
            started = datetime.fromisoformat(gate["started_at"].replace("Z", "+00:00"))
            if (datetime.now(timezone.utc) - started).total_seconds() >= 90:
                return f'runs/{render["id"]}/cancel'
        return None

    if render["status"] != "completed" or render.get("conclusion") not in STOPPED:
        return None
    if gate and gate.get("conclusion") in STOPPED:
        return f'jobs/{job["id"]}/rerun'
    if previously_parked_queued and not steps and job.get("conclusion") == "cancelled":
        return f'jobs/{job["id"]}/rerun'
    return None


def reconcile(groups, target_voice=None):
    for group in groups:
        if target_voice and group["voice"][0] != target_voice:
            continue
        branch = group["branch"]
        voice = pinned(group["voice"], branch)
        for run_id, workflow in group["renders"]:
            render = pinned((run_id, group["render_commit"], workflow), branch)
            if render["status"] not in {"in_progress","completed"} or render.get("conclusion") == "success":
                continue
            jobs = request(f"runs/{run_id}/jobs?filter=latest&per_page=100")["jobs"]
            action = gate_action(voice, render, jobs, group.get("waitStep", DEFAULT_GATE),
                                 group.get("previouslyParkedQueued", False))
            if not action:
                continue
            if action.endswith("/cancel") and pinned(group["voice"], branch).get("conclusion") == "success":
                continue
            print(f"{workflow}: {action}", flush=True)
            request(action, post=True)


if __name__ == "__main__":
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    voice_id = event["workflow_run"]["id"] if "workflow_run" in event else None
    reconcile(json.loads((ROOT/"split-recording-runs.json").read_text()), voice_id)
