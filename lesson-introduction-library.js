import {introductionCatalogueComplete,introMediaSource,loadIntroductionCatalogue,loadIntroductionDetails} from "./lesson-introduction-media.js?v=bridge-deck-20261122";

const formatTime = value => Math.floor(value / 60) + ":" + String(Math.floor(value % 60)).padStart(2,"0");
const watchHref = slot => "watch-lesson-intro.html?slot=" + slot;

function element(tag, text, classes) {
  const node = document.createElement(tag);
  if (text) node.textContent = text;
  if (classes) node.className = classes;
  return node;
}

async function addToGallery(gallery) {
  const remote = (await loadIntroductionCatalogue()).filter(entry => entry.status === "verified");
  const status = document.getElementById("introProgress");
  const present = new Map([...gallery.querySelectorAll("li[data-intro-slot]")]
    .map(row => [Number(row.dataset.introSlot), row]));
  const slots = new Set(remote.map(entry => entry.slot));
  for (const [slot, row] of present) {
    if (!slots.has(slot)) row.remove();
  }
  for (const entry of remote) {
    const existing = present.get(entry.slot);
    if (existing) {
      const title = existing.querySelector("strong");
      const time = existing.querySelector("small");
      if (title.textContent !== entry.title) title.textContent = entry.title;
      if (time.textContent !== formatTime(entry.seconds)) time.textContent = formatTime(entry.seconds);
      continue;
    }
    const li = element("li");
    li.dataset.introSlot = String(entry.slot);
    const link = element("a");
    link.href = watchHref(entry.slot);
    link.append(element("span", String(entry.slot).padStart(2,"0"), "number"),
      element("strong", entry.title), element("small", formatTime(entry.seconds)));
    li.append(link);
    const following = [...gallery.querySelectorAll("li[data-intro-slot]")]
      .find(row => Number(row.dataset.introSlot) > entry.slot);
    gallery.insertBefore(li, following ?? null);
  }
  const count = introductionCatalogueComplete()
    ? gallery.children.length + " of 283 lesson introductions available"
    : "Showing " + gallery.children.length + " lesson introductions. The full catalogue could not be loaded.";
  if (status && status.textContent !== count) status.textContent = count;
}

async function showVideo(route) {
  const number = new URLSearchParams(window.location.search).get("slot") || "";
  const status = document.getElementById("introStatus");
  const slot = Number(number);
  if (!/^[0-9]{1,3}$/.test(number) || slot < 1 || slot > 372) {
    status.textContent = "Choose a lesson from the video library.";
    return;
  }
  if (slot <= 6) {
    window.location.replace("watch-intro-s" + String(slot).padStart(3, "0") + ".html" + window.location.hash);
    return;
  }
  const retry = document.getElementById("introRetry");
  retry.addEventListener("click", () => window.location.reload());
  const catalogue = await loadIntroductionCatalogue();
  const entry = catalogue.find(item => item.slot === slot && item.status === "verified");
  if (!entry) {
    const complete = introductionCatalogueComplete();
    status.textContent = complete
      ? "No lesson introduction is published for session " + slot + "."
      : "The full catalogue could not be loaded. Reconnect and try again.";
    retry.hidden = complete;
    return;
  }
  const title = document.getElementById("introTitle");
  title.textContent = entry.title;
  document.title = entry.title + " · Summit One";
  document.getElementById("introLessonNumber").textContent = "Lesson " + entry.slot + " · " + formatTime(entry.seconds);
  const player = document.getElementById("introFilm");
  const media = introMediaSource(entry.id);
  player.setAttribute("aria-label", entry.title + " with English captions");
  player.poster = media.poster;
  const chapterNote = {
    "S019-Intro-Illustrated.mp4": "At 0:45 the two squares removed are the two leftmost squares of the top row. The domino shown fits the two squares that remain in that row.",
    "S020-Intro-Illustrated.mp4": "At 2:18, twelve full cycles account for powers 1 to 48. The next exponent is 49. It occupies position 1 in the next cycle."
  }[new URL(media.movie, document.baseURI).pathname.split("/").pop()];
  if (chapterNote) player.after(element("p", chapterNote));

  const source = element("source");
  source.src = media.movie;
  source.type = "video/mp4";
  function playbackUnavailable() {
    status.textContent = "The video could not load. Check your connection and try again.";
    status.hidden = false;
    retry.hidden = false;
  }
  player.addEventListener("error", playbackUnavailable, {once: true});
  source.addEventListener("error", playbackUnavailable, {once: true});
  player.append(source);
  player.load();
  route.hidden = false;
  status.hidden = true;

  try {
    const details = await loadIntroductionDetails(entry.id);
    if (details.id !== entry.id || !Array.isArray(details.chapters) || !Array.isArray(details.transcript)) {
      throw new Error("Invalid chapter data");
    }
    const chapters = document.getElementById("introChapters");
    for (const chapter of details.chapters) {
      if (typeof chapter.title !== "string" || !Number.isFinite(chapter.start) || chapter.start < 0) continue;
      const row = element("li");
      const jump = element("button", chapter.title + " ");
      jump.type = "button";
      jump.dataset.time = String(chapter.start);
      jump.append(element("span", formatTime(chapter.start)));
      row.append(jump);
      chapters.append(row);
    }
    document.getElementById("introTranscript").append(...details.transcript.map(line => element("p", line)));
    document.getElementById("introContents").hidden = false;
  } catch {
    const guideStatus = document.getElementById("introGuideStatus");
    guideStatus.textContent = "Chapters and transcript could not load.";
    guideStatus.hidden = false;
    retry.hidden = false;
  }

  const next = catalogue.find(item => item.slot > entry.slot && item.status === "verified");
  if (next) {
    const link = element("a", "Next lesson →");
    link.rel = "next";
    link.href = watchHref(next.slot);
    document.getElementById("introNavigation").append(link);
  }
}
const gallery = document.getElementById("introGallery");
if (gallery) {
  addToGallery(gallery);
  const refresh = () => { if (!document.hidden) addToGallery(gallery); };
  document.addEventListener("visibilitychange", refresh);
  window.addEventListener("online", refresh);
  setInterval(refresh, 45_000);
}
const route = document.getElementById("introWatch");
if (route) showVideo(route);
