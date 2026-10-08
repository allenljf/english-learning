from __future__ import annotations

import json
import pathlib
import re
import sys

from content_contracts import find_contract_violations

ROOT = pathlib.Path(__file__).resolve().parents[1]

problems = find_contract_violations(ROOT)
words = json.loads((ROOT / 'content/vocabulary.json').read_text())
questions = json.loads((ROOT / 'content/questions.json').read_text())
reading = json.loads((ROOT / 'content/reading.json').read_text())
listening = json.loads((ROOT / 'content/listening.json').read_text())
tenses = json.loads((ROOT / 'content/tenses.json').read_text())
scenarios = json.loads((ROOT / 'content/tense-scenarios.json').read_text())
all_questions = questions + [q for passage in reading for q in passage['questions']] + listening

if len({q['id'] for q in all_questions}) != len(all_questions):
    problems.append('Question IDs collide across question bank, reading, and listening.')
for scenario in scenarios:
    if len(scenario.get('tenses', [])) != 12:
        problems.append(f"{scenario['id']}: expected 12 generated tense rows.")
    for tense in scenario.get('tenses', []):
        for voice in ('active', 'passive'):
            cells = tense.get(voice, [])
            if len(cells) != 3 or any(not cell.endswith(('.', '?')) for cell in cells):
                problems.append(f"{scenario['id']} / {tense.get('name')} / {voice}: expected three punctuated forms.")
if len(tenses) != 12 or sum(t.get('rare', False) for t in tenses) != 4:
    problems.append('The base tense matrix must preserve 12 tenses and four rare-passive warnings.')

full = (ROOT / 'docs/00-complete.md').read_text() if (ROOT / 'docs/00-complete.md').exists() else ''
for item in words:
    if item['id'] not in full:
        problems.append(f"Full book is missing vocabulary entry {item['id']}.")
for q in all_questions:
    if q['id'] not in full:
        problems.append(f"Full book is missing question {q['id']}.")
for path in [ROOT / 'README.md', *(ROOT / 'docs').glob('*.md'), *(ROOT / 'docs/vocabulary').glob('*.md')]:
    for href in re.findall(r'\[[^\]]+\]\(([^)]+)\)', path.read_text()):
        if not href.startswith(('http', '#')) and not (path.parent / href.split('#')[0]).exists():
            problems.append(f"{path.relative_to(ROOT)} has a broken local link: {href}")
app = (ROOT / 'app.js').read_text()
page = (ROOT / 'index.html').read_text()
if re.search(r'fetch\(|XMLHttpRequest|https?://', app):
    problems.append('Runtime app code must remain independent of remote requests.')
if re.search(r'(?:src|href)="https?://', page):
    problems.append('Runtime HTML must not load remote assets.')
for artifact in ('index.html', 'app.js', 'styles.css', 'data.js', 'listening-audio.js', 'english-study-pack.zip'):
    if not (ROOT / artifact).exists() or (ROOT / artifact).stat().st_size < 20:
        problems.append(f'Missing or empty deliverable: {artifact}.')

if problems:
    for problem in problems:
        print('FAIL:', problem)
    sys.exit(1)

counts = {kind: sum(q.get('kind') == kind for q in questions) for kind in ('填空', '文法')}
counts['閱讀'] = sum(len(p['questions']) for p in reading if p['id'].startswith('R'))
print(f"PASS: {len(words):,} unique headwords with examples; {counts['閱讀']} reading, {counts['填空']} cloze, {counts['文法']} grammar, and {len(listening)} listening questions; five tense scenarios; links and static runtime verified.")
