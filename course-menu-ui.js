/** Vertical course navigation: green checks mean completed and reviewable. */
export function mountCourseMenu({navigation,getDone,getCurrent,onContinue,onCompleted,onIntroduction,onView}){
  const dialog=document.getElementById("courseMenu");
  const toggle=document.getElementById("menuToggle");
  const close=document.getElementById("menuClose");
  const content=document.getElementById("courseMenuContent");
  const title=document.getElementById("courseMenuTitle");
  const badge=document.getElementById("navProgress");
  if(!dialog||!toggle||!close||!content||!title||!badge)throw new Error("Course menu controls unavailable");
  let state={level:"root",section:null,group:null};
  const escape=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
  const btn=(name,label,detail)=>`<button type="button" class="course-menu-row course-menu-entry" data-menu-screen="${escape(name)}"><span class="course-menu-copy"><b>${escape(label)}</b><small>${escape(detail)}</small></span><span class="course-menu-chevron" aria-hidden="true">›</span></button>`;
  const action=(key,label,detail)=>`<button type="button" class="course-menu-row course-menu-entry" data-menu-action="${escape(key)}"><span class="course-menu-copy"><b>${escape(label)}</b><small>${escape(detail)}</small></span></button>`;
  const link=(href,label,detail)=>`<a class="course-menu-row course-menu-entry" href="${escape(href)}"><span class="course-menu-copy"><b>${escape(label)}</b><small>${escape(detail)}</small></span><span class="course-menu-chevron" aria-hidden="true">›</span></a>`;
  const statusOf=item=>item.slot<=(Number(getDone())||0)?"completed":getCurrent()?.slot===item.slot?"current":"locked";
  function refreshProgress(){
    const done=Math.max(0,Math.min(372,Number(getDone())||0));
    badge.textContent=done+" / 372";
    badge.closest("button")?.setAttribute("aria-label",`Progress and profile: ${done} of 372 sessions completed, ${372-done} remaining`);
    return done;
  }
  function groupRow(group){
    const completed=group.items.filter(item=>statusOf(item)==="completed").length;
    return `<button type="button" class="course-menu-row course-menu-group" data-menu-group="${escape(group.id)}"><span class="course-menu-copy"><b>${escape(group.title)}</b><small>${group.items.length} ${group.kind==="LESSON"?"lessons":"sessions"} · ${completed} completed</small></span><span class="course-menu-chevron" aria-hidden="true">›</span></button>`;
  }
  function sessionRow(item){
    const status=statusOf(item),number=String(item.slot).padStart(3,"0");
    const label=`Session ${number}. ${item.focus}. ${status==="completed"?"Completed, open saved review":status==="current"?"Current, continue":"Not yet available"}.`;
    const marker=status==="completed"?"✓":status==="current"?"▶":"○";
    const detail=status==="completed"?"Completed · View saved working":status==="current"?"Continue this session":"Upcoming · Follows the course path";
    const inner=`<span class="course-menu-number">${number}</span><span class="course-menu-copy"><b>${escape(item.focus)}</b><small>${escape(detail)}</small></span><span class="course-menu-status ${status}" aria-hidden="true">${marker}</span>`;
    if(status==="locked")return `<div class="course-menu-row course-menu-session is-locked" aria-label="${escape(label)}">${inner}</div>`;
    const availableIntro=item.type==="LESSON";
    const publishedFilm=item.slot===1||item.slot===2;
    const watch=availableIntro?`<button type="button" class="course-menu-watch" data-menu-intro-slot="${item.slot}" aria-label="${escape(publishedFilm?"Watch introduction video for session "+number:"Review teaching for session "+number)}" title="${publishedFilm?"Watch introduction":"Review teaching"}">${publishedFilm?"Watch intro":"Teaching"}</button>`:"";
    return `<div class="course-menu-row course-menu-session is-${status}" data-menu-slot="${item.slot}"><button type="button" class="course-menu-session-main" aria-label="${escape(label)}">${inner}</button>${watch}</div>`;
  }
  function groups(){
    if(state.section==="lessons")return navigation.topics;
    if(state.section==="mawa")return navigation.mawa;
    if(state.section==="mixed")return navigation.mixed;
    return [];
  }
  function redraw(){
    const done=refreshProgress();
    if(state.level==="root"){
      title.textContent="Menu";
      const current=getCurrent();
      content.innerHTML=`<section class="course-menu-current"><span class="eyebrow">CURRENT LEARNING</span><b>${done>=372?"All 372 sessions completed":`Session ${current?.slot??"—"} · ${escape(current?.focus||"")}`}</b><button type="button" class="course-menu-continue" data-menu-action="continue">${done>=372?"See progress":"Continue lesson"}</button>${done<372&&current?.type==="LESSON"?`<button type="button" class="course-menu-current-intro" data-menu-intro-slot="${current.slot}">Watch lesson introduction</button>`:""}</section>
        <div class="course-menu-divider" role="separator"></div>
        ${btn("lessons","Lessons",`${navigation.totals.lessons} technique lessons · ${navigation.topics.length} maths categories`)}
        ${btn("mawa","MAWA investigations",`${navigation.totals.mawa} investigations`)}
        ${btn("mixed","Strategy workshops",`${navigation.totals.workshops} workshops`)}
        ${btn("exams","Exams","AMC practice, real papers and Rossmoyne")}
        <div class="course-menu-divider" role="separator"></div>
        ${action("profile","Progress & profile","Completion, milestones and results")}
        ${action("review","Completed sessions","Your original answers and working")}
        ${action("repairs","Repairs & revision","Unresolved problems and techniques")}
        ${action("roadmap","Goals & readiness","Current targets and milestones")}
        ${link("welcome.html?from=dashboard","AMC introduction","What the competition involves")}`;
    }else if(state.level==="sections"){
      title.textContent={lessons:"Lessons",mawa:"MAWA investigations",mixed:"Strategy workshops",exams:"Exams"}[state.section]||"Menu";
      if(state.section==="exams"){
        content.innerHTML=`<button type="button" class="course-menu-back" data-menu-back="root">‹ All menu sections</button>
          ${link("tests.html?section=speed","AMC Practice · Part A","Questions 1–20 · 20 minutes")}
          ${link("tests.html?section=depth","AMC Practice · Part B","Questions 21–30 · 40 minutes")}
          ${link("tests.html?section=amc","Real AMC exams","Authentic Upper Primary papers")}
          ${link("tests.html?section=rossmoyne","Rossmoyne Honours","Specialist entrance preparation")}
          ${link("tests.html","All exam results","Exam centre and saved attempts")}`;
      }else{
        content.innerHTML=`<button type="button" class="course-menu-back" data-menu-back="root">‹ All menu sections</button>
          <p class="course-menu-explainer">Choose a topic to see its sessions in course order. Completed lessons have a green check; future sessions remain locked.</p>
          ${groups().map(groupRow).join("")}`;
      }
    }else{
      const group=groups().find(g=>g.id===state.group);
      if(!group){state={level:"sections",section:state.section,group:null};redraw();return}
      title.textContent=group.title;
      content.innerHTML=`<button type="button" class="course-menu-back" data-menu-back="sections">‹ ${escape({lessons:"Maths categories",mawa:"Investigations",mixed:"Workshops"}[state.section]||"Categories")}</button>
        <p class="course-menu-explainer">${group.items.length} ${group.kind==="LESSON"?"lessons":"sessions"} in their original numbered order. <span class="course-menu-legend"><span class="legend-complete">✓ completed</span> · <span class="legend-current">▶ current</span> · ○ locked</span></p>
        <div class="course-menu-session-list">${group.items.map(sessionRow).join("")}</div>`;
    }
    content.scrollTop=0;
  }
  function show(){
    state={level:"root",section:null,group:null};
    redraw();
    if(!dialog.open)dialog.showModal();
    toggle.setAttribute("aria-expanded","true");
    close.focus();
  }
  function hide(){
    if(dialog.open)dialog.close();
    toggle.setAttribute("aria-expanded","false");
  }
  toggle.addEventListener("click",()=>dialog.open?hide():show());
  close.addEventListener("click",hide);
  dialog.addEventListener("close",()=>toggle.setAttribute("aria-expanded","false"));
  dialog.addEventListener("click",event=>{if(event.target===dialog)hide()});
  content.addEventListener("click",async event=>{
    const group=event.target.closest("[data-menu-group]");
    const screen=event.target.closest("[data-menu-screen]");
    const back=event.target.closest("[data-menu-back]");
    const actionButton=event.target.closest("[data-menu-action]");
    const introduction=event.target.closest("[data-menu-intro-slot]");
    const session=event.target.closest("[data-menu-slot]");
    if(back){
      state=back.dataset.menuBack==="root"?{level:"root",section:null,group:null}:{level:"sections",section:state.section,group:null};
      redraw();return
    }
    if(screen){state={level:"sections",section:screen.dataset.menuScreen,group:null};redraw();return}
    if(group){state={level:"group",section:state.section,group:group.dataset.menuGroup};redraw();return}
    if(introduction){
      const slot=Number(introduction.dataset.menuIntroSlot);
      const item=navigation.all.find(x=>x.slot===slot);
      if(!item||item.type!=="LESSON"||statusOf(item)==="locked")return;
      hide();
      try{await onIntroduction(slot)}
      catch(error){alert(error.message)}
      return;
    }
    if(session){
      const slot=Number(session.dataset.menuSlot);
      const item=navigation.all.find(x=>x.slot===slot);
      if(!item)return;
      const status=statusOf(item);
      if(status==="locked")return;
      hide();
      try{if(status==="completed")await onCompleted(slot);else await onContinue()}
      catch(error){alert(error.message)}
      return
    }
    if(actionButton){
      const key=actionButton.dataset.menuAction;
      hide();
      try{if(key==="continue")await onContinue();else await onView(key)}
      catch(error){alert(error.message)}
    }
  });
  dialog.querySelector("[data-menu-action='profile']")?.addEventListener("click",async()=>{hide();try{await onView("profile")}catch(e){alert(e.message)}});
  refreshProgress();
  return {show,hide,refreshProgress,refresh(){if(dialog.open)redraw();else refreshProgress()}};
}
