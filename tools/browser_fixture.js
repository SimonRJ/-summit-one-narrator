// Isolated browser-test adapter; only intercepted by tools/browser_check.mjs.
const db=globalThis.__fixture;
class Query{
 constructor(table){this.table=table;this.filters=[];this.sort=[];this.op='read'}
 select(){return this} eq(k,v){this.filters.push(x=>x[k]===v);return this}not(k,op,v){this.filters.push(x=>x[k]!==v);return this}order(k,o={}){this.sort.push([k,o.ascending!==false]);return this}range(a,b){this.span=[a,b];return this}limit(n){this.span=[0,n-1];return this}single(){this.one=true;return this}maybeSingle(){this.one=true;return this}insert(v){this.op='insert';this.value=v;return this}upsert(v,options={}){this.op='upsert';this.value=v;this.upsertOptions=options;return this}update(v){this.op='update';this.value=v;return this}
 then(ok,bad){return this.run().then(ok,bad)}
 async run(){let rows=(db[this.table]||[]).filter(x=>this.filters.every(f=>f(x)));if(this.op==='insert'||this.op==='upsert'){
 let row=structuredClone(this.value);if(this.op==='upsert'){const keys=this.upsertOptions.onConflict?.split(',')||(this.table==='session_records'?['user_id','session_number']:['user_id']);const prior=(db[this.table]||[]).find(x=>keys.every(k=>x[k]===row[k]));if(prior){if(!this.upsertOptions.ignoreDuplicates)Object.assign(prior,row);row=prior}else{row.id='fixture-'+(++db.counter);if(this.table==='learning_repairs')Object.assign(row,{stage:0,evidence:{},created_at:new Date().toISOString()});(db[this.table]||=[]).push(row)}}else{row.id='fixture-'+(++db.counter);row.reviewed_at=new Date().toISOString();if(this.table==='exam_sittings'){row.attempt_number=db.exam_sittings.filter(x=>x.exam_id===row.exam_id).length+1;row.started_at=new Date().toISOString();row.expires_at=new Date(Date.now()+3600000).toISOString();} (db[this.table]||=[]).push(row)}rows=[row];
 }else if(this.op==='update'){rows.forEach(x=>Object.assign(x,this.value))}
 for(const [k,asc] of [...this.sort].reverse())rows.sort((a,b)=>(a[k]<b[k]?-1:a[k]>b[k]?1:0)*(asc?1:-1));if(this.span)rows=rows.slice(this.span[0],this.span[1]+1);return {data:this.one?(rows[0]||null):structuredClone(rows),error:null}}
}
export const supabase={from:t=>new Query(t),auth:{getSession:async()=>({data:{session:{access_token:'fixture-token'}}})},rpc:async(name,{p_sitting_id,p_question,p_response})=>{const s=db.exam_sittings.find(x=>x.id===p_sitting_id);if(name==='get_exam_learning_map')return {data:s?.completed&&s?.submitted_at?structuredClone(db.exam_questions_student.filter(q=>q.exam_id===s.exam_id).map(q=>({question_number:q.question_number,category:q.category,metadata:q.metadata}))):[],error:null};if(p_response===null)delete s.responses[p_question];else s.responses[p_question]=p_response;return {data:structuredClone(s)}},functions:{invoke:async(name)=>({data:name==='get-problem-solution'?{solution_text:'Compare the totals, subtract the shared amount, and check the original conditions.'}:{correct:true,independent_credit:true}})}};
export const currentUser=async()=>({id:'fixture-learner'});
export const loadProgress=async()=>db.progress_state[0];
export const saveProgress=async patch=>Object.assign(db.progress_state[0],patch);
export const signOut=async()=>{};
export const upsertSession=async row=>(await new Query('session_records').upsert({user_id:'fixture-learner',...row}).single()).data;
