// Pure exam state: shared by the page and boundary checks.
export function examClock(expiresAt, now=Date.now()){
  const seconds=Math.max(0,Math.ceil((new Date(expiresAt).getTime()-now)/1000));
  return {seconds,label:`${String(Math.floor(seconds/60)).padStart(2,'0')}:${String(seconds%60).padStart(2,'0')}`,prominent:seconds<=180,urgent:seconds<=60};
}
export function answerGaps(questions,responses,drafts={}){
  const missing=questions.filter(q=>responses[q.question_number]===undefined||responses[q.question_number]===null||responses[q.question_number]==='').map(q=>q.question_number);
  const unsaved=questions.filter(q=>Object.hasOwn(drafts,q.question_number)&&String(drafts[q.question_number])!==String(responses[q.question_number]??'')).map(q=>q.question_number);
  return {missing,unsaved};
}
