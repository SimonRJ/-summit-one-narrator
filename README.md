# Summit One

Summit One is a mathematics training web app for one gifted upper-primary learner working well above year level. It follows a single guided path of 372 sessions aimed at the Australian Mathematics Competition (AMC) Upper Primary paper, the Rossmoyne Senior High School specialist mathematics entrance test, and MAWA-style problem-solving investigations.

**Live site:** https://simonrj.github.io/-summit-one-narrator/

Summit One is an independent family project. It is not affiliated with or endorsed by the Australian Maths Trust, Rossmoyne Senior High School or MAWA. Lesson problems, mock papers and investigations labelled "original" were written for Summit One. Genuine AMC past papers are kept in a separate, frozen examination centre (see [docs/AUTHENTIC_AMC_FREEZE.md](docs/AUTHENTIC_AMC_FREEZE.md)).

## What the app does

| Area | What the learner gets | Status |
|---|---|---|
| Lessons | 283 teaching sessions on 52 techniques: Remember, Discover, Try, Transfer, Check. Two protected original problems per lesson (566 in total). | Deployed |
| Investigations | 53 visits to 20 MAWA-style investigation themes. | Deployed |
| Original AMC practice | Part A (questions 1–20, speed and accuracy) and Part B (questions 21–30, deeper problems). | Partially complete: 4 active split papers, 60 questions |
| Rossmoyne practice | Original Rossmoyne-style papers over 23 problem families. | Partially complete: 9 active papers, 207 questions |
| Authentic AMC centre | 19 genuine Upper Primary papers, 2007–2025, one attempt each. | Deployed and frozen |
| Teaching videos | 72 concept and worked-example videos planned. | 2 finished; 70 have scripts only |
| Optional advanced maths | "Where this maths can lead" pages for the 52 techniques; not assessed. | Deployed |

Exact, dated numbers are in [docs/CURRENT_STATUS.md](docs/CURRENT_STATUS.md). That file, not this table, is the source of truth.

## How it is built

- **Front end:** plain HTML, CSS and JavaScript modules served by GitHub Pages from the `main` branch. No build step. Entry points are `index.html` (course), `login.html`, `welcome.html`, `coverage.html` and `tests.html`.
- **Typography:** Source Sans 3 for interface text, Source Serif 4 for selected headings, KaTeX for mathematics. These are settled; do not change them.
- **Back end:** one Supabase project (Postgres, Auth, Storage, Edge Functions). The browser holds only the publishable key in `supabase-client.js`.
- **Protected content:** answers and worked solutions live only in the database. They are never in this repository or in any file served by Pages. Three Edge Functions mediate access: `submit-problem-attempt` (grades an answer and records the attempt), `get-problem-solution` (returns a solution only after a recorded attempt) and `grade-exam`.
- **Offline shell:** `sw.js` caches static assets under a versioned cache name. Bump the cache name and the `?v=` query strings when shipping front-end changes.
- **Media:** finished public videos sit in `media/`; protected solution videos belong in private Supabase Storage.

```
Browser (GitHub Pages, static JS)
   |  publishable key + learner session
   v
Supabase Auth ── Postgres (RLS) ── Edge Functions (service role, server-side only)
                    |                     |
        progress, attempts,        grading, solution release,
        exam sittings              exam grading
```

More detail: [docs/PLATFORM_ARCHITECTURE.md](docs/PLATFORM_ARCHITECTURE.md).

## Where content lives

| Content | Source of truth | Reaches the learner via |
|---|---|---|
| Course map, techniques, investigations | `data/*.json` (public, answer-free) | fetched by `app-main.js` |
| 566 lesson problems | `tools/content/build_original_lessons.py` with `curated_revisits.py`, `curated_batch2.py` and `curated_spatial.py` | rows in `content_problems`, released through Edge Functions |
| Original mock papers | `tools/papers/*.py` | rows in `exam_catalog` and `exam_questions` |
| Authentic AMC papers | database only; frozen | exam centre |
| Teaching-video scripts | `production/scripts/src/*.txt` | built to `production/scripts/*.json`; not yet recorded |

The generator and the database must agree. Changing one without the other lets a later rebuild silently restore old content.

## Local development

```bash
git clone https://github.com/SimonRJ/-summit-one-narrator
cd -summit-one-narrator
python -m http.server 8765        # then open http://localhost:8765/
```

Requirements: Python 3.12, Node 22 or later. Browser tests additionally need `pip install playwright==1.58.0` and Google Chrome.

Server-side configuration (set in Supabase and GitHub secrets, never committed): `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`.

## Tests

```bash
node tools/check_learning.mjs                     # course mapping, original-only lesson selection
node tools/check_fixed_lesson.mjs                 # lesson screens and protected data
node tools/check_split_training.mjs               # AMC Part A / Part B structure
python tools/content/check_original_lessons.py    # recomputes every generator family
python tools/content/check_curated_batch2.py      # recomputes 60 reauthored problems one by one
python tools/content/check_curated_spatial.py      # enumerates 30 spatial answers and checks the diagram manifest
python tools/content/audit_all_lessons.py         # structure, wording and repetition audit of all 566
python tools/papers/build_all.py /tmp/summit-papers && python tools/papers/audit_generated_papers.py /tmp/summit-papers
python tools/video/build_scripts.py --check       # validates the 70 video scripts
```

What each test does and does not prove is set out in [docs/CURRENT_STATUS.md](docs/CURRENT_STATUS.md#what-the-tests-prove). Passing structural checks is not the same as every problem having been individually solved and read.

## Deployment

Merging to `main` publishes the site through GitHub Pages. GitHub Actions run `Teaching behavior checks` and `Release QA` on pull requests to `main`. Database content is updated separately, with guarded SQL (see the audit register for the procedure used). Verify a release by loading the live site and by running `tools/check_amc_freeze.sql` to confirm the authentic AMC fingerprint is unchanged.

## Rules for contributors

1. Never modify the authentic AMC subsystem: its questions, images, answer keys, timers, interface or stored sittings.
2. Never commit answers, solutions or secrets to this repository.
3. Never change a problem that a learner has already attempted. Add a new version instead.
4. Change original content in the generator and the database together, and add an independent check for every new answer.
5. State status precisely: implemented, tested, deployed, partially complete, planned or blocked.

## Documentation

Start at [docs/README.md](docs/README.md), which lists every document and marks which are current and which are historical checkpoints.
