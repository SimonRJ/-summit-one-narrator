import json, os, re, sys, math, textwrap, subprocess, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H=1280,720
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(p,s): return ImageFont.truetype(p,s)
def colour(key):
    k=str(key).lower()
    if any(x in k for x in ["geometry","area","angle","t12","t13"]): return (92,207,250)
    if any(x in k for x in ["digit","factor","remainder","t03","t04","t11"]): return (255,209,102)
    if any(x in k for x in ["count","probability","route","symmetry","t05","t06","t08","t14","t15"]): return (124,224,163)
    if any(x in k for x in ["ratio","fraction","algebra","rate","t09","t16"]): return (255,122,168)
    return (112,220,255)
def split_text(text, max_words=48):
    text=re.sub(r"\s+"," ",str(text)).strip()
    if not text:return []
    sentences=re.split(r"(?<=[.!?])\s+",text)
    out=[];cur=[]
    for s in sentences:
        words=s.split()
        while len(words)>max_words:
            if cur:out.append(" ".join(cur));cur=[]
            out.append(" ".join(words[:max_words]));words=words[max_words:]
        if len(cur)+len(words)>max_words:
            if cur:out.append(" ".join(cur))
            cur=words
        else:cur+=words
    if cur:out.append(" ".join(cur))
    return out
def wrap(draw,text,f,maxw):
    words=text.split();lines=[];cur=""
    for w in words:
        test=(cur+" "+w).strip()
        if draw.textbbox((0,0),test,font=f)[2]<=maxw:cur=test
        else:
            if cur:lines.append(cur)
            cur=w
    if cur:lines.append(cur)
    return lines
def visual(draw,key,accent):
    k=str(key).lower();a=accent
    if any(x in k for x in ["area","geometry","angle","t12","t13"]):
        draw.rounded_rectangle((90,85,430,425),20,outline=a,width=6)
        draw.line((90,425,430,85),fill=(255,209,102),width=6)
        draw.line((90,255,430,310),fill=a,width=5)
        draw.ellipse((245,230,263,248),fill=(124,224,163))
    elif any(x in k for x in ["count","probability","route","symmetry","t05","t06","t08","t14","t15"]):
        pts=[(110,130),(250,225),(110,330),(410,130),(410,225),(410,330)]
        for p in pts:draw.ellipse((p[0]-10,p[1]-10,p[0]+10,p[1]+10),fill=a)
        for p in pts[:3]:
            for q in pts[3:]:draw.line((*p,*q),fill=(*a,130),width=3)
    else:
        for i,w in enumerate([360,280,200]):
            y=130+i*95;draw.rounded_rectangle((90,y,90+w,y+54),18,outline=a,width=5)
def make_slide(item,text,idx,total,out):
    accent=colour(item.get("category",""))
    base=Image.new("RGB",(W,H),(5,10,18));px=base.load()
    # soft vertical gradient
    for y in range(H):
        t=y/H;col=(int(7+6*(1-t)),int(17+18*(1-t)),int(29+27*(1-t)))
        for x in range(W):px[x,y]=col
    # glow
    glow=Image.new("RGBA",(W,H),(0,0,0,0));gd=ImageDraw.Draw(glow)
    gd.ellipse((W-520,-260,W+180,440),fill=(*accent,42))
    glow=glow.filter(ImageFilter.GaussianBlur(70));base=Image.alpha_composite(base.convert("RGBA"),glow)
    d=ImageDraw.Draw(base)
    # deterministic stars
    h=int(hashlib.sha256(item["id"].encode()).hexdigest()[:8],16)
    for i in range(45):
        x=(h*(i+17)*37)%W;y=(h*(i+23)*53)%H;r=1+(i%3==0)
        d.ellipse((x,y,x+r,y+r),fill=(255,255,255,45))
    visual(d,item.get("category",""),accent)
    d.rounded_rectangle((515,82,1190,575),28,fill=(7,18,31,218),outline=(40,67,90,220),width=2)
    d.text((555,112),item["id"],font=font(BOLD,24),fill=accent)
    title=item.get("title","Mathematical reasoning")
    titlef=font(BOLD,38);titlelines=wrap(d,title,titlef,590)[:2]
    ty=155
    for line in titlelines:d.text((555,ty),line,font=titlef,fill=(244,248,255));ty+=46
    bodyf=font(FONT,29);lines=wrap(d,text,bodyf,585)
    if len(lines)>8:
        bodyf=font(FONT,25);lines=wrap(d,text,bodyf,585)
    y=ty+24
    for line in lines[:10]:
        d.text((555,y),line,font=bodyf,fill=(218,232,244));y+=int(bodyf.size*1.48)
    d.text((555,535),f"Step {idx+1} of {total}",font=font(BOLD,19),fill=(145,167,192))
    d.rounded_rectangle((90,650,1190,662),6,fill=(20,42,60))
    prog=1100*(idx+1)/total;d.rounded_rectangle((90,650,90+prog,662),6,fill=accent)
    base.convert("RGB").save(out,quality=95)
def probe(audio):
    p=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",audio],capture_output=True,text=True,check=True)
    return float(p.stdout.strip())
def main():
    manifest=json.load(open(sys.argv[1]));ids=set(sys.argv[2:])
    outdir=Path("render/out");outdir.mkdir(parents=True,exist_ok=True)
    for item in manifest["items"]:
        if ids and item["id"] not in ids:continue
        audio=Path("render/audio")/f'{item["id"]}_narration.wav'
        if not audio.exists():
            print("MISSING AUDIO",item["id"]);continue
        pieces=[]
        for s in item.get("segments",[]):pieces+=split_text(s)
        if not pieces:pieces=[item.get("title","Explanation")]
        duration=probe(str(audio));weights=[max(1,len(x.split())) for x in pieces];totalw=sum(weights)
        work=Path("render/work")/item["id"];work.mkdir(parents=True,exist_ok=True)
        concat=[]
        for i,(piece,w) in enumerate(zip(pieces,weights)):
            img=work/f"slide-{i:03d}.png";make_slide(item,piece,i,len(pieces),str(img))
            sec=max(.7,duration*w/totalw);concat+= [f"file '{img.resolve()}'",f"duration {sec:.4f}"]
        concat.append(f"file '{(work/f'slide-{len(pieces)-1:03d}.png').resolve()}'")
        lst=work/"slides.txt";lst.write_text("\n".join(concat)+"\n")
        target=outdir/f'{item["id"]}_final.mp4'
        subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(lst),"-i",str(audio),"-r","30","-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",str(target)],check=True)
        print("RENDERED",item["id"],round(target.stat().st_size/1048576,2),"MB")
if __name__=="__main__":main()
