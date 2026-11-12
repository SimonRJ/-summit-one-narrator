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

/**
 * Elapsed-time display for Summit One split AMC practice.
 * The server's immutable expiry remains the authority on when an attempt ends.
 */
export function elapsedClock(startedAt,expiresAt,now=Date.now()){
  const start=new Date(startedAt).getTime(),expiry=new Date(expiresAt).getTime();
  const duration=Math.max(0,Math.round((expiry-start)/1000));
  const seconds=Math.max(0,Math.min(duration,Math.floor((now-start)/1000)));
  return {seconds,label:`${String(Math.floor(seconds/60)).padStart(2,'0')}:${String(seconds%60).padStart(2,'0')}`,limitSeconds:duration};
}
