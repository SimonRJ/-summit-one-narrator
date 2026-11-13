import assert from 'node:assert/strict';
import fs from 'node:fs';
const read=p=>fs.readFileSync(new URL(p,import.meta.url),'utf8');
const app=read('../app-main.js'),css=read('../main.css'),html=read('../index.html'),sw=read('../sw.js');
const screens=read('../lesson-screenflow.js'),pager=read('../lesson-pager.js');
const lessons=JSON.parse(read('../data/sessions-372.json')).sessions;
assert.equal(lessons.length,372);
assert.equal(lessons[0].focus,'Divisibility tests and modular remainders');
assert.equal(lessons[1].focus,'Place-value decomposition and estimation');
for(let i=0;i<2;i++){
 const id='S00'+(i+1),data=JSON.parse(read('../production/lesson-intros/'+id+'.json'));
 assert.equal(data.id,id);
 assert.equal(data.segments.length,9);
 assert.equal(data.pause_seconds.length,9);
 assert.deepEqual(data.examples.map(x=>x.level),['easy','medium','hard']);
 assert(data.segments.at(-1).toLowerCase().includes('your turn'));
 assert(data.voice.includes('voice C'));
 assert(data.segments.every(x=>x.length>100));
 assert(!data.segments.join(' ').toLowerCase().includes('george'));
}
assert.equal(2473%3,1);
assert.equal(1739%6,5);
assert.equal(279%5,4);
assert.equal(279%7,6);
assert.equal(279%9,0);
assert.equal(398+207,605);
assert.equal(57*98,5586);
assert.equal(49996*50004,50000**2-16);
assert.equal(49996*50004-(50000**2-17),1);
assert(/function renderLessonOpening/.test(app));
assert(/function renderSession/.test(app));
assert(/activeStage=-1/.test(app));
assert(/activeLessonPanel/.test(app));
assert(/S001-Intro\.mp4/.test(app)||/\$\{id\}-Intro\.mp4/.test(app));
assert(/data-screen-back/.test(app));
assert(/data-screen-next/.test(app));
assert(/mountLessonPager/.test(app));
assert(/learningScreens/.test(app));
for(let stage=-1;stage<=4;stage++){
 assert(screens.includes('stage==='+stage)||stage===-1&&screens.includes('stage===-1'), 'Missing stage '+stage);
}
for(const s of ['renderChallenge','renderCheck','submit-problem-attempt','get-problem-solution','upsertSession','rememberDraft'])assert(app.includes(s),'Missing protected learning feature '+s);
assert(pager.includes('pages[index].show(true)'));
assert(pager.includes('onChange?.(index,p)'));
assert(pager.includes('scrollContainer.scrollTop=0'));
assert(app.includes('scrollContainer:target'));
assert(css.includes('2026-11-13 responsive lessons'));
assert(css.includes('overflow-y:auto;'));
assert(css.includes('.lesson-screen-stage .problem-card,'));
assert(css.includes('body.lesson-fullscreen{height:100dvh;overflow:hidden'));
assert(css.includes('.lesson-screen-footer'));
assert(css.includes('.opening-video-wrap'));
assert(sw.includes('lesson-screenflow.js?v=cinematic-practice-20261113'));
assert(sw.includes('lesson-pager.js?v=responsive-20261113'));
assert(html.includes('app-main.js?v=responsive-20261113'));
assert(html.includes('id="courseMenu"') && html.includes('id="menuToggle"'));
assert(html.includes('id="menuClose"') && html.includes('id="courseMenuContent"'));
assert(!html.includes('class="topnav"'), 'No horizontal tabs');
const menuModel=read('../course-menu.js');
const menuUI=read('../course-menu-ui.js');
const buildCourseNavigation=new Function(menuModel.replace(/^export /gm,'')+';return buildCourseNavigation')();
const grouped=buildCourseNavigation(lessons,JSON.parse(read('../data/taxonomy-52.json')));
assert.deepEqual(grouped.totals,{lessons:283,mawa:53,workshops:36,total:372});
assert.equal(grouped.topics.length,13,'12 mathematical topics plus capstone');
assert.equal(grouped.mawa.length,3);
assert.equal(grouped.mixed.length,2);
for(const section of [grouped.topics,grouped.mawa,grouped.mixed])for(const g of section)
 assert.deepEqual(g.items.map(x=>x.slot),g.items.map(x=>x.slot).sort((a,b)=>a-b),'Category must be chronological');
