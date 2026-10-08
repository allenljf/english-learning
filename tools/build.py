from pathlib import Path
import json,re,html,runpy
ROOT=Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT/'tools'/'build_transformations.py'))
def inline(s):
    s=html.escape(s)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
    s=re.sub(r'\[([^\]]+)\]\(([^\s)]+)\)',r'<a href="\2">\1</a>',s)
    return s
def markdown(src):
    lines=src.splitlines();out=[];i=0
    while i<len(lines):
        s=lines[i].strip()
        if not s:i+=1;continue
        if s.startswith('#'):
            m=re.match(r'(#{1,6}) (.*)',s);n=len(m[1]);out.append(f'<h{n}>{inline(m[2])}</h{n}>');i+=1;continue
        if s.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                row=[x.strip() for x in lines[i].strip().strip('|').split('|')];i+=1
                if all(re.match(r'^:?-{3,}:?$',x) for x in row):continue
                rows.append(row)
            out.append('<div class="table-scroll" tabindex="0" role="region" aria-label="可左右捲動的對照表"><table>')
            for j,row in enumerate(rows):
                tag='th' if j==0 else 'td';out.append('<tr>'+''.join(f'<{tag}>{inline(x)}</{tag}>' for x in row)+'</tr>')
            out.append('</table></div>');continue
        if re.match(r'^(- |\d+\. )',s):
            ordered=bool(re.match(r'^\d+\.',s));tag='ol' if ordered else 'ul';out.append('<'+tag+'>')
            while i<len(lines) and re.match(r'^(- |\d+\. )',lines[i].strip()):
                out.append('<li>'+inline(re.sub(r'^(- |\d+\. )','',lines[i].strip()))+'</li>');i+=1
            out.append('</'+tag+'>');continue
        para=[]
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||- |\d+\. )',lines[i].strip()):
            para.append(lines[i].strip());i+=1
        out.append('<p>'+'<br>'.join(inline(x) for x in para)+'</p>')
    return '\n'.join(out)
# Merge headwords across senses and categories; do not inflate the unique-word count.
words={};cats=[]
for line in (ROOT/'content/vocabulary.txt').read_text().splitlines():
    if line.startswith('# '):cat=line[2:];cats.append(cat);continue
    if not line:continue
    w,pos,zh,phrase=line.split('|')
    if w not in words:words[w]=dict(id=f'W{len(words)+1:04}',word=w,category=cat,categories=[],senses=[])
    if cat not in words[w]['categories']:words[w]['categories'].append(cat)
    sense=dict(pos=pos,zh=zh,phrase=phrase)
    if sense not in words[w]['senses']:words[w]['senses'].append(sense)
# Additional headwords and examples are authored in JSON so the same source feeds
# both the web app and the downloadable books.
extra_path=ROOT/'content/vocabulary-extra.json'
if extra_path.exists():
    for item in json.loads(extra_path.read_text()):
        w=item['word'];key=w.casefold()
        found=next((x for x in words.values() if x['word'].casefold()==key),None)
        if found:
            for sense in item.get('senses',[]):
                if sense not in found['senses']:found['senses'].append(sense)
            if item.get('category') not in found['categories']:found['categories'].append(item['category'])
            continue
        words[w]=dict(id=f'W{len(words)+1:04}',word=w,category=item['category'],categories=[item['category']],senses=item['senses'],example=item.get('example',''),exampleZh=item.get('exampleZh',''))
example_path=ROOT/'content/vocabulary-examples.json'
examples=json.loads(example_path.read_text()) if example_path.exists() else {}
irregular=[line.split('|') for line in (ROOT/'content/irregular.txt').read_text().splitlines() if line]
lookup={r[0]:r[1:5] for r in irregular}
def inflect(w):
    if w in lookup:return lookup[w]
    double=w in {'admit','permit','submit','refer','prefer','stop','drop','ship'}
    third=w+'es' if w.endswith(('s','sh','ch','x','z','o')) else w[:-1]+'ies' if w.endswith('y') and w[-2] not in 'aeiou' else w+'s'
    past=w+'d' if w.endswith('e') else w[:-1]+'ied' if w.endswith('y') and w[-2] not in 'aeiou' else w+w[-1]+'ed' if double else w+'ed'
    ing=w[:-1]+'ing' if w.endswith('e') and not w.endswith('ee') else w+w[-1]+'ing' if double else w+'ing'
    return [third,past,past,ing]
for w,item in words.items():
    if any(s['pos']=='v' for s in item['senses']):item['forms']=inflect(w)
    entry=examples.get(w.casefold(),{})
    item['example']=entry.get('example') or item.get('example','')
    item['exampleZh']=entry.get('exampleZh') or item.get('exampleZh','')
families=[]
for row in (ROOT/'content/families.txt').read_text().splitlines():
    a=row.split('|');assert len(a)==9
    families.append(dict(zip(['verb','noun','person','adj','adv','phrase','phrase2','example','memory'],a)))
