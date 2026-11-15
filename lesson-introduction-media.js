const localSlots = new Set([1, 2, 3, 4, 5, 6]);
const online = new Map();
const repository = "SimonRJ/-summit-one-narrator";
const catalogueRoot = "https://raw.githubusercontent.com/" + repository
  + "/refs/heads/lesson-intro-catalog/data/";
const releaseRoot = "https://github.com/" + repository + "/releases/download/lesson-introductions/";
export const INTRO_MEDIA_VERSION = "lesson-intros-v2";

let loading;

export function lessonIntroId(slot) {
  const number = Number(slot);
  return localSlots.has(number) || online.get(number)?.status === "verified"
    ? "S" + String(number).padStart(3, "0") : null;
}

export function introMediaSource(id) {
  if (!/^S[0-9]{3}$/.test(id)) throw new TypeError("Invalid lesson ID");
  const base = localSlots.has(Number(id.slice(1))) ? "media/" : releaseRoot;
  const suffix = base === "media/" ? "?v=" + INTRO_MEDIA_VERSION : "";
  return {
    movie: base + id + "-Intro.mp4" + suffix,
    poster: base + id + "-Intro-poster.jpg" + suffix,
  };
}

async function readJson(path) {
  const response = await fetch(catalogueRoot + path + "?v=" + Math.floor(Date.now() / 20000), {
    cache: "no-store", credentials: "omit", signal: AbortSignal.timeout(5500),
  });
  if (!response.ok) throw new Error("Lesson introduction catalogue unavailable");
  return response.json();
}

function normaliseEntry(entry) {
  if (typeof entry?.id !== "string" || !/^S[0-9]{3}$/.test(entry.id)) return null;
  const slot = Number(entry.id.slice(1));
  if (slot <= 6 || slot > 372) return null;
  if (!["checking","verified"].includes(entry.status) || typeof entry.title !== "string") return null;
  if (!Number.isFinite(entry.seconds) || entry.seconds < 1 || entry.seconds > 600) return null;
  return {...entry, slot};
}

export function loadIntroductionCatalogue() {
  loading ??= readJson("lesson-intros-live.json").then(catalogue => {
    if (catalogue.version !== 1 || !Array.isArray(catalogue.entries)) return [];
    for (const raw of catalogue.entries) {
      const entry = normaliseEntry(raw);
      if (entry) online.set(entry.slot, entry);
    }
    return [...online.values()].sort((a,b) => a.slot - b.slot);
  }).catch(() => {
    loading = undefined;
    return [...online.values()].sort((a,b) => a.slot - b.slot);
  });
  return loading;
}

export async function loadIntroductionDetails(id) {
  if (!/^S[0-9]{3}$/.test(id)) throw new TypeError("Invalid lesson ID");
  return readJson("lesson-intros/" + id + ".json");
}
