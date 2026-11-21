const host = document.querySelector('#coverage');
const bands = ['Q1–10', 'Q11–20', 'Q21–25', 'Q26–30'];
const escape = value => String(value ?? '').replace(/[&<>"']/g, ch => ({
  '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'
})[ch]);

function strategyCard(skill) {
  return `<article><h3>${escape(skill.strategy)}</h3><p>${escape(skill.topic)} · ${escape(skill.id)}</p>
    <p><b>Watch for</b> · ${escape(skill.avoid)}</p><p><b>Check</b> · ${escape(skill.check)}</p></article>`;
}

async function loadCoverage() {
  host.setAttribute('role','status');
  host.textContent = 'Loading the coverage map…';
  try {
    const response = await fetch('data/amc-coverage.json?v=recognition-20261113');
    if (!response.ok) throw Error('Archive map unavailable');
    const archive = await response.json();
    const topics = [...new Set(archive.skills.map(skill => skill.topic))].sort();
    host.innerHTML = `<h2 id="archiveTopics">Coverage across the complete archive</h2>
      <p>Each question has one primary teaching area. A method can also help with questions listed in another area.</p>
      <div class="coverage-scroll" tabindex="0" role="region" aria-labelledby="archiveTopics"><table class="coverage-table">
      <thead><tr><th scope="col">Teaching area</th><th scope="col">All questions</th>
      ${bands.map(band => `<th scope="col">${band}</th>`).join('')}<th scope="col">Range per paper</th></tr></thead>
      <tbody>${archive.topics.map(topic => `<tr><th scope="row">${escape(topic.topic)}</th>
      <td>${topic.questions}</td>${bands.map(band => `<td>${topic.bands[band] || 0}</td>`).join('')}
      <td>${topic.minimum_per_paper}–${topic.maximum_per_paper}</td></tr>`).join('')}</tbody>
      <tfoot><tr><th scope="row">All areas</th><td>${archive.questions}</td>
      ${bands.map(band => `<td>${archive.topics.reduce((sum,topic) => sum+(topic.bands[band] || 0),0)}</td>`).join('')}<td>30</td></tr></tfoot></table></div>
      <details><summary>Explore ${archive.skills.length} problem-solving tools</summary>
      <label class="tool-filter"><span id="teachingAreaLabel">Teaching area</span> <select id="toolTopic" aria-labelledby="teachingAreaLabel"><option value="">All areas</option>
      ${topics.map(topic => `<option>${escape(topic)}</option>`).join('')}</select></label>
      <p id="toolCount" role="status"></p><div class="tool-list"></div></details>
      <h2>Choose a practice set</h2>
      <p><a href="tests.html?section=speed">Part A · Questions 1–20</a> gives you 20 multiple-choice problems to practise speed and accuracy.
      <a href="tests.html?section=depth">Part B · Questions 21–30</a> gives you 40 minutes for five multiple-choice problems and five whole-number answers.</p>
      <p>The table describes past papers. The mix of topics can change each year.</p>
      <p><a href="https://amt.edu.au/amc" target="_blank" rel="noopener">Australian Maths Trust competition information</a></p>`;
    const select = host.querySelector('#toolTopic');
    function displayTools() {
      const skills = archive.skills.filter(skill => !select.value || select.value === skill.topic);
      host.querySelector('.tool-list').innerHTML = skills.map(strategyCard).join('');
      host.querySelector('#toolCount').textContent = `${skills.length} ${skills.length === 1 ? 'tool' : 'tools'}`;
    }
    select.addEventListener('change',displayTools);
    displayTools();
    host.removeAttribute('role');
  } catch {
    host.textContent = 'The coverage map could not load. ';
    const retry = document.createElement('button');
    retry.type = 'button';
    retry.className = 'secondary';
    retry.textContent = 'Try again';
    retry.onclick = loadCoverage;
    host.append(retry);
  }
}
loadCoverage();
