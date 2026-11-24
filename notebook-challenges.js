// Optional authored challenges use the learner's existing problem index and attempt history.
export function mountNotebookChallenges(target, { problems, history, submit, openSolution, showSolution }) {
  const choices = problems.filter(problem => problem.source_type === 'original_authored'
    && /^(?:K\d+|N\d+\.\d+)$/.test(problem.id));
  if (!choices.length) return;

  target.innerHTML = `<details class="review-detail"><summary>Extra challenge practice</summary>
    <p>Choose a challenge and submit your answer to open its worked solution.</p>
    <label>Challenge <select><option value="">Choose a challenge</option></select></label>
    <div class="math-copy"></div></details>`;
  const select = target.querySelector('select');
  const panel = target.querySelector('.math-copy');
  choices.forEach(problem => select.add(new Option(problem.title, problem.id)));
  select.addEventListener('change', () => {
    panel.replaceChildren();
    const problem = choices.find(entry => entry.id === select.value);
    if (!problem) return;
    const previous = history.findLast(entry => entry.problem_id === problem.id && entry.answer_text?.trim());
    panel.innerHTML = `<p data-prompt></p><form><label>Your answer or reasoning
      <textarea required maxlength="3000" rows="3"></textarea></label>
      <label><input type="checkbox"> I used help</label>
      <button type="submit" class="primary">Submit answer</button></form>
      <p role="status"></p><button type="button" class="secondary" data-replay hidden>Open worked solution</button><div data-solution></div>`;
    const prompt = panel.querySelector('[data-prompt]');
    const form = panel.querySelector('form');
    const answer = form.querySelector('textarea');
    const send = form.querySelector('button');
    const status = panel.querySelector('[role="status"]');
    const replay = panel.querySelector('[data-replay]');
    const solution = panel.querySelector('[data-solution]');
    prompt.textContent = problem.prompt;
    function graded(entry) {
      form.hidden = true;
      replay.hidden = false;
      const result = entry.is_correct === true ? 'Correct.' : entry.is_correct === false
        ? 'Check your reasoning against the worked solution.' : 'Compare your reasoning with the worked solution.';
      status.textContent = `Your saved answer: ${entry.answer_text}. ${result}`;
    }
    if (previous) graded(previous);
    form.addEventListener('submit', async event => {
      event.preventDefault();
      const response = answer.value.trim();
      if (!response || send.disabled) return;
      send.disabled = true;
      status.textContent = 'Saving your answer…';
      try {
        const entry = await submit(problem.id, response, form.querySelector('input').checked);
        graded(entry);
      } catch (error) {
        status.textContent = error.message;
      } finally {
        send.disabled = false;
      }
    });
    replay.addEventListener('click', async () => {
      replay.disabled = true;
      try {
        const data = await openSolution(problem.id);
        showSolution(solution, data, problem.id);
        replay.hidden = true;
      } catch (error) {
        status.textContent = error.message;
        replay.disabled = false;
      }
    });
  });
}
