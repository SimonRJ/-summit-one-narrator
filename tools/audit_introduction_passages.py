"""Compare actual current guide text across lesson IDs and flag repeated mathematical scenarios."""
import argparse
import csv
import json
import math
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

NUMBER=set('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred hundreds thousand thousands million millions first second third fourth fifth sixth seventh eighth ninth tenth eleventh twelfth'.split())
SKIP=set('a an the for in with on of from some using as to it by is there how many what are can they each this that has and be use are after than if find when which do does'.split())
BLOCKS={'basic':(2,4),'medium':(4,6),'challenge':(6,9)}


def tokens(text):
    return re.findall(r"[a-z]+|[0-9]+",text.casefold())


def mask(text):
    output=[]
    for word in tokens(text):
        if word in NUMBER or word.isnumeric():
            if not output or output[-1]!='#':output.append('#')
        else:output.append(word)
    return ' '.join(output)


def features(text):
    terms=mask(text).split()
    return Counter(['w:'+w for w in terms if w not in SKIP and w!='#']+
                   ['b:'+a+' '+b for a,b in zip(terms,terms[1:]) if a not in SKIP or b not in SKIP])


def scenario_key(prompt,working):
    wording=(prompt+' '+working).casefold()
    if ('domino' in prompt.casefold() and re.search(r'\b(vertic\w*|upright)\b',prompt.casefold()) and
        'exactly' in prompt.casefold() and any(word in wording for word in ('horizontal','flat','sideways')) and
        any(key in wording for key in ('how many','different tilings','different arrangements'))):
        return 'fixed number of vertical dominoes in a two-row strip'
    if ('two' in wording and 'notebook' in prompt.casefold() and 'ruler' in prompt.casefold() and 'cost' in wording):
        return 'two receipts for notebooks and rulers'
    if ('three boxes' in prompt.casefold() and ('together' in wording or 'pair' in wording)):
        return 'recover three box contents from their three overlapping pair totals'
    if ('marker' in prompt.casefold() and 'pens' in prompt.casefold() and 'cost' in wording):
        return 'recover pen and marker prices from two purchases'
    return ''


def vector_list(texts):
    data=[features(t) for t in texts];df=Counter(k for x in data for k in x)
    vectors=[]
    for row in data:
        v={k:(1+math.log(n))*math.log(1+len(data)/(1+df[k])) for k,n in row.items()}
        norm=math.sqrt(sum(x*x for x in v.values())) or 1
        vectors.append({k:value/norm for k,value in v.items()})
    return vectors


def cosine(x,y):
    if len(x)>len(y):x,y=y,x
    return sum(v*y.get(k,0) for k,v in x.items())


def git_data(root,ref,path):
    return subprocess.check_output(['git','-C',str(root),'show',ref+':'+path]).decode()


def read_catalogue(repo,catalog,ref):
    live=json.loads((catalog/'data/lesson-intros-live.json').read_text())['entries']
    studies=json.loads(git_data(repo,ref,'data/recorded-studies.json'))['lessons']
    rows={};uncertain=[]
    for entry in live:
        id=entry['id']
        file=(catalog/'data/lesson-intros')/(id+('-Illustrated' if entry.get('detailsEdition')==1 else '')+'.json')
        guide=json.loads(file.read_text())
        matches=guide['sha256']==entry['sha256']
        rows[id]=dict(status=entry['status'],title=guide['title'],source='catalogue',transcript=guide['transcript'],
                      digest=entry['sha256'],same_guide_digest=matches)
        if not matches:uncertain.append(id)
    for id,guide in studies.items():
        rows[id]=dict(status='verified',title=guide['title'],source='recorded study',transcript=guide['transcript'],digest=guide.get('sha256',''),same_guide_digest=True if guide.get('sha256') else None)
    for n in range(1,7):
        id=f'S{n:03d}';script=json.loads(git_data(repo,ref,f'production/scripts/{id}.json'))
        rows[id]=dict(status='verified',title=script['title'],source='bundled local film',transcript=[s['narration'] for s in script['scenes']],digest='',same_guide_digest=None)
    register=list(csv.DictReader(git_data(repo,ref,'docs/lesson-introduction-review-register-20261116.csv').splitlines()))
    return rows,register,uncertain


