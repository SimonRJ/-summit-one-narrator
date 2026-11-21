// Only completed, published reviews count. The release registers can change independently.
function completedFilms(csv, type) {
  const title = '(?:"(?:[^"]|"")*"|[^,\\r\\n]*)';
  const id = type === 'lesson' ? 'S\\d{3}' : 'T\\d{2}\\.[123E]';
  const pattern = new RegExp('^(' + id + '),' + title + ',' + title + ',final editorial review complete,', 'gm');
  return new Set(Array.from(csv.matchAll(pattern), match => match[1]));
}

async function get(path, json = false) {
  const response = await fetch(new URL(path, import.meta.url), {cache: 'no-store'});
  if (!response.ok) throw Error('Progress data unavailable');
  return json ? response.json() : response.text();
}

export async function readProgress() {
  const [scope, lessons, teaching] = await Promise.all([
    get('course-review-scope.json', true),
    get('../docs/lesson-introduction-review-register-20261116.csv'),
    get('../docs/teaching-video-review-register-20261116.csv'),
  ]);
  const intros = completedFilms(lessons, 'lesson');
  for (const id of scope.additionalVerifiedIntroductions) intros.add(id);
  const counts = { introductions: intros.size, companions: completedFilms(teaching, 'teaching').size };
  let completed = 0, total = 0;
  for (const area of scope.areas) {
    const count = counts[area.key] ?? area.verified;
    if (!Number.isSafeInteger(count) || !Number.isSafeInteger(area.total) || count < 0 || count > area.total || area.total < 1)
      throw Error('Invalid review count');
    completed += count;
    total += area.total;
  }
  if (!total) throw Error('Missing review scope');
  return {completed, total, percent: Math.floor(100 * completed / total)};
}
