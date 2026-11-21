// Only marked question numbers are stored. One entry per question lets separate tabs mark different questions.
export function createExamFlags(userId, sittingId, questionNumbers, store) {
  const prefix = 'summit-one:exam-flag:' + encodeURIComponent(userId) + ':' + encodeURIComponent(sittingId) + ':';
  const keys = new Map(questionNumbers.map(number => [prefix + number, number]));
  const marked = new Set();
  try {
    if (store === undefined) store = globalThis.localStorage;
    for (const [key, number] of keys) if (store.getItem(key) === '1') marked.add(number);
  } catch { /* The question marks still work during this visit. */ }

  return {
    has(number) { return marked.has(number); },
    toggle(number) {
      const key = prefix + number;
      if (!keys.has(key)) return;
      const adding = !marked.has(number);
      if (adding) marked.add(number);
      else marked.delete(number);
      try {
        if (adding) store.setItem(key, '1');
        else store.removeItem(key);
      } catch { /* Keep the in-memory mark when browser storage is unavailable. */ }
    },
    sync(event) {
      if (event.storageArea !== store) return false;
      if (event.key === null) { marked.clear(); return true; }
      if (!keys.has(event.key)) return false;
      const number = keys.get(event.key);
      if (event.newValue === '1') marked.add(number);
      else marked.delete(number);
      return true;
    },
    clear() {
      marked.clear();
      try { for (const key of keys.keys()) store.removeItem(key); } catch {}
    }
  };
}
