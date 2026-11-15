document.addEventListener("click", event => {
  const button = event.target.closest("[data-time]");
  const player = button && document.getElementById("introFilm");
  if (!player) return;
  const time = Number(button.dataset.time);
  if (!(time >= 0 && Number.isFinite(time))) return;
  const seek = () => { player.currentTime = time; };
  if (player.readyState >= 1) seek();
  else player.addEventListener("loadedmetadata", seek, {once: true});
  player.scrollIntoView({block: "center"});
  player.play().catch(() => {});
});