# Markdown deliverables.
vdir=ROOT/'docs/vocabulary';vdir.mkdir(parents=True,exist_ok=True)
links=[]
for n,cat in enumerate(cats,1):
    items=[x for x in words.values() if x['category']==cat]
    md=[f'# {cat}',f'\n本冊 {len(items)} 個首次歸類的獨立單字；跨情境同字合併在首次出現處。n 名詞、v 動詞、adj 形容詞、adv 副詞、prep 介系詞、conj 連接詞、det 限定詞。只列本教材選用意思，不宣稱涵蓋字典所有義項。','\n先遮中文說意思，再看搭配造句；造句示範與記憶方法見「單字與詞形學習法」。','\n| 編號 | 單字 | 詞性與中文 | 常用搭配 |','| --- | --- | --- | --- |']
    for x in items:
        md.append('| '+x['id']+' | '+x['word']+' | '+'；'.join(s['pos']+'. '+s['zh'] for s in x['senses'])+' | '+'；'.join(s['phrase'] for s in x['senses'])+' |')
        md.append('例句：'+x['example']+'<br>中文：'+x['exampleZh'])
    filename=f'{n:02}.md';(vdir/filename).write_text('\n'.join(md).rstrip()+'\n');links.append(f'- [{cat}（{len(items)} 字）](vocabulary/{filename})')
(ROOT/'docs/07-vocabulary-index.md').write_text('# 單字分冊索引\n\n共 '+str(len(words))+' 個不重複 headwords。不同詞性、複數或時態形式不重複灌水計數；同一拼字不同義項合併。另有例句補充字不計入此數。\n\n'+'\n'.join(links)+'\n')
for path in (ROOT/'content').glob('*.md'):
    text=path.read_text()
    for a,b in {'语气':'語氣','可数':'可數','决定':'決定','常见':'常見','结构':'結構','强调':'強調','情绪':'情緒','期間':'期間','期间':'期間','数量':'數量','单独':'單獨','读一次':'讀一次'}.items():text=text.replace(a,b)
    path.write_text(text);(ROOT/'docs'/path.name).write_text(text)
fmd=['# 詞族對照：派生、屈折與語意關聯','\n橫線表示未列常用對應詞，不是絕對不存在。不要自行把每個格子都補成字。分詞形容詞如 approved 是屈折形式作修飾語，與新的派生詞如 approval 不同。']
for f in families:
    fmd += ['\n## '+f['verb'],'\n| 動詞 | 名詞 | 人 | 形容詞 | 副詞 |','| --- | --- | --- | --- |','| '+' | '.join(f[k] for k in ['verb','noun','person','adj','adv'])+' |','\n搭配：`'+f['phrase']+'`；`'+f['phrase2']+'`。','\n案例：'+f['example'],'\n記憶與辨析：'+f['memory']]
(ROOT/'docs/08-word-families.md').write_text('\n'.join(fmd)+'\n')
vmd=['# 動詞五態與不規則表','\n以美式拼字為主；五欄依序為原形、三單現在、過去、過去分詞、現在分詞。be 的 am/is/are 須按人稱選，不全是三單。read 過去與分詞拼法相同但讀 /red/，現在原形讀 /riːd/。gotten 常見於美式；get 的具體完成式用法仍須依語意判斷。cost 表成本通常 cost–cost；作估價可見 costed。','\n## 64 個常用不規則動詞','\n| 原形 | 三單／be 人稱 | 過去 | 過去分詞 | V-ing | 中文 |','| --- | --- | --- | --- | --- | --- |']
vmd+=['| '+' | '.join(r)+' |' for r in irregular]
vmd+=['\n## 單字庫所有動詞的五態','\n規則動詞亦完整列出。knowing 等形式的存在，不表示 know 的每個意思都能使用進行式。詞形正確與句子用法正確是兩個檢查。','\n| 原形 | 三單／be 人稱 | 過去 | 過去分詞 | V-ing |','| --- | --- | --- | --- | --- |']
vmd+=['| '+' | '.join([x['word']]+x['forms'])+' |' for x in words.values() if 'forms' in x]
(ROOT/'docs/09-verb-forms.md').write_text('\n'.join(vmd)+'\n')
questions=json.loads((ROOT/'content/questions.json').read_text());reading=json.loads((ROOT/'content/reading.json').read_text())
listening=json.loads((ROOT/'content/listening.json').read_text()) if (ROOT/'content/listening.json').exists() else []
def qmd(q):
    out=[f"\n### {q['id']} · {q['topic']}",f"\n{q['stem']}"]
    out+=['\n'+chr(65+i)+'. '+x for i,x in enumerate(q['options'])]
    out+=['\n<details>','<summary>作答後看翻譯與解析</summary>','\n中文：'+q['zh'],f"\n答案：{chr(65+q['answer'])} · {q['options'][q['answer']]}"]
    out+=['\n- '+chr(65+i)+'：'+reason for i,reason in enumerate(q['reasons'])]
    out+=['\n記法：'+q['tip'],'\n</details>'];return '\n'.join(out)
