import fs from "node:fs";
import path from "node:path";
const fail=m=>{console.error("FAIL:",m);process.exitCode=1},ok=m=>console.log("PASS:",m);
const read=p=>JSON.parse(fs.readFileSync(p,"utf8"));
const sessions=read("data/sessions-372.json"),teaching=read("data/teaching-72.json");
const banks=["data/challenges-original-42.json","data/challenges-amc-001-040.json","data/challenges-amc-041-080.json","data/challenges-amc-081-120.json","data/challenges-amc-121-152.json"].map(read);
const awards=read("data/amc-awards.json"),exams=read("data/exams/index.json");
if(sessions.sessions.length===372)ok("372 canonical sessions");else fail("session count");
if(sessions.sessions.every((x,i)=>x.slot===i+1))ok("session ordinals consecutive");else fail("session ordinal gap");
const mawa=sessions.sessions.filter(x=>x.type==="MAWA").map(x=>x.slot);
const expected=Array.from({length:Math.floor(372/7)},(_,i)=>(i+1)*7);
if(JSON.stringify(mawa)===JSON.stringify(expected))ok("MAWA exactly every seventh session");else fail("MAWA cadence");
if(sessions.sessions.filter(x=>x.type==="AMC MOCK").length===25)ok("25 AMC mocks");else fail("AMC mock count");
if(sessions.sessions.filter(x=>x.type==="ROSSMOYNE MOCK").length===11)ok("11 Rossmoyne mocks");else fail("Rossmoyne mock count");
if(teaching.items.length===72&&new Set(teaching.items.map(x=>x.id)).size===72)ok("72 unique teaching records");else fail("teaching records");
const challenges=banks.flatMap(b=>b.items);
if(challenges.length===194&&new Set(challenges.map(x=>x.id)).size===194)ok("194 unique challenge records");else fail(`challenge records ${challenges.length}`);
if(challenges.every(x=>x.prompt&&x.answer!==undefined&&x.answer!==null))ok("all challenges have prompt/answer");else fail("challenge prompt/answer missing");
const marks=[...Array(10).fill(3),...Array(10).fill(4),...Array(5).fill(5),6,7,8,9,10];
if(marks.reduce((a,b)=>a+b,0)===135)ok("AMC scoring totals 135");else fail("AMC marks");
if(Array.isArray(exams.papers))ok("official paper import index ready");else fail("exam index");
if(awards.practice_estimate_wa?.year5?.perfect===135&&awards.practice_estimate_wa?.year6?.perfect===135)ok("award config max 135");else fail("award config");
const html=fs.readdirSync(".").filter(x=>x.endsWith(".html"));
for(const file of html){
 const t=fs.readFileSync(file,"utf8"),re=/(?:src|href)="([^"#?]+)(?:[?#][^"]*)?"/g;let m;
 while((m=re.exec(t))){const u=m[1];if(/^https?:|^mailto:|^tel:/.test(u))continue;const p=u.replace(/^\.\//,"");if(p.endsWith("/"))continue;if(!fs.existsSync(p))fail(`${file} missing local link ${p}`)}
}
ok("HTML local-link scan complete");
for(const file of fs.readdirSync(".").filter(x=>x.endsWith(".js"))){
 const t=fs.readFileSync(file,"utf8");if(/sb_secret_|SUPABASE_SERVICE_ROLE_KEY\s*=/.test(t))fail(`secret-looking key in ${file}`);
}
ok("no server secret keys in browser JavaScript");
if(process.exitCode)process.exit(process.exitCode);else console.log("ALL RELEASE GATES PASSED");
