const publishedSlots = new Set([1, 2, 3, 4, 5]);
export const INTRO_MEDIA_VERSION = "lesson-intros-v2";

export function lessonIntroId(slot) {
  const number = Number(slot);
  return publishedSlots.has(number) ? "S" + String(number).padStart(3, "0") : null;
}
