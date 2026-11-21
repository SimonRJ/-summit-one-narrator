// Enlarge only the figure already visible on this question. Native scrolling also works with touch.
const figures = '.rwl-opening-figure, .original-figure svg, .problem-figure svg, .exam-visual svg, .exam-visual img';
const wired = new WeakSet();
let nextCaption = 0;

export function enableFigureViewing(root) {
  for (const figure of root.querySelectorAll(figures)) {
    if (wired.has(figure) || figure.closest('button, a, .figure-viewer') || figure.parentElement.closest('svg')) continue;
    wired.add(figure);
    const scan = figure.matches('.exam-visual img');
    const trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.className = 'fv-open';
    trigger.textContent = scan ? 'Enlarge original question' : 'Enlarge diagram';
    trigger.setAttribute('aria-haspopup', 'dialog');
    figure.after(trigger);
    trigger.addEventListener('click', () => openViewer(figure, trigger, scan));
  }
}

function openViewer(figure, trigger, scan) {
  // Move the original so SVG definitions, accessible names, and all fragment references stay unique.
  const placeholder = document.createComment('original figure position');
  const original = figure.getBoundingClientRect();
  figure.before(placeholder);
  const dialog = document.createElement('dialog');
  dialog.className = 'figure-viewer';
  dialog.setAttribute('aria-label', scan ? 'Enlarged original question' : 'Enlarged diagram');
  dialog.innerHTML = `<div class="fv-toolbar">
    <div role="group" aria-label="Figure size">
      <button type="button" data-scale="1">Fit</button>
      <button type="button" data-scale="2">2×</button>
      <button type="button" data-scale="3">3×</button>
    </div>
    <button type="button" class="fv-close">Close</button>
  </div>
  <div class="fv-window" tabindex="0" role="region" aria-label="Figure. Scroll to explore when enlarged.">
    <div class="fv-media"></div>
  </div>`;
  const caption = figure.closest('figure')?.querySelector(':scope > figcaption')?.textContent.trim();
  if (caption) {
    const description = document.createElement('p');
    description.className = 'fv-caption';
    description.id = 'fv-caption-' + (++nextCaption);
    description.textContent = caption;
    dialog.append(description);
    dialog.setAttribute('aria-describedby', description.id);
  }
  // Keep the dialog in the owning question. A timed paper can replace that question while it is open.
  trigger.after(dialog);
  const viewport = dialog.querySelector('.fv-window');
  const media = dialog.querySelector('.fv-media');
  const close = dialog.querySelector('.fv-close');
  const buttons = dialog.querySelectorAll('[data-scale]');
  media.append(figure);
  dialog.showModal();
  let scale = scan ? 2 : 1;
  function resize() {
    if (!dialog.isConnected) { observer.disconnect(); return; }
    const box = figure.viewBox?.baseVal;
    const ratio = (figure.naturalWidth / figure.naturalHeight) || (box?.width / box?.height) || original.width / original.height || 1;
    const fit = Math.min(viewport.clientWidth, viewport.clientHeight * ratio);
    media.style.setProperty('--fv-width', Math.max(1, fit * scale) + 'px');
    for (const button of buttons) button.setAttribute('aria-pressed', String(Number(button.dataset.scale) === scale));
  }
  const observer = new ResizeObserver(resize);
  observer.observe(viewport);
  figure.addEventListener('load', resize);
  resize();
  for (const button of buttons) {
    button.addEventListener('click', () => {
      const x = (viewport.scrollLeft + viewport.clientWidth / 2) / viewport.scrollWidth;
      const y = (viewport.scrollTop + viewport.clientHeight / 2) / viewport.scrollHeight;
      scale = Number(button.dataset.scale);
      resize();
      viewport.scrollLeft = x * viewport.scrollWidth - viewport.clientWidth / 2;
      viewport.scrollTop = y * viewport.scrollHeight - viewport.clientHeight / 2;
    });
  }
  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => {
    observer.disconnect();
    figure.removeEventListener('load', resize);
    placeholder.replaceWith(figure);
    dialog.remove();
    if (trigger.isConnected) trigger.focus({preventScroll: true});
  }, {once: true});
  close.focus();
}
