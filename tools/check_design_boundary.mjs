import assert from "node:assert/strict";
import fs from "node:fs";
import {createHash} from "node:crypto";

const css=fs.readFileSync("summit-polish.css","utf8");
const clean=css.replace(/\/\*[\s\S]*?\*\//g,"");
const validStart=[
  "body:not(.exam-mode)",
  "body.home-focus:not(.exam-mode)",
  "body.rossmoyne-theme:not(.exam-mode)"
];
function splitSelectors(s){
  let depth=0,start=0,out=[];
  for(let i=0;i<s.length;i++){
    if(s[i]==="(")depth++;
    else if(s[i]===")")depth--;
    else if(s[i]===","&&depth===0){out.push(s.slice(start,i).trim());start=i+1;}
  }
  out.push(s.slice(start).trim());
  return out.filter(Boolean);
}
// Check every CSS rule, including selectors nested inside media queries.
// Every selector must exclude the authentic examination workspace.
let open=0,first=0;
for(let i=0;i<clean.length;i++){
  const ch=clean[i];
  if(ch==="{"){
    const selector=clean.slice(first,i).trim();
    if(selector.startsWith("@")){
      assert.match(selector,/^@media\b/,"Only media wrappers are permitted");
    }else{
      for(const part of splitSelectors(selector)){
        assert(validStart.some(prefix=>part.startsWith(prefix)),
          "Unscoped design selector would affect AMC exam mode: "+part);
      }
    }
    open++;first=i+1;
  }else if(ch==="}"){
    assert(open>0,"Unmatched CSS close");
    open--;first=i+1;
  }
}
assert.equal(open,0,"CSS braces must balance");
for(const html of ["index.html","tests.html","welcome.html","login.html",
  "offline-reader.html","lesson-introduction-videos.html","teaching-videos.html","coverage.html"]){
  assert(fs.readFileSync(html,"utf8").includes("summit-polish.css?v=craft-20261121"),html+" is missing the theme");
}
assert(fs.readFileSync("sw.js","utf8").includes("./summit-polish.css?v=craft-20261121"),
  "Offline asset manifest is missing the design system");
assert(fs.readFileSync("app-main.js","utf8").includes("focus-course-progress"),
  "Learning home does not expose course progress");
assert(fs.readFileSync("tests.js","utf8").includes('classList.add("exam-mode")'),
  "The examination class boundary is missing");
// The official-style question-taking stylesheet must remain byte-for-byte frozen.
const bytes=fs.readFileSync("exam.css");
const blobHash=createHash("sha1")
  .update(Buffer.from("blob "+bytes.length+"\0"))
  .update(bytes)
  .digest("hex");
assert.equal(blobHash,"17953e7757a605a334ea1c46c13ed7bb9ebb0338",
  "Exam centre appearance has changed: restore the preserved original stylesheet");
console.log("Design-system scope, assets, home UI and authentic exam freeze verified.");

for(const page of fs.readdirSync('.').filter(name=>name.startsWith('watch-') && name.endsWith('.html'))){
  assert(fs.readFileSync(page,'utf8').includes('href="public-study-theme.css"'),page+' is missing the shared study theme');
}
