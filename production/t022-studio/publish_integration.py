"""Apply the narrowly scoped app changes only after the new movie is verified."""
import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[2]
def update(path,func):
 p=root/path;p.write_text(func(p.read_text()))
def route(s):
 # Preserve attempt gating and all unrelated lesson routes.
 line='  if(id==="T02.2")return "media/T02.2.mp4?v=studio-v1";'
 if re.search(r'if\(id===\"T02\.2\"\)',s):s=re.sub(r'  if\(id===\"T02\.2\"\).*?;',line,s)
 else:
  mark='  if(id==="T02.1")';assert mark in s
  at=s.index('\n',s.index(mark));s=s[:at]+'\n'+line+s[at:]
 s=s.replace('media/T02.1.mp4?v=3d-speechlocked-v3','media/T02.1.mp4?v=studio-v4')
 return s
update('app-main.js',route)
update('index.html',lambda s:re.sub(r'app-main\.js\?v=[^"\s]+','app-main.js?v=studio-t022-v1',s))
def sw(s):
 s=re.sub(r'const CACHE="[^"]+"','const CACHE="summit-one-studio-t022-v1"',s)
 return re.sub(r'app-main\.js\?v=[^"\s]+','app-main.js?v=studio-t022-v1',s)
update('sw.js',sw)
script=json.loads((Path(__file__).parent/'narration.json').read_text());p=root/'data/teaching-72.json';data=json.loads(p.read_text())
item=next(x for x in data['items'] if x['id']=='T02.2')
item['title']=script['title'];item['transcript']=' '.join(script['segments']);item['audio_url']='media/T02.2-narration.m4a';p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
update('watch-t02-1.html',lambda s:s if 'watch-t02-2.html' in s else s.replace('</main>','<p><a href="watch-t02-2.html?v=studio-v1">Next lesson: work backwards →</a></p></main>'))
print('Updated T02.2 lesson route, transcript, navigation and app cache version.')
