let cancelChapterJump;

document.addEventListener('click', event => {
  const button = event.target.closest('[data-time]');
  const player = button && document.getElementById('introFilm');
  const target = Number(button?.dataset.time);
  if (!player || !Number.isFinite(target) || target < 0) return;

  cancelChapterJump?.();
  const listeners = new AbortController();
  const options = {signal: listeners.signal};
  const deadline = Date.now() + 10000;
  let retryAfter = 0;
  let attempts = 0;
  let landedAt;
  let landedPosition;
  let pausedForRetry = false;
  let interval;

  function cancel() {
    listeners.abort();
    clearInterval(interval);
    if (cancelChapterJump === cancel) cancelChapterJump = undefined;
  }

  function finish() {
    cancel();
    if (pausedForRetry && player.paused) player.play().catch(() => {});
  }

  function inspect() {
    if (listeners.signal.aborted) return;
    const now = Date.now();
    if (now >= deadline) { finish(); return; }
    if (player.readyState < 1 || player.seeking) return;
    const wanted = Number.isFinite(player.duration) ? Math.min(target, player.duration) : target;
    const position = player.currentTime;
    const sinceLanding = landedAt === undefined ? 0 : (now - landedAt) / 1000;
    const distance = position - wanted;
    if (player.readyState >= 2 && distance >= -0.25 && distance <= 0.65 + sinceLanding * (player.playbackRate || 1)) {
      if (pausedForRetry && player.paused) {
        pausedForRetry = false;
        landedAt = undefined;
        player.play().catch(() => {});
        return;
      }
      if (landedAt === undefined) { landedAt = now; landedPosition = position; }
      // A successful-looking seeked event can precede WebKit silently jumping back.
      // Keep checking the playhead after resumption until it actually advances.
      const atEnd = Number.isFinite(player.duration) && player.duration - position < 0.15;
      if (sinceLanding >= 0.4 && (player.paused || atEnd || position > landedPosition + 0.08)) finish();
      return;
    }
    landedAt = undefined;
    if (now < retryAfter) return;
    if (attempts >= 3) { finish(); return; }
    // WebKit can acknowledge an inline seek while returning to its former time.
    // On a missed seek let the decoder settle while paused, then check the landing.
    if (attempts && !pausedForRetry && !player.paused) {
      pausedForRetry = true;
      retryAfter = now + 150;
      player.pause();
      return;
    }
    attempts++;
    retryAfter = now + 650;
    player.currentTime = wanted;
  }

  cancelChapterJump = cancel;
  for (const type of ['pointerdown','keydown','emptied','error']) player.addEventListener(type, cancel, options);
  player.addEventListener('pause', () => { if (player.paused && !pausedForRetry) cancel(); }, options);
  for (const type of ['loadedmetadata','seeked']) player.addEventListener(type, inspect, options);
  interval = setInterval(inspect, 100);
  player.scrollIntoView({block:'center'});
  // Unlock playback within the chapter tap. Replaying an already-playing element
  // immediately after assigning currentTime can undo the seek on mobile WebKit.
  if (player.paused) player.play().catch(() => {});
  inspect();
});
