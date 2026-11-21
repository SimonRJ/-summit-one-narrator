// These investigations use the example currently drawn in the lesson model.
export const modelClaims = {
  'SOLID-01': [
    {
      name: 'Hidden cubes', claim: 'From the front, the entire back-left stack is hidden behind the front-left stack.',
      test: s => s.height <= 3, example: s => `Front left: 3 cubes. Back left: ${s.height}.`,
      verdict: 'Sometimes', clue: 'Try a back-left stack equal in height to the front one, then make it taller.',
      reason: 'At heights 1, 2 and 3 the front stack hides every cube behind it. At heights 4 and 5 the back stack rises above it.'
    },
    {
      name: 'The right column', claim: 'The right column of the front outline is four cubes high.',
      test: s => s.rightHeight === 4, example: s => `Back left: ${s.height}. The front view on the right is ${s.rightHeight} cubes high.`,
      verdict: 'Always', clue: 'Which two stacks make the right column of the front view?',
      reason: 'Only the two right-hand stacks set that height. They are fixed at 2 and 4, so the outline reaches 4 however you change the left stack.'
    },
    {
      name: 'Two layers', claim: 'Layer 3 contains more cubes than layer 2.',
      test: s => s.third > s.second, example: s => `Back left: ${s.height}. Layer 2 has ${s.second} cubes and layer 3 has ${s.third}.`,
      verdict: 'Never', clue: 'Look directly below every cube on layer 3.',
      reason: 'Every cube on layer 3 has its own supporting cube on layer 2. Layer 2 can have extra cubes, but layer 3 cannot outnumber it.'
    }
  ],
  'SPATIAL-02': [
    {
      name: 'A square outline', claim: 'The selected rectangle is a square.',
      test: s => s.width === s.height, example: s => `At ${s.cell}, outline ${s.frame} is ${s.width} cells wide and ${s.height} high.`,
      verdict: 'Sometimes', clue: 'Keep the marked cell and change the outline. Compare its width with its height.',
      reason: 'The one-cell outline is square. The outline around the whole four-by-three grid also contains the marked cell and has unequal sides.'
    },
    {
      name: 'A half-turn', claim: 'The marked cell and its partner after a half-turn belong to the same number of rectangles.',
      test: s => s.count === s.partnerCount, example: s => `${s.cell} belongs to ${s.count} rectangles. Its partner ${s.partner} belongs to ${s.partnerCount}.`,
      verdict: 'Always', clue: 'Imagine turning the marked cell and its enclosing rectangle together.',
      reason: 'A half-turn sends each enclosing rectangle to one enclosing the partner cell. Turn it again to get the original back. That pairs them up exactly.'
    },
    {
      name: 'An odd perimeter', claim: 'The selected rectangle has a perimeter of seven cell edges.',
      test: s => 2 * (s.width + s.height) === 7, example: s => `The ${s.width}-by-${s.height} outline has a perimeter of ${2 * (s.width + s.height)} cell edges.`,
      verdict: 'Never', clue: 'Pair each side with the side opposite it.',
      reason: 'The perimeter is twice the sum of two whole-number side lengths, so it is even. Seven is odd.'
    }
  ],
  'GEO-05': [
    {
      name: 'Wider than deep', claim: 'The pen is wider than it is deep.',
      test: s => s.width > s.depth, example: s => `${s.wall ? 'With a wall' : 'With four fenced sides'}, the pen is ${s.width} m wide and ${s.depth} m deep.`,
      verdict: 'Sometimes', clue: 'Keep the same boundary and compare a shallow pen with a deep one.',
      reason: 'With four fenced sides, a depth of 2 m gives a width of 10 m. Swapping those dimensions uses the same 24 m of fencing and reverses the comparison.'
    },
    {
      name: 'Using the wall', claim: 'At the same depth, using the back wall doubles the area compared with fencing all four sides.',
      test: s => s.wallWidth * s.depth === 2 * s.closedWidth * s.depth,
      example: s => `At depth ${s.depth} m: four fenced sides give ${s.closedWidth * s.depth} m² and the wall gives ${s.wallWidth * s.depth} m².`,
      verdict: 'Always', clue: 'After fencing both sides that run front to back, where does the remaining fence go?',
      reason: 'With four sides, the leftover fencing is shared equally between front and back. With the wall, it all goes across the front. Twice the width at the same depth gives twice the area.'
    },
    {
      name: 'Two long dimensions', claim: 'The pen is both more than 8 m wide and more than 8 m deep.',
      test: s => s.width > 8 && s.depth > 8, example: s => `Width: ${s.width} m. Depth: ${s.depth} m. Fence available: 24 m.`,
      verdict: 'Never', clue: 'Count the front and the two side fences, even when there is a back wall.',
      reason: 'The front and two sides alone would each need more than 8 m. Those three lengths would already use more than 24 m.'
    }
  ]
};

export function mountClaimChallenge(body, claims, readExample, initial) {
  const panel = document.createElement('details');
  panel.className = 'lm-claims';
  panel.innerHTML = `<summary>Always, sometimes or never?</summary>
    <label>Choose a claim<select></select></label>
    <p class="lm-claim-text"></p>
    <p>Change the diagram above and save an example. For “sometimes”, find a case on each side.</p>
    <button type="button" class="lm-save-case">Use this example</button>
    <ul class="lm-cases"></ul>
    <fieldset><legend>When is the claim true?</legend>
      <button type="button">Always</button><button type="button">Sometimes</button><button type="button">Never</button>
    </fieldset>
    <p class="lm-verdict" role="status"></p>`;
  body.append(panel);
  const select = panel.querySelector('select');
  for (const entry of claims) select.add(new Option(entry.name));
  const saved = new Map();
  const evidence = panel.querySelector('.lm-cases');
  const message = panel.querySelector('.lm-verdict');
  const current = () => claims[select.selectedIndex];
  function chooseClaim() {
    panel.querySelector('.lm-claim-text').textContent = current().claim;
    saved.clear();
    evidence.replaceChildren();
    message.textContent = '';
  }
  select.selectedIndex = initial % claims.length;
  chooseClaim();
  select.addEventListener('change', chooseClaim);
  panel.querySelector('.lm-save-case').addEventListener('click', () => {
    const state = readExample();
    const claim = current();
    const holds = claim.test(state);
    const detail = claim.example(state);
    const item = saved.get(holds) || document.createElement('li');
    item.textContent = (holds ? 'Claim holds. ' : 'Counterexample. ') + detail;
    if (!saved.has(holds)) evidence.append(item);
    saved.set(holds, item);
    message.textContent = saved.size === 2 ? 'You have an example on each side. Which conclusion follows?' : item.textContent;
  });
  for (const choice of panel.querySelectorAll('fieldset button')) {
    choice.addEventListener('click', () => {
      const claim = current();
      if (choice.textContent !== claim.verdict) {
        message.textContent = claim.clue;
      } else if (claim.verdict === 'Sometimes' && saved.size < 2) {
        message.textContent = 'Yes. Show why by saving one example where it holds and one counterexample. ' + claim.clue;
      } else {
        message.textContent = claim.verdict + '. ' + claim.reason;
      }
    });
  }
}
