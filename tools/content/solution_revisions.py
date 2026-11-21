"""Load a private wording correction and verify it against its reviewed digest."""
import hashlib
import json
from pathlib import Path


def private_overlay(directory):
    path = Path(directory) / 'practice-revision-solutions.json'
    return json.loads(path.read_text()) if path.exists() else {}


def checked_solution(problem_id, authored, hashes, overlay):
    if problem_id not in hashes:
        return authored
    solution = overlay.get(problem_id, authored)
    if hashlib.sha256(solution.encode()).hexdigest() != hashes[problem_id]:
        raise ValueError(f'{problem_id}: refresh the private solution overlay before rebuilding')
    return solution
