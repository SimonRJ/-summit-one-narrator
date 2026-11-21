// All numerical answer keys in the lesson banks are integers or exact fractions.
const vulgar = new Map(Object.entries({
  '½':'1/2', '⅓':'1/3', '⅔':'2/3', '¼':'1/4', '¾':'3/4',
  '⅕':'1/5', '⅖':'2/5', '⅗':'3/5', '⅘':'4/5', '⅙':'1/6', '⅚':'5/6',
  '⅐':'1/7', '⅛':'1/8', '⅜':'3/8', '⅝':'5/8', '⅞':'7/8', '⅑':'1/9', '⅒':'1/10',
}));

export function exactValue(input) {
  let text = String(input ?? '').trim();
  if (!text || text.length > 120) return null;
  text = text.replace(/−/g, '-').replace(/[⁄∕]/g, '/');
  const glyph = vulgar.get(text.at(-1));
  if (glyph) text = text.slice(0, -1).trimEnd() + ' ' + glyph;
  text = text.trim().replace(/^([+-])\s+/, '$1');
  // A separator must delimit a complete group of three digits. A list stays a list.
  if (/^[+-]?\d{1,3}(?:,\d{3})+(?:\.\d+)?$/.test(text)) text = text.replaceAll(',', '');
  if (/^[+-]?\d{1,3}(?:[\u0020\u00a0\u202f]\d{3})+(?:\.\d+)?$/.test(text)) text = text.replace(/[\u0020\u00a0\u202f]/g, '');
  const mixed = /^([+-]?)(\d+)\s+(\d+)\s*\/\s*(\d+)$/.exec(text);
  if (mixed) {
    const [whole, part, denominator] = mixed.slice(2).map(BigInt);
    if (part >= denominator || denominator === 0n) return null;
    return {n: (mixed[1] === '-' ? -1n : 1n) * (whole * denominator + part), d: denominator, form:'mixed'};
  }
  const fraction = /^([+-]?\d+)\s*\/\s*(\d+)$/.exec(text);
  if (fraction && BigInt(fraction[2]) > 0n) {
    return {n:BigInt(fraction[1]), d:BigInt(fraction[2]), form:'fraction'};
  }
  const decimal = /^([+-]?)(?:(\d+)(?:\.(\d*))?|\.(\d+))$/.exec(text);
  if (!decimal) return null;
  const digits = decimal[3] || decimal[4] || '';
  return {n:BigInt((decimal[2] || '0') + digits) * (decimal[1] === '-' ? -1n : 1n),
    d:10n ** BigInt(digits.length), form:digits ? 'decimal' : 'integer'};
}

function commonFactor(a, b) {
  a = a < 0n ? -a : a;
  while (b) [a, b] = [b, a % b];
  return a;
}

export function numericResponse(expected, response, prompt = '') {
  const key = exactValue(expected);
  if (!key) return null;
  let written = String(response ?? '').trim();
  const percent = written.endsWith('%');
  if (percent) written = written.slice(0, -1).trimEnd();
  const value = exactValue(written);
  if (!value) return {correct:null, message:'Enter one final value, such as 12, 3/4 or 2 1/2. Use the unit named in the question.'};

  if (percent) {
    const asksPercentage = /(?:what|which|by what|find the) (?:\w+[ -]){0,3}percent(?:age)?\b|enter (?:the|your) percentage|as a percentage|percentage (?:increase|decrease|discount)\?/i.test(prompt);
    const asksProportion = /(?:what|which|find the) (?:fraction|probability|proportion|chance)\b|probability (?:of|that)|chance (?:of|that)/i.test(prompt);
    if (!asksPercentage && !asksProportion) return {correct:null, message:'Enter the answer in the unit requested in the question.'};
    if (!asksPercentage) value.d *= 100n;
  }
  if (/fraction in (?:its |the )?(?:simplest|lowest) (?:form|terms)/i.test(prompt) &&
      (percent || value.form !== 'fraction' || commonFactor(value.n, value.d) !== 1n)) {
    return {correct:null, message:'Write one fraction in lowest terms before checking it.'};
  }
  return {correct:key.n * value.d === value.n * key.d};
}
