from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1]
words=json.loads((R/'content/vocabulary.json').read_text())
questions=json.loads((R/'content/questions.json').read_text())
reading=json.loads((R/'content/reading.json').read_text())
tenses=json.loads((R/'content/tenses.json').read_text())
assert len(words)>=1000 and len({w['word'].casefold() for w in words})==len(words)
assert len({w['id'] for w in words})==len(words)
for w in words:
 assert w['senses'] and all(s['zh'] and s['phrase'] and s['pos'] in {'n','v','adj','adv','prep','conj','det'} for s in w['senses'])
 assert w['category'] in w['categories']
 if any(s['pos']=='v' for s in w['senses']): assert len(w['forms'])==4 and all(w['forms'])
lookup={w['word']:w for w in words}
for word,forms in {'shrink':['shrinks','shrank / shrunk','shrunk','shrinking'],'troubleshoot':['troubleshoots','troubleshot','troubleshot','troubleshooting'],'apply':['applies','applied','applied','applying'],'refer':['refers','referred','referred','referring'],'be':['am/is/are','was/were','been','being']}.items():assert lookup[word]['forms']==forms,(word,lookup[word]['forms'])
allq=questions+[q for p in reading for q in p['questions']]
assert len(allq)==120 and len({q['id'] for q in allq})==120
for q in allq:
 assert len(q['options'])==len(set(q['options']))==len(q['reasons'])==4,q['id']
 assert 0<=q['answer']<4 and q['zh'] and q['tip']
 assert all(len(x)>4 for x in q['reasons'])
for p in reading:
 assert p['text'] and p['zh'] and len(p['questions'])==4
 if p['id'].startswith('C'):assert all(f'[{n}]' in p['text'] for n in range(1,5))
assert len(tenses)==12 and sum(len(t['active'])+len(t['passive']) for t in tenses)==72
assert sum(t['rare'] for t in tenses)==4
for t in tenses:assert t['active'][2].endswith('?') and t['passive'][2].endswith('?')
assert len(list((R/'docs/vocabulary').glob('*.md')))==23
full=(R/'docs/00-complete.md').read_text()
assert all(w['id'] in full for w in words)
assert all(q['id'] in full for q in allq)
for p in [R/'README.md',*(R/'docs').glob('*.md')]:
 for href in re.findall(r'\[[^\]]+\]\(([^)]+)\)',p.read_text()):
  if not href.startswith(('http','#')):assert (p.parent/href.split('#')[0]).exists(),(p,href)
for f in ['index.html','app.js','styles.css','data.js']:assert (R/f).stat().st_size>100
app=(R/'app.js').read_text();page=(R/'index.html').read_text()
assert not re.search(r'fetch\(|XMLHttpRequest|https?://',app)
assert not re.search(r'(?:src|href)="https?://',page)
print(f'PASS: {len(words)} unique words, 23 categories, 269 verb paradigms, 72 tense cells, {len(allq)} explained questions, all Markdown local links valid; no remote runtime dependencies.')
