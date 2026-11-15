import {introMediaSource,loadIntroductionCatalogue,loadIntroductionDetails} from "./lesson-introduction-media.js?v=lesson-intros-v4";

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
  for (const entry of remote) {
    const li = element("li");
    const link = element("a");
    link.href = watchHref(entry.slot);
    link.append(element("span", String(entry.slot).padStart(2,"0"), "number"),
      element("strong", entry.title), element("small", formatTime(entry.seconds)));
    li.append(link);
    gallery.append(li);
  }
  if (status) status.textContent = gallery.children.length + " of 283 lesson introductions available";
}

async function showVideo(route) {
  const number = new URLSearchParams(window.location.search).get("slot") || "";
  const status = document.getElementById("introStatus");
  const catalogue = await loadIntroductionCatalogue();
  const entry = /^[0-9]{1,3}$/.test(number) && catalogue.find(item => item.slot === Number(number));
  if (!entry) {
    status.textContent = "This lesson introduction is awaiting publication.";
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
  const source = element("source");
  source.src = media.movie;
  source.type = "video/mp4";
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
    // The captioned video remains playable if chapter metadata is temporarily unavailable.
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
if (gallery) addToGallery(gallery);
const route = document.getElementById("introWatch");
if (route) showVideo(route);