def catalogue_map(repo,catalog,out,ref):
    films,register,uncertain=read_catalogue(repo,catalog,ref)
    def watch(id):
        n=int(id[1:])
        return 'watch-intro-'+id.lower()+'.html' if n<=6 else 'watch-lesson-intro.html?slot='+str(n)
    # Same-ID historical recuts and checking-only films are never counted as separate active lessons.
    active={id:v for id,v in films.items() if v['status']=='verified'}
    scenes=defaultdict(list)
    for id,v in active.items():
        for i,line in enumerate(v['transcript'],1):scenes[' '.join(tokens(line))].append((id,i))
    standard={id:v for id,v in active.items() if len(v['transcript'])==11 and v['source']=='catalogue'}
    specs=[(id,label) for id in standard for label in BLOCKS]
    sets=[standard[id]['transcript'][slice(*BLOCKS[level])] for id,level in specs]
    prompt=[s[0] for s in sets];purpose=[' '.join(s) for s in sets]
    prompt_features=vector_list(prompt); passage_features=vector_list(purpose)
    scenario=[scenario_key(question,body) for question,body in zip(prompt,purpose)]
    by_id=defaultdict(lambda:defaultdict(list));pairs=[]
    for i,(a,level) in enumerate(specs):
        for j in range(i+1,len(specs)):
            b,other=specs[j]
            if a==b:continue
            ps=cosine(prompt_features[i],prompt_features[j]);bs=cosine(passage_features[i],passage_features[j])
            # The full working and prompt must agree, unless the numerical template of the entire prompt matches.
            identical=mask(prompt[i])==mask(prompt[j])
            structural=scenario[i] if scenario[i] and scenario[i]==scenario[j] else ''
            if not (identical or structural or (ps>=.39 and bs>=.48) or (ps>=.58 and bs>=.36)):continue
            strength='same number-masked prompt' if identical else ('same mathematical scenario: '+structural if structural else 'probable related scenario')
            by_id[a][level].append(f'{b}/{other}');by_id[b][other].append(f'{a}/{level}')
            pairs.append([a,level,watch(a),b,other,watch(b),strength,round(ps,3),round(bs,3),prompt[i],prompt[j]])
    out.mkdir(parents=True,exist_ok=True)
    with (out/'intro-example-near-matches.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['lesson','example','player','other_lesson','other_example','other_player','screen','prompt_similarity','whole_example_similarity','first_prompt','second_prompt']);w.writerows(pairs)
    totals=Counter();candidates=defaultdict(list);rowout=[]
    for entry in register:
        id=entry['id'];film=films.get(id);title=film['title'] if film else entry['title']
        exact=[];duplicate={}
        near=by_id[id]
        if not film:kind='no listed dedicated introduction'
        elif film['status']!='verified':kind='checking in the catalogue'
        elif id not in standard:kind='individual structure; review its own chapters'
        else:
            for i,line in enumerate(film['transcript'][2:9],3):
                found=[f'{j}/{n}' for j,n in scenes[' '.join(tokens(line))] if j!=id]
                if found:duplicate[str(i)]=found
                else:exact.append(i)
            if duplicate:kind='rewrite repeated spoken passages'
            elif near:kind='seven unique passages; compare numerical or scenario variants'
            else:kind='seven unique passages; no near matches detected'
        totals[kind]+=1;candidates[kind].append(id)
        rowout.append([id,title,watch(id) if film else '',film['source'] if film else '',film['status'] if film else '',(film or {}).get('digest',''),
                       ('yes' if film['same_guide_digest'] else 'no') if film and film['same_guide_digest'] is not None else '',len(film['transcript']) if film else '',kind,
                       ' '.join(map(str,exact)),json.dumps(duplicate,separators=(',',':')) if duplicate else '',
                       *[' '.join(sorted(near[k])) for k in BLOCKS]])
    with (out/'intro-passage-coverage.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['lesson','title','player','transcript_source','baseline_availability','movie_sha256','guide_digest_matches_movie','scene_count','editorial_next_step','unique_scene_numbers_3_to_9','exact_matches_to_other_lessons','basic_near_matches','medium_near_matches','challenge_near_matches']);w.writerows(rowout)
    summary={'course_commit':subprocess.check_output(['git','-C',str(repo),'rev-parse',ref],text=True).strip(),
        'catalogue_commit':subprocess.check_output(['git','-C',str(catalog),'rev-parse','HEAD'],text=True).strip(),
        'canonical_course_lessons':len(register),'active_distinct_intro_ids':len(active),'active_legacy_11_scene_films':len(standard),
        'current_guide_digest_differs_from_selected_movie':sorted(id for id in active if active[id]['same_guide_digest'] is False),
        'near_match_pairs_of_examples':len(pairs),'counts':dict(totals),'groups':dict(candidates),
        'interpretation':'3–9 are one-based scene numbers in the legacy eleven-scene format. Exact matches are word-for-word after punctuation and case normalization against every currently playable canonical guide. The near-match screen compares the problem and full worked passage across every legacy example, independent of course focus, after masking numerical values, and also checks explicit scenario signatures including the fixed-vertical two-row domino problem, paired receipt totals and three overlapping box totals. It flags probable variants for editorial inspection. No score asserts mathematical originality. Checking-only, bespoke and absent films are listed separately. Current guide metadata may describe preserved audio without matching the selected illustrated movie digest. Verify the actual selected recording before reusing any passage. Duplicates can still occur against bespoke or unpublished examples outside the legacy near-match screen.'}
    (out/'intro-passage-coverage-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ('canonical_course_lessons','active_distinct_intro_ids','active_legacy_11_scene_films','near_match_pairs_of_examples','counts','current_guide_digest_differs_from_selected_movie')},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('course',type=Path);p.add_argument('catalogue',type=Path);p.add_argument('out',type=Path);p.add_argument('--course-ref',default='HEAD');args=p.parse_args()
    catalogue_map(args.course,args.catalogue,args.out,args.course_ref)
