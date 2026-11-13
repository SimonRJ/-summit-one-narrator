/* Summit One mathematics typesetting.
 * Dynamic lesson, investigation and exam text stays authoritative; only its
 * visible arithmetic expressions become semantic TeX through KaTeX.
 * Inputs, saved answers, question text and DOM event handlers are untouched.
 */
const MATH_AREAS = [
  ".math-copy",".problem-prompt",".stem",".choice-content",
  ".flash-question",".flash-options",".flash-feedback",".flash-summary",
  ".mini-check",".worked-example",".method-card",".reasoning-steps",
  ".bridge-example",".session-intro",".lesson-recall-brief",
  ".lesson-fade-unit",".lesson-prep-unit",
  ".lesson-mix-unit",".lesson-extra-unit",".lesson-problem-unit",
  ".solution-panel",".question-review",".exam-visual",".exam-section-key",
  ".np-transcript",".transcript",".problem-card","[data-math-tex]"
].join(",");
const SKIP_SELECTOR = [
  "script","style","noscript","textarea","input","select","option",
  "svg","math","code","pre","samp","kbd",
  ".math-inline",".katex",".math-display","[contenteditable]",
  "[data-math-skip]"
].join(",");
const ATOM = "(?:(?:LCM|GCD|HCF|lcm|gcd|C)\\([^)]{1,24}\\)|\\d+(?:\\.\\d+)?[A-Za-z]?(?:\\([^)]{1,35}\\))?|[A-Za-zπθφ]{1,5}(?:\\([^)]{1,35}\\))?|\\([^)]{1,45}\\)|…)(?:\\^\\{?[\\w]+\\}?|[⁰¹²³⁴⁵⁶⁷⁸⁹]|!)?";
// A spaced slash often means progress ("6 / 6"), not a fraction.
// Times such as 10:30 are handled by an explicit contextual guard below.
const OPERATOR = "(?:\\s*(?:[+=×÷−<>≤≥≠≈·])\\s*|/|:|\\s+-\\s+)";
const EXPRESSION = new RegExp(
  ATOM + "(?:" + OPERATOR + ATOM + ")+|(?:\\d+|[A-Za-zπθφ]{1,3})(?:\\^\\{?[\\w]+\\}?|[⁰¹²³⁴⁵⁶⁷⁸⁹])+|\\d+!",
  "gu"
);
const DELIMITERS = /\\\[([\s\S]*?)\\\]|\\\(([\s\S]*?)\\\)|\$\$([\s\S]*?)\$\$/g;
const SUPERSCRIPTS = {"⁰":"0","¹":"1","²":"2","³":"3","⁴":"4","⁵":"5","⁶":"6","⁷":"7","⁸":"8","⁹":"9"};
const RENDER_OPTIONS = {throwOnError:true,strict:"ignore",trust:false,output:"htmlAndMathml"};

