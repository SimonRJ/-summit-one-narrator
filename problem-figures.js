function svgWrap(inner,label){
  return `<figure class="problem-figure"><svg viewBox="0 0 420 280" role="img" aria-label="${label}">${inner}</svg><figcaption>${label}</figcaption></figure>`;
}
function polygonPoints(cx,cy,r,n=6,rot=Math.PI/6){return Array.from({length:n},(_,i)=>{const a=rot+i*2*Math.PI/n;return [cx+r*Math.cos(a),cy+r*Math.sin(a)]}).map(p=>p.join(",")).join(" ")}
function sevenSegDigit(x,y,d,scale=1){
  const seg={0:"abcedf",1:"bc",2:"abdeg",3:"abcdg",4:"bcfg",5:"acdfg",6:"acdefg",7:"abc",8:"abcdefg",9:"abcdfg"}; // normalized below
  const map={0:"abcdef",1:"bc",2:"abdeg",3:"abcdg",4:"bcfg",5:"acdfg",6:"acdefg",7:"abc",8:"abcdefg",9:"abcdfg"};
  const on=new Set(map[d].split(""));
  const line=(id,x1,y1,x2,y2)=>`<line class="${on.has(id)?"seg-on":"seg-off"}" x1="${x+x1*scale}" y1="${y+y1*scale}" x2="${x+x2*scale}" y2="${y+y2*scale}"/>`;
  return line("a",10,0,40,0)+line("b",45,5,45,35)+line("c",45,45,45,75)+line("d",10,80,40,80)+line("e",5,45,5,75)+line("f",5,5,5,35)+line("g",10,40,40,40);
}
function spiralCells(size){
  const c=(size-1)/2,cells=[[c,c]],dirs=[[0,-1],[1,0],[0,1],[-1,0]];let len=2,di=0,x=c,y=c;
  while(true){
    for(let rep=0;rep<2;rep++){
      const [dx,dy]=dirs[di%4];
      for(let k=0;k<len;k++){x+=dx;y+=dy;if(x<0||y<0||x>=size||y>=size)return cells;cells.push([x,y])}
      di++;
    }
    len+=2;
  }
}
function quiltGold(size){
  const c=(size-1)/2;let x=c,y=c;const cells=[[x,y]],dirs=[[1,0],[0,-1],[-1,0],[0,1]];let di=0;
  for(let len=2;len<=size-3;len+=2){
    for(let rep=0;rep<2;rep++){const [dx,dy]=dirs[di%4];for(let k=0;k<len;k++){x+=dx;y+=dy;cells.push([x,y])}di++}
  }
  const [dx,dy]=dirs[di%4];for(let k=0;k<size-2;k++){x+=dx;y+=dy;if(x>=0&&y>=0&&x<size&&y<size)cells.push([x,y])}
  return cells;
}
function gridSvg(size,cells,colors={on:"#f4c96b",off:"#153049"}){
  const pad=35,cell=200/size, set=new Set(cells.map(([x,y])=>x+","+y));let s="";
  for(let y=0;y<size;y++)for(let x=0;x<size;x++)s+=`<rect x="${pad+x*cell}" y="${pad+y*cell}" width="${cell}" height="${cell}" fill="${set.has(x+","+y)?colors.on:colors.off}" stroke="#6a8ba4" stroke-width=".7"/>`;
  return s;
}
export function problemFigure(id){
  if(id==="A013"){
    const pts=[[55,140],[120,85],[120,195],[205,85],[205,195],[290,140]],edges=[[0,1],[0,2],[1,2],[1,3],[2,3],[2,4],[3,4],[3,5],[4,5]];
    return svgWrap(`<g class="pf-lines">${edges.map(([a,b])=>`<line x1="${pts[a][0]}" y1="${pts[a][1]}" x2="${pts[b][0]}" y2="${pts[b][1]}"/>`).join("")}</g>${pts.map(([x,y],i)=>`<circle cx="${x}" cy="${y}" r="29" class="pf-node"/><text x="${x}" y="${y+7}" class="pf-text">${i+1}</text>`).join("")}<text x="210" y="252" class="pf-note">A line means the two polygons touch.</text>`,"Touching relation for polygons 1 to 6");
  }
  if(id==="A047"){
    const lines=`<rect x="85" y="30" width="240" height="240" class="pf-outline"/><line x1="205" y1="30" x2="325" y2="270"/><line x1="85" y1="150" x2="325" y2="30"/><line x1="325" y1="150" x2="85" y2="270"/><line x1="205" y1="270" x2="85" y2="30"/>`;
    const shades=`<polygon points="205,30 325,30 229,78" class="pf-shade"/><polygon points="325,150 325,270 277,174" class="pf-shade"/><polygon points="205,270 85,270 181,222" class="pf-shade"/><polygon points="85,150 85,30 133,126" class="pf-shade"/>`;
    return svgWrap(shades+lines+`<text x="205" y="20" class="pf-note">30 cm</text>`,"30 cm square with each side midpoint joined to the indicated opposite corner; four congruent shaded triangles");
  }
  if(id==="A070"){
    const cells=spiralCells(9);return svgWrap(gridSvg(9,cells,{on:"#e8edf4",off:"#101820"})+`<circle cx="146" cy="146" r="4" fill="#f4c96b"/><text x="310" y="75" class="pf-note">9×9 model of the same black spiral rule</text>`,"Small model of the black spiral beginning at the centre and turning with run lengths 2, 2, 4, 4, 6, 6 and so on");
  }
  if(id==="A122"){
    let s="";for(let d=0;d<=9;d++){const col=d%5,row=Math.floor(d/5),x=35+col*75,y=35+row*115;s+=sevenSegDigit(x,y,d,.85)+`<text x="${x+22}" y="${y+90}" class="pf-note">${d}</text>`}
    return svgWrap(s,"Standard seven-segment digit display for 0 through 9");
  }
  if(id==="A128"){
    const rows=[[["1",120],["2",200],["3",280]],[["4",80],["5",160],["6",240],["7",320]],[["8",120],["9",200],["0",280]]],ys=[65,140,215];let s="";
    rows.forEach((row,ri)=>row.forEach(([d,x])=>{s+=`<polygon points="${polygonPoints(Number(x),ys[ri],37)}" class="pf-node"/><text x="${x}" y="${ys[ri]+8}" class="pf-text">${d}</text>`}));
    return svgWrap(s,"Hexagonal keypad: 1 2 3 on the top row, 4 5 6 7 in the middle, and 8 9 0 on the bottom; touching hexagons are neighbours");
  }
  if(id==="A149"){
    const cells=quiltGold(7);return svgWrap(gridSvg(7,cells,{on:"#d9aa40",off:"#36a56e"})+`<text x="292" y="75" class="pf-note">7×7 model</text><text x="292" y="98" class="pf-note">gold path shown in gold</text>`,"7 by 7 model of the two one-square-wide spiral paths; the same run-length pattern continues to 45 by 45");
  }
  return "";
}
