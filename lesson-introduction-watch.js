const player = document.getElementById("introFilm");
if (player) {
  for (const button of document.querySelectorAll("[data-time]")) {
    button.addEventListener("click", () => {
      const time = Number(button.dataset.time);
      const seek = () => { player.currentTime = time; };
      if (player.readyState >= 1) seek();
      else player.addEventListener("loadedmetadata", seek, {once: true});
      player.scrollIntoView({block: "center"});
      player.play().catch(() => {});
    });
  }
}
