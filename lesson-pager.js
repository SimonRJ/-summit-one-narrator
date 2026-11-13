/** Fixed-screen navigation: preserve the lesson DOM and its saved answer handlers.
 *  Only one compact teaching card is displayed at a time. No scrolling is used to advance.
 */
export function mountLessonPager({pages,initial=0,footer,onBack,onNext,onChange}){
 if(!Array.isArray(pages)||!pages.length)throw new Error("Lesson screen has no pages");
 const back=footer.querySelector("[data-screen-back]");
 const next=footer.querySelector("[data-screen-next]");
 const count=footer.querySelector("[data-screen-count]");
 const name=footer.querySelector("[data-screen-name]");
 let index=Math.max(0,Math.min(pages.length-1,Number(initial)||0));
 let busy=false;
 function show(value){
  index=Math.max(0,Math.min(pages.length-1,value));
  pages.forEach((p,i)=>p.show(i===index));
  const p=pages[index];
  if(count)count.textContent=`${index+1} / ${pages.length}`;
  if(name)name.textContent=p.title||"Learning";
  if(back)back.textContent=index===0?"Back":"Previous";
  if(next)next.textContent=index===pages.length-1?(p.finishLabel||"Continue"):"Next";
  const active=document.activeElement;
  if(active&&footer.contains(active)){} // Keyboard focus stays on Back/Next for predictable navigation.
  onChange?.(index,p);
 }
 async function advance(){
  if(busy)return;busy=true;try{
   const p=pages[index];
   if(p.guard&&await p.guard()===false)return;
   if(index<pages.length-1){show(index+1);return}
   await onNext?.();
  }finally{busy=false}
 }
 async function retreat(){
  if(busy)return;busy=true;try{
   if(index>0){show(index-1);return}
   await onBack?.();
  }finally{busy=false}
 }
 back.onclick=()=>retreat().catch(e=>alert(e.message));
 next.onclick=()=>advance().catch(e=>alert(e.message));
 footer.addEventListener("keydown",e=>{
  if(e.altKey||e.ctrlKey||e.metaKey||e.target.closest("input,textarea,select"))return;
  if(e.key==="ArrowLeft"){e.preventDefault();back.click()}
  if(e.key==="ArrowRight"){e.preventDefault();next.click()}
 });
 show(index);
 return {show,advance,retreat,get index(){return index},get count(){return pages.length}};
}
