const localSlots = new Set([1, 2, 3, 4, 5, 6]);
const online = new Map();
const repository = "SimonRJ/-summit-one-narrator";
const catalogueRoot = "https://raw.githubusercontent.com/" + repository
  + "/refs/heads/lesson-intro-catalog/data/";
const releaseRoot = "https://github.com/" + repository + "/releases/download/lesson-introductions/";
export const INTRO_MEDIA_VERSION = "lesson-intros-v2";
const updatedMedia = { S001: "intro-20261116-illustrated", S002: "intro-20261116-illustrated" };

let loading;
let loadedAt = -Infinity;

export function lessonIntroId(slot) {
  const number = Number(slot);
  return localSlots.has(number) || online.get(number)?.status === "verified"
    ? "S" + String(number).padStart(3, "0") : null;
}

export function introMediaSource(id) {
  if (!/^S[0-9]{3}$/.test(id)) throw new TypeError("Invalid lesson ID");
  const slot = Number(id.slice(1));
  const base = localSlots.has(slot) ? "media/" : releaseRoot;
  const edition = !localSlots.has(slot) && online.get(slot)?.illustration === 1 ? "-Illustrated" : "";
  const suffix = base === "media/" ? "?v=" + (updatedMedia[id] ?? INTRO_MEDIA_VERSION) : "";
  const path = base + id + "-Intro" + edition;
  return {
    movie: path + ".mp4" + suffix,
    poster: path + "-poster.jpg" + suffix,
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
  const latest = () => [...online.values()].sort((a,b) => a.slot - b.slot);
  if (Date.now() - loadedAt < 30_000) return Promise.resolve(latest());
  loading ??= readJson("lesson-intros-live.json")
    .then(catalogue => {
      if (catalogue.version !== 1 || !Array.isArray(catalogue.entries)) return;
      online.clear();
      for (const raw of catalogue.entries) {
        const entry = normaliseEntry(raw);
        if (entry) online.set(entry.slot, entry);
      }
      loadedAt = Date.now();
    })
    .catch(() => {})
    .then(latest)
    .finally(() => { loading = undefined; });
  return loading;
}

export async function loadIntroductionDetails(id) {
  if (!/^S[0-9]{3}$/.test(id)) throw new TypeError("Invalid lesson ID");
  return readJson("lesson-intros/" + id + ".json");
}
