const search = document.getElementById('filmSearch');
const kind = document.getElementById('filmKind');
const result = document.getElementById('filmMatches');
const sections = [...document.querySelectorAll('.chapters > section')];
const fold = value => value.normalize('NFKD').toLowerCase().replace(/[\u0300-\u036f]/g,'');

function filterFilms(){
  const terms = fold(search.value.trim()).split(/\s+/).filter(Boolean);
  let count = 0;
  for(const section of sections){
    const chapter = section.querySelector('h2').textContent;
    let visible = 0;
    for(const film of section.querySelectorAll('li')){
      const label = film.querySelector('small').textContent;
      const text = fold(chapter+' '+film.textContent);
      const matches = (!kind.value || label.endsWith(kind.value)) && terms.every(t => text.includes(t));
      film.hidden = !matches;
      if(matches)visible++;
    }
    section.hidden = visible===0;
    count+=visible;
  }
  result.textContent = count===0 ? 'No films match. Try a topic name or clear the filters.' :
    count+' '+(count===1?'film':'films');
}
search.addEventListener('input',filterFilms);
kind.addEventListener('change',filterFilms);
document.getElementById('filmFilters').addEventListener('reset',()=>queueMicrotask(filterFilms));
document.getElementById('filmFilters').hidden=false;
filterFilms();
