(() => {
  const video = document.querySelector('video');
  if (!video) return;
  let requestNumber = 0;
  let timer = 0;
  let resumeAfterSeek;

  function cancelPending() {
    ++requestNumber;
    clearTimeout(timer);
    if (resumeAfterSeek) video.removeEventListener('seeked', resumeAfterSeek);
    resumeAfterSeek = undefined;
  }
  function start() {
    video.play().catch(() => {});
  }
  function jump(target) {
    cancelPending();
    const request = requestNumber;
    video.scrollIntoView({block: 'center'});
    let attempts = 0;

    function checkPosition() {
      if (request !== requestNumber || video.paused || attempts >= 2) return;
      if (video.seeking) {
        timer = setTimeout(checkPosition, 240);
        return;
      }
      if (Math.abs(video.currentTime - target) <= 2) return;
      ++attempts;
      // Some WebKit decoders report the requested time at seeked, then resume at the old frame.
      // Seek while the decoder is paused and give the displayed frame time to settle.
      video.pause();
      resumeAfterSeek = () => {
        video.removeEventListener('seeked', resumeAfterSeek);
        resumeAfterSeek = undefined;
        if (request !== requestNumber) return;
        timer = setTimeout(() => {
          if (request !== requestNumber) return;
          start();
          timer = setTimeout(checkPosition, 480);
        }, 95);
      };
      video.addEventListener('seeked', resumeAfterSeek);
      video.currentTime = target;
      timer = setTimeout(() => {
        if (request === requestNumber && resumeAfterSeek && !video.seeking) resumeAfterSeek();
      }, 400);
    }

    video.currentTime = target;
    start();
    timer = setTimeout(checkPosition, 480);
  }
  video.addEventListener('pointerdown', cancelPending);
  video.addEventListener('keydown', cancelPending);
  document.querySelectorAll('button[data-time]').forEach(button => {
    button.addEventListener('click', () => {
      const time = Number(button.dataset.time);
      if (Number.isFinite(time) && time >= 0) jump(time);
    });
  });
})();