for kind,name in [('填空','10-cloze-practice.md'),('文法','11-grammar-practice.md')]:
    (ROOT/'docs'/name).write_text('# '+kind+'練習與逐項解析\n\n原創教學練習，先作答再展開解析。不限時學會後再計時；不是官方模擬卷，不換算正式分數。\n'+''.join(qmd(q) for q in questions if q['kind']==kind))
r_count=sum(len(x['questions']) for x in reading if x['id'].startswith('R'));c_count=sum(len(x['questions']) for x in reading if x['id'].startswith('C'))
rmd=[f'# 閱讀與段落填空：{len([x for x in reading if x["id"].startswith("R")])} 個閱讀題組、{r_count} 題閱讀、{c_count} 題段落填空','\n原創教學情境，非真實公司公告。先讀英文作答，再看翻譯與證據；每題四選一。']
for r in reading:
    rmd += ['\n## '+r['id']+' '+r['title'],f"\n{r['level']} · {r['genre']}\n",r['text'],'\n<details>\n<summary>查看全文中文</summary>\n\n'+r['zh']+'\n\n</details>','\n策略：'+r['strategy']]
    rmd += [qmd(q) for q in r['questions']]
(ROOT/'docs/12-reading-practice.md').write_text('\n'.join(rmd)+'\n')
if listening:
    lmd=['# 聽力策略與練習案例','\n以下為原創文字轉語音練習，不是官方錄音，也不代表真實口音。播放時先抓場景、人物關係、轉折與數字。']
    for q in listening:
        lmd += [f"\n## {q['id']} · Part {q['part']} · {q['scene']}",f"\n{q['stem']}"]
        lmd += ['\n'+chr(65+i)+'. '+x for i,x in enumerate(q['options'])]
        lmd += ['\n<details><summary>作答後看逐字稿、翻譯與解析</summary>\n']
        lmd += [f"{s['speaker']}: {s['text']}" for s in q['segments']]
        lmd += ['\n中文：'+q['zh'],f"\n答案：{chr(65+q['answer'])} · {q['options'][q['answer']]}"]
        lmd += ['\n- '+chr(65+i)+'：'+reason for i,reason in enumerate(q['reasons'])]
        lmd += ['\n策略：'+q['tip'],'\n</details>']
    (ROOT/'docs/15-listening-practice.md').write_text('\n'.join(lmd)+'\n')
scenarios=json.loads((ROOT/'content/tense-scenarios.json').read_text()) if (ROOT/'content/tense-scenarios.json').exists() else []
article_paths=['01-guide.md','02-grammar.md','03-prepositions.md','04-reading.md','05-transformations.md','06-vocabulary-method.md','08-word-families.md','09-verb-forms.md','14-youtube-toeic-resources.md']+(['15-listening-practice.md'] if listening else [])
articles=[dict(id=p.split('-')[0],title=(ROOT/'docs'/p).read_text().splitlines()[0][2:],path='docs/'+p,html=markdown((ROOT/'docs'/p).read_text())) for p in article_paths]
data=dict(words=list(words.values()),categories=cats,families=families,irregular=irregular,tenses=json.loads((ROOT/'content/tenses.json').read_text()),tenseScenarios=scenarios,questions=questions,reading=reading,listening=listening,articles=articles)
(ROOT/'data.js').write_text('window.ENGLISH_DATA = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n')
(ROOT/'content/vocabulary.json').write_text(json.dumps(list(words.values()),ensure_ascii=False,indent=2))
allparts=['# 電子廠英文學習全冊\n\n繁體中文 · 原創練習 · 離線教材\n\n此檔整合全部分冊，可全文搜尋與備份；網站入口為根目錄 index.html。\n']
for p in sorted((ROOT/'docs').glob('*.md')):
    if p.name in ['00-complete.md','07-vocabulary-index.md']:continue
    allparts.append(p.read_text())
allparts+= [p.read_text() for p in sorted(vdir.glob('*.md'))]
allparts.append((ROOT/'CONTENT-LICENSE.md').read_text())
(ROOT/'docs/00-complete.md').write_text('\n\n---\n\n'.join(allparts).rstrip()+'\n')
print('Unique words:',len(words),'Verb headwords:',sum('forms' in x for x in words.values()),'Families:',len(families),'Questions:',len(questions)+sum(len(r['questions']) for r in reading)+len(listening))
import zipfile
manifest=['index.html','app.js','listening-audio.js','data.js','styles.css','README.md','VERIFICATION.md','CONTENT-LICENSE.md','licenses/ECDICT-LICENSE.txt','docs/00-complete.md']
manifest += [str(p.relative_to(ROOT)) for p in sorted((ROOT/'docs').glob('*.md')) if p.name!='00-complete.md']
manifest += [str(p.relative_to(ROOT)) for p in sorted((ROOT/'docs/vocabulary').glob('*.md'))]
manifest += [str(p.relative_to(ROOT)) for p in sorted((ROOT/'content').glob('*.json'))]
manifest += ['content/vocabulary.txt','content/irregular.txt','content/families.txt']
with zipfile.ZipFile(ROOT/'english-study-pack.zip','w',zipfile.ZIP_DEFLATED) as archive:
    for name in manifest:
        path=ROOT/name
        if path.exists():archive.write(path,name)