export function plainToTeX(expression){
  // Render a copy only: never rewrite the original prompt or submitted response.
  return String(expression)
    .replace(/([⁰¹²³⁴⁵⁶⁷⁸⁹]+)/g, (_,power)=>"^{"+[...power].map(n=>SUPERSCRIPTS[n]).join("")+"}")
    .replace(/(?:LCM|lcm)(?=\()/g, "\\operatorname{lcm}")
    .replace(/(?:GCD|gcd|HCF)(?=\()/g, "\\operatorname{gcd}")
    .replace(/\bC(?=\()/g, "\\mathrm{C}")
    .replace(/(\d+)\/(\d+)(?![\d/])/g,(_,n,d)=>"\\frac{"+n+"}{"+d+"}")
    .replace(/\b([a-z])\/([a-z])\b/g,(_,n,d)=>"\\frac{"+n+"}{"+d+"}")
    .replace(/×/g,"\\times ").replace(/÷/g,"\\div ")
    .replace(/·/g,"\\cdot ").replace(/−/g,"-")
    .replace(/≤/g,"\\leq ").replace(/≥/g,"\\geq ")
    .replace(/∑/g,"\\sum ").replace(/∞/g,"\\infty ")
    .replace(/±/g,"\\pm ").replace(/∈/g,"\\in ")
    .replace(/≠/g,"\\ne ").replace(/≈/g,"\\approx ")
    .replace(/…/g,"\\cdots ").replace(/π/g,"\\pi ")
    .replace(/θ/g,"\\theta ").replace(/φ/g,"\\varphi ");
}
function renderMath(span,tex,display=false){
  span.dataset.tex=tex;
  span.className=display?"math-inline math-display":"math-inline";
  try{
    if(typeof window.katex?.render!=="function")throw new Error("Typesetter not loaded");
    window.katex.render(tex,span,{...RENDER_OPTIONS,displayMode:display});
  }catch{
    span.classList.add("math-fallback");
    return false;
  }
  return true;
}
function createMath(tex,original,display=false){
  const span=document.createElement("span");
  span.setAttribute("aria-label",original);
  span.dataset.mathSource=original;
  span.textContent=original;
  renderMath(span,tex,display);
  return span;
}
function appendPlainMath(fragment,text){
  EXPRESSION.lastIndex=0;
  let i=0,match,changed=false;
  while((match=EXPRESSION.exec(text))){
    const formula=match[0];
    // Ratios are usually unspaced. Do not convert clock times or progress counters.
    if(/^\d{1,2}:\d{2}$/.test(formula))continue;
    if(/^\d+\s*\/\s*\d+$/.test(formula)&&/\s\/\s/.test(formula))continue;
    if(/^\d{4}[-/]\d{1,2}[-/]\d{1,2}$/.test(formula))continue;
    if(match.index>i)fragment.append(document.createTextNode(text.slice(i,match.index)));
    fragment.append(createMath(plainToTeX(formula),formula));
    i=match.index+formula.length;
    changed=true;
  }
  if(i<text.length)fragment.append(document.createTextNode(text.slice(i)));
  return changed;
}
function replaceText(node){
  const original=node.nodeValue;
  if(!original||original.length<3||original.length>50000)return;
  if(!/[=+×÷−/<>≤≥≠≈·:²³⁴⁵⁶⁷⁸⁹⁰^!]|\\[\[(]|\$\$/.test(original))return;
  const parent=node.parentElement;
  if(!parent||parent.closest(SKIP_SELECTOR))return;
  let last=0,matched=false;
  const fragment=document.createDocumentFragment();
  DELIMITERS.lastIndex=0;
  let delim;
  while((delim=DELIMITERS.exec(original))){
    const before=original.slice(last,delim.index);
    if(before)matched=appendPlainMath(fragment,before)||matched;
    const tex=delim[1]??delim[2]??delim[3];
    fragment.append(createMath(tex,delim[0],delim[1]!==undefined||delim[3]!==undefined));
    last=DELIMITERS.lastIndex;
    matched=true;
  }
  if(last<original.length)matched=appendPlainMath(fragment,original.slice(last))||matched;
  if(matched)node.replaceWith(fragment);
}
export function typesetMath(root=document){
  if(!root?.querySelectorAll||typeof document==="undefined")return;
  // Intentional notation takes precedence over the conservative prose recogniser.
  for(const explicit of root.querySelectorAll("[data-math-tex]")){
    if(explicit.dataset.mathRendered==="yes")continue;
    const tex=explicit.dataset.mathTex;
    const original=explicit.textContent||tex;
    explicit.dataset.mathRendered="yes";
    explicit.setAttribute("aria-label",original);
    explicit.textContent=original;
    renderMath(explicit,tex,explicit.hasAttribute("data-math-display"));
  }
  const found=root.querySelectorAll(MATH_AREAS);
  const done=new Set();
  for(const area of found){
    if(area.closest(SKIP_SELECTOR))continue;
    const walker=document.createTreeWalker(area,NodeFilter.SHOW_TEXT);
    const texts=[];
    while(walker.nextNode()){
      const t=walker.currentNode;
      if(!done.has(t)&&!t.parentElement?.closest(SKIP_SELECTOR)){
        done.add(t);texts.push(t);
      }
    }
    for(const t of texts)replaceText(t);
  }
}
if(typeof window!=="undefined"&&typeof document!=="undefined"){
  const go=()=>{
    let scheduled=false,observer;
    const refresh=()=>{
      scheduled=false;
      observer.disconnect();
      try{
        if(typeof window.katex?.render==="function"){
          for(const node of document.querySelectorAll(".math-inline.math-fallback[data-tex]")){
            renderMath(node,node.dataset.tex,node.classList.contains("math-display"));
          }
        }
        typesetMath(document);
      }finally{observer.observe(document.body,{subtree:true,childList:true,characterData:true});}
    };
    const schedule=()=>{if(!scheduled){scheduled=true;requestAnimationFrame(refresh);}};
    observer=new MutationObserver(schedule);
    observer.observe(document.body,{subtree:true,childList:true,characterData:true});
    schedule();
    window.addEventListener("load",schedule,{once:true});
    window.addEventListener("summit:math-ready",schedule);
  };
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",go,{once:true});
  else go();
}
