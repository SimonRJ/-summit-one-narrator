import {enableFigureViewing} from './figure-viewer.js?v=deeper-20261121';
import {readCard, readingAvailable} from './reviewed-lesson.js?v=deeper-20261121';
import {mountLessonModel} from './lesson-models.js?v=deeper-20261121';

const status = document.querySelector('#readerStatus');
const picker = document.querySelector('#readerLesson');
const reading = document.querySelector('#reading');
const editions = [
  './data/read-watch-practise.json?v=matched-investigations-20261121',
  './data/read-watch-practise-later.json?v=matched-investigations-20261121',
];

async function prepareOffline() {
  if (!('serviceWorker' in navigator)) {
    status.textContent = 'This browser can display the readings while online.';
    return;
  }
  let ready = false;
  const unavailable = 'Offline reading is not ready on this device. Reconnect and reload to try again.';
  // An older worker may remain active without knowing this reader's status request.
  const timeout = window.setTimeout(() => { if (!ready) status.textContent = unavailable; }, 15000);
  try {
    const service = navigator.serviceWorker;
    const ask = worker => worker?.postMessage({type: 'summit-reader-status'});
    service.addEventListener('message', event => {
      if (event.data?.type !== 'summit-reader-status-result') return;
      ready = event.data.ready === true;
      clearTimeout(timeout);
      status.textContent = ready ? 'Ready to read offline on this device.' : unavailable;
    });
    service.addEventListener('controllerchange', () => ask(service.controller));
    ask(service.controller);
    const registration = await service.register('./sw.js');
    ask(registration.active);
    const installing = registration.installing || registration.waiting;
    if (installing) installing.addEventListener('statechange', () => {
      if (installing.state === 'activated') ask(installing);
      if (installing.state === 'redundant' && !ready) {
        clearTimeout(timeout);
        status.textContent = unavailable;
      }
    });
    service.ready.then(registration => ask(registration.active));
  } catch {
    clearTimeout(timeout);
    if (!ready) status.textContent = unavailable;
  }
}

async function openReader() {
  const volumes = await Promise.all(editions.map(async path => {
    const response = await fetch(path);
    if (!response.ok) throw Error('Lesson text unavailable');
    return response.json();
  }));
  const available = volumes.flatMap(volume => volume.lessons).filter(lesson => readingAvailable(lesson.slot));
  for (const lesson of available) picker.add(new Option(`S${String(lesson.slot).padStart(3,'0')} · ${lesson.headline}`, lesson.slot));
  const requested = new URL(location.href).searchParams.get('slot');
  let recent;
  try { recent = localStorage.getItem('summit-one-reading:last'); } catch {}
  const initial = [requested, recent].map(Number).find(slot => available.some(lesson => lesson.slot === slot));
  picker.value = String(initial || 1);
  const display = () => {
    const lesson = available.find(item => item.slot === Number(picker.value));
    reading.innerHTML = readCard(lesson);
    enableFigureViewing(reading);
    mountLessonModel(reading.querySelector('[data-lesson-model]'), lesson);
    const recap = document.createElement('p');
    recap.textContent = lesson.recap;
    reading.firstElementChild.append(recap);
  };
  picker.addEventListener('change', display);
  document.querySelector('#readerPicker').hidden = false;
  display();
  prepareOffline();
}

openReader().catch(() => {
  status.textContent = 'The readings could not load. Reconnect and open this page once, then try again.';
});
