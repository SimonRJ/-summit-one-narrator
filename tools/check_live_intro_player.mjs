import assert from "node:assert/strict";
import {chromium} from "playwright";

const lesson = process.argv[2];
assert(/^S[0-9]{3}$/.test(lesson));
const slot = Number(lesson.slice(1));
const root = "https://simonrj.github.io/-summit-one-narrator/";
const browser = await chromium.launch({
  channel: "chrome",
  args: ["--autoplay-policy=no-user-gesture-required", "--no-sandbox"],
});
try {
  const page = await browser.newPage({viewport: {width: 390, height: 844}, isMobile: true, hasTouch: true});
  await page.goto(root + "watch-lesson-intro.html?slot=" + slot, {waitUntil: "domcontentloaded", timeout: 30000});
  const correct = page.locator("#introChapters button").filter({hasText: "Exam-style challenge"});
  await correct.waitFor({state: "visible", timeout: 38000});
  assert.equal(await page.locator("#introChapters button").count(), 7);
  assert.equal(await page.locator("video[playsinline]").count(), 1);
  const jump = Number(await correct.getAttribute("data-time"));
  assert(jump > 0);
  await page.locator("video").evaluate(video => { video.muted = true; });
  await correct.click();
  await page.waitForFunction(time => {
    const player = document.querySelector("video");
    return !player.error && !player.paused && player.videoWidth === 1920 && player.currentTime > time + .15;
  }, jump, {timeout: 35000});
  assert.equal(await page.locator("video source").getAttribute("src"),
    "https://github.com/SimonRJ/-summit-one-narrator/releases/download/lesson-introductions/" + lesson + "-Intro.mp4");
  console.log(lesson + " plays and seeks at phone width on the live Summit One watch page.");
} finally {
  await browser.close();
}