const unique=grouped.all.map(x=>x.slot);
assert.equal(new Set(unique).size,372);
assert(menuUI.includes('class="course-menu-status ${status}"'));
assert(menuUI.includes('status==="completed"?"✓"'));
assert(menuUI.includes('is-locked') && menuUI.includes('is-${status}') && menuUI.includes('status==="current"'));
assert(menuUI.includes('onCompleted(slot)') && menuUI.includes('onContinue()'));
assert(menuUI.includes('data-menu-intro-slot') && menuUI.includes('onIntroduction(slot)'));
assert(menuUI.includes('status==="locked"') && menuUI.includes('item.type==="LESSON"'));
assert(menuUI.includes('Watch intro') && menuUI.includes('Teaching'));
const readOnlyReplay=app.slice(app.indexOf('async function openLessonIntroductionFromMenu('),app.indexOf('function wireNav(){'));
assert(readOnlyReplay.includes('id="replayIntroVideo"') && readOnlyReplay.includes('media/${introId}-Intro.mp4'));
assert(readOnlyReplay.includes('renderHome') && readOnlyReplay.includes('openCompletedFromMenu(slot)'));
assert(!/upsertSession\(|recordVideoEvidence\(|submit-problem-attempt|completeSession\(/.test(readOnlyReplay),'Replays must never mutate a locked sitting');
assert(app.includes('data-video-session') && app.includes('saved-intro'));
assert(css.includes('.course-menu-watch') && css.includes('body.lesson-video-review'));
assert(app.includes('buildCourseNavigation(course,taxonomy)'));
assert(app.includes('mountCourseMenu(') && app.includes('data-review-session'));
assert(css.includes('.course-menu-status.completed') && css.includes('.course-menu-status.current'));
assert(css.includes('.course-menu-status.locked') && css.includes('dialog.course-menu'));
assert(sw.includes('./course-menu-ui.js?v=lesson-replay-20261113') && sw.includes('./course-menu.js?v=menu-20261113'));
const focusedHome=app.slice(app.indexOf('function renderHome(){'),app.indexOf('async function startSession(s){'));
assert(focusedHome.includes('focus-session-card') && focusedHome.includes('id="continue"'));
assert(!focusedHome.includes('side-stack') && !focusedHome.includes('learning-note') && !focusedHome.includes('learning-to-exams'));
assert(app.includes('profile-upcoming') && app.includes('sessions remaining'));
assert(css.includes('body.home-focus{min-height:100dvh;height:100dvh;overflow:hidden'));
assert(css.includes('.course-menu-session.is-completed') && css.includes('.focus-session-card'));
assert(sw.includes('summit-one-math-label-fix-20261113'));
assert(!app.includes('node.scrollIntoView({behavior:\'smooth\',block:\'start\'});'));

const loader=read('../boot-loader.js'),loaderCss=read('../boot-loader.css');
const practiceUI=read('../transfer-practice.js'),originalLearning=read('../original-learning.js');
assert(html.includes('id="summitBoot"') && html.includes('data-mode="main"'));
assert(html.includes('boot-loader.js?v=identity-math-20261113'));
assert(sw.includes('boot-loader.css?v=cinematic-20261113'));
assert(loader.includes('SummitLoader={ready,beginSmall,endSmall,withSmallLoading'));
assert(loader.includes('Play sound') && loader.includes('prefers-reduced-motion'));
assert(loaderCss.includes('.sb-facet--left') && loaderCss.includes('.summit-mini'));
assert(screens.includes('data-extra-question') && screens.includes('drill:'));
assert(screens.includes('showTop([summary,foot])'));
assert(!screens.includes('What clue tells you the method?'));
assert(!screens.includes('Explain your plan'));
assert(!practiceUI.includes('class="answer-box method"'));
assert(!originalLearning.includes('data-reason="clue"'));
assert(!app.includes("Before submitting, record the clue"));
assert(!html.includes('working-box') && html.includes('class="answer-box final-answer-input"'));
assert(app.includes("for(let i=0;i<3;i++)") && app.includes("'drill:'+mode+':'+s.slot+':'+i"));
assert(app.includes('modeKeys.every(key=>sessionDraft.evidence[key])'));
assert(!app.includes('id="workshopReflection"') && !app.includes('id="takeaway"'));

const design=read('../design-system.css'),maths=read('../math-typography.js'),brand=read('../summit-mark.svg');
assert(html.includes('summit-mark.svg') && html.includes('design-system.css?v=math-label-fix-20261113'));
assert(html.includes('math-typography.js?v=math-label-fix-20261113'));
assert(html.includes('katex@0.16.47/dist/katex.min.css') && html.includes('katex@0.16.47/dist/katex.min.js'));
assert(design.includes('Source Sans 3') && design.includes('Source Serif 4') && design.includes('STIX Two Math'));
assert(brand.includes('M142 19 25 232 142 157Z'));
assert(maths.includes('plainToTeX') && maths.includes('typesetMath'));
const {plainToTeX,findMathExpressions}=await import('../math-typography.js');
const expressions=s=>findMathExpressions(s).map(x=>x.formula);
for(const label of [
 'TRANSFER · PROBLEM 1 OF 3',
 'PRACTICE · PROBLEM 2 OF 3',
 'YOUR TURN · FINISH THE NEXT EXAMPLE',
 'BRIDGE · ADD ONE NEW IDEA',
 'LEARNING SESSION 2 / 372 · FOUNDATIONS',
 '6 / 6',
 '10:30'
])assert.deepEqual(expressions(label),[],'UI label incorrectly typeset: '+label);
assert.deepEqual(expressions('3/4 + 1/2 = 5/4'),['3/4 + 1/2 = 5/4']);
assert.deepEqual(expressions('a² + b² = c²'),['a² + b² = c²']);
assert.deepEqual(expressions('49 + 26 = 75'),['49 + 26 = 75']);
assert.deepEqual(expressions('N=qd+r'),['N=qd+r']);
assert(expressions('LCM(4,6,9)=36').includes('LCM(4,6,9)=36'));
assert(!maths.includes('"button","label"'),'Choice-button maths should remain eligible for typesetting');
assert.equal(plainToTeX('a² + b² = c²'), 'a^{2} + b^{2} = c^{2}');
assert.equal(plainToTeX('3/4'), String.raw`\frac{3}{4}`);
assert.equal(plainToTeX('a/b'), String.raw`\frac{a}{b}`);
assert.equal(plainToTeX('∑'), String.raw`\sum `);
assert(maths.includes('data-math-tex') && maths.includes('math-fallback'));

assert.equal(plainToTeX('2^3 × 5²').replace(/\s{2,}/g,' '), String.raw`2^3 \times 5^{2}`);
assert.equal(plainToTeX('N=qd+r, 0≤r<d'), String.raw`N=qd+r, 0\leq r<d`);
assert(sw.includes('summit-mark.svg') && sw.includes('math-typography.js?v=math-label-fix-20261113'));

assert(app.includes('attempted_on_paper_unreviewed'));

console.log('PASS: two unique graduated video scripts, mathematical solutions, all stage screens, fixed viewport and protected learning data.');
