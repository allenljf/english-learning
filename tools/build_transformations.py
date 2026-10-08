from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
# Each row is intentionally authored, including time anchors and naturalness notes.
tenses=[
('現在簡單式','習慣、事實；每天例行檢查','checks the sensor every day','does not check the sensor every day','Does the technician check the sensor every day?','is checked every day','is not checked every day','Is the sensor checked every day?'),
('過去簡單式','已結束的過去；昨天檢查','checked the sensor yesterday','did not check the sensor yesterday','Did the technician check the sensor yesterday?','was checked yesterday','was not checked yesterday','Was the sensor checked yesterday?'),
('未來簡單式','預測、承諾；明天會檢查','will check the sensor tomorrow','will not check the sensor tomorrow','Will the technician check the sensor tomorrow?','will be checked tomorrow','will not be checked tomorrow','Will the sensor be checked tomorrow?'),
('現在進行式','現在進行中的動作；正在檢查','is checking the sensor now','is not checking the sensor now','Is the technician checking the sensor now?','is being checked now','is not being checked now','Is the sensor being checked now?'),
('過去進行式','過去某時正在做；昨天十點正在檢查','was checking the sensor at ten yesterday','was not checking the sensor at ten yesterday','Was the technician checking the sensor at ten yesterday?','was being checked at ten yesterday','was not being checked at ten yesterday','Was the sensor being checked at ten yesterday?'),
('未來進行式','未來某時正在做；明天十點會正在檢查','will be checking the sensor at ten tomorrow','will not be checking the sensor at ten tomorrow','Will the technician be checking the sensor at ten tomorrow?','will be being checked at ten tomorrow','will not be being checked at ten tomorrow','Will the sensor be being checked at ten tomorrow?'),
('現在完成式','過去到現在的完成結果；已檢查過，結果與現在有關','has checked the sensor','has not checked the sensor yet','Has the technician checked the sensor yet?','has been checked','has not been checked yet','Has the sensor been checked yet?'),
('過去完成式','在另一過去事件以前已完成；主管抵達前已檢查','had checked the sensor before the supervisor arrived','had not checked the sensor before the supervisor arrived','Had the technician checked the sensor before the supervisor arrived?','had been checked before the supervisor arrived','had not been checked before the supervisor arrived','Had the sensor been checked before the supervisor arrived?'),
('未來完成式','到未來參考點已完成；到明天中午會已檢查','will have checked the sensor by noon tomorrow','will not have checked the sensor by noon tomorrow','Will the technician have checked the sensor by noon tomorrow?','will have been checked by noon tomorrow','will not have been checked by noon tomorrow','Will the sensor have been checked by noon tomorrow?'),
('現在完成進行式','從過去持續到現在，強調過程；一直檢查兩小時了','has been checking the sensor for two hours','has not been checking the sensor for two hours','Has the technician been checking the sensor for two hours?','has been being checked for two hours','has not been being checked for two hours','Has the sensor been being checked for two hours?'),
('過去完成進行式','持續到過去參考點；主管來時已檢查兩小時','had been checking the sensor for two hours when the supervisor arrived','had not been checking the sensor for two hours when the supervisor arrived','Had the technician been checking the sensor for two hours when the supervisor arrived?','had been being checked for two hours when the supervisor arrived','had not been being checked for two hours when the supervisor arrived','Had the sensor been being checked for two hours when the supervisor arrived?'),
('未來完成進行式','持續到未來參考點；到中午會已檢查兩小時','will have been checking the sensor for two hours by noon','will not have been checking the sensor for two hours by noon','Will the technician have been checking the sensor for two hours by noon?','will have been being checked for two hours by noon','will not have been being checked for two hours by noon','Will the sensor have been being checked for two hours by noon?')]
formulas=[('V / V-s','am/is/are + p.p.'),('V-ed / 不規則過去','was/were + p.p.'),('will + V','will be + p.p.'),('am/is/are + V-ing','am/is/are being + p.p.'),('was/were + V-ing','was/were being + p.p.'),('will be + V-ing','will be being + p.p.'),('have/has + p.p.','have/has been + p.p.'),('had + p.p.','had been + p.p.'),('will have + p.p.','will have been + p.p.'),('have/has been + V-ing','have/has been being + p.p.'),('had been + V-ing','had been being + p.p.'),('will have been + V-ing','will have been being + p.p.')]
md=['# 時態 × 語態 × 肯定否定疑問：72 格變化實驗室','\n同一個動作 check，變更時間與觀察角度。每組中文描述的是肯定句情境；否定句否定該敘述，疑問句詢問該敘述是否成立。主動主詞固定為 the technician，受詞 the sensor；被動主詞改為 the sensor。p.p. 是過去分詞，不是過去式的同義詞。','\n優先精熟現在／過去簡單、現在進行、現在完成及 will 未來；再補其他組合。標有「辨識用」的被動形式非常少見，不建議當成日常表達模板。']
matrix=[]
for i,(name,usage,pos,neg,q,pp,pn,pq) in enumerate(tenses):
    rare=i in (5,9,10,11)
    active=['The technician '+pos+'.','The technician '+neg+'.',q]
    passive=['The sensor '+pp+'.','The sensor '+pn+'.',pq]
    md += ['\n## '+name,'\n情境：'+usage+'。','\n主動公式：`'+formulas[i][0]+'`；被動公式：`'+formulas[i][1]+'`。','\n| 語態 | 肯定 | 否定 | 疑問 |','| --- | --- | --- | --- |','| 主動 | '+' | '.join(active)+' |','| 被動'+('（辨識用）' if rare else '')+' | '+' | '.join(passive)+' |']
    note=''
    if rare:
        note='此被動在形式上可組合，但冗長且少見。實際表達優先使用本列主動句。若不重要的是持續過程，可改用簡單或完成被動，但語意重點會改變。'
        md += ['\n'+note]
    if i in (9,10,11):
        md+=['\n否定句中的 for two hours 可能否定「有在做」或「已持續兩小時」；若只想說尚不足兩小時，寫 `... but for less than two hours`；若完全未檢查，用 `has/had not checked` 並依參考時間調整。不要把長度否定當成唯一固定中文意思。']
    matrix.append(dict(name=name,usage=usage,active=active,passive=passive,rare=rare,note=note,formulas=formulas[i]))
md+=['''
## 替換人稱，不要全句亂改

`I check → I do not check → Do I check?`；`She checks → She does not check → Does she check?`
`I am checking → We are checking → He is checking`。
`I have checked → She has checked → They have checked`。
`She checked → They checked`：一般過去式除 be 外不隨人稱改變。
`She will check → They will check`：will 後都用原形。

## 一個動作延伸到疑問詞

- What does she check? 她檢查什麼？what 取代受詞。
- Who checks the sensor? 誰檢查感測器？who 本身作主詞，一般肯定主詞問句不加 does。
- When did she check it? 她何時檢查？did 後回原形。
- How long has she been checking it? 她已經檢查多久？問持續長度。
- Why was it checked again? 為何又檢查了一次？被動的疑問。
- Hasn't she checked it yet? 她還沒檢查嗎？否定疑問常帶期待或驚訝，不是中性的 Has she ...?

## 同一消息，用意不同

`She checked it.`：過去做過此事。
`She has checked it.`：已做過，對現在狀態有關。
`She was checking it when I called.`：我打電話當時正在做，不保證完成。
`She had checked it when I called.`：我打電話前已完成。
`She has been checking it.`：强调最近持續的過程，可能剛停或仍在做。

## 不適合硬套的組合

- 狀態動詞 know、belong、own 在一般認知／所有權意思通常不用進行式。`I know the answer.`
- 同一動詞換意思可用進行式：`I think it is safe.`（認為）vs. `I am thinking about the proposal.`（正在思考）。
- `I have a car.` 表所有權；`I am having lunch.` 表正在吃午餐。不是 have 永遠不能進行。
- 不及物 arrive、happen 通常不造被動；`The incident happened yesterday.`
- 每個句子都能加否定，不代表否定後語意仍適合同一情境。先決定要說的事，再選形式。

## 自己做六格練習

把 check the sensor 換成 inspect the pump、test the sample、review the report，各寫：現在習慣、昨天完成、現在正在、到現在已完成、明天會做、昨天被做。再各改一個否定及疑問。答案不能只看尾巴；要檢查主詞、助動詞與動詞原形／分詞是否一起改對。
''']
(ROOT/'content/05-transformations.md').write_text('\n'.join(md))
(ROOT/'content/tenses.json').write_text(json.dumps(matrix,ensure_ascii=False,indent=2))
scenario_file=ROOT/'content/tense-scenarios.json'
if scenario_file.exists():
    scenarios=json.loads(scenario_file.read_text())
    cue_sets=[
      ['every shift','yesterday','tomorrow','now','at 10 a.m. yesterday','at 10 a.m. tomorrow','already','before the supervisor arrived','by noon tomorrow','for two hours','for two hours when the supervisor arrived','for two hours by noon'],
      ['before release each day','during yesterday’s audit','tomorrow morning','right now','at 2 p.m. yesterday','at 2 p.m. tomorrow','already','before the lot was approved','by the end of tomorrow','since the morning','since the morning when the manager arrived','for three hours by noon'],
      ['once a month','last Monday','next week','at present','at 4 p.m. yesterday','at 4 p.m. tomorrow','this week','before the line restarted','by Friday','for an hour','for an hour when the shift ended','for two hours by five in the afternoon'],
      ['at the end of each run','during the last run','in the next run','currently','at 8 a.m. yesterday','at 8 a.m. tomorrow','so far today','before the review began','by the next review','since noon','since noon when the audit began','for four hours by the deadline'],
      ['every quarter','yesterday afternoon','tomorrow afternoon','at this moment','at 3 p.m. yesterday','at 3 p.m. tomorrow','already this month','before the next batch started','by next month','for two days','for two days when the review began','for two days by Friday']]
    def forms(s,cue,index,voice,polarity):
        actor=s['actor'];obj=s['object'];base=s['base'];third=s['thirdPerson'];past=s['past'];pp=s['pastParticiple'];ing=s['ing']
        if voice=='active':
            positives=[f'{actor} {third} {obj} {cue}',f'{actor} {past} {obj} {cue}',f'{actor} will {base} {obj} {cue}',f'{actor} is {ing} {obj} {cue}',f'{actor} was {ing} {obj} {cue}',f'{actor} will be {ing} {obj} {cue}',f'{actor} has {pp} {obj} {cue}',f'{actor} had {pp} {obj} {cue}',f'{actor} will have {pp} {obj} {cue}',f'{actor} has been {ing} {obj} {cue}',f'{actor} had been {ing} {obj} {cue}',f'{actor} will have been {ing} {obj} {cue}']
            aux=['does','did','will','is','was','will','has','had','will','has','had','will'][index]
            rest=[f'{base} {obj} {cue}',f'{base} {obj} {cue}',f'{base} {obj} {cue}',f'{ing} {obj} {cue}',f'{ing} {obj} {cue}',f'be {ing} {obj} {cue}',f'{pp} {obj} {cue}',f'{pp} {obj} {cue}',f'have {pp} {obj} {cue}',f'been {ing} {obj} {cue}',f'been {ing} {obj} {cue}',f'have been {ing} {obj} {cue}'][index]
            if polarity==0: text=positives[index]
            elif index==0:text=f'{actor} does not {base} {obj} {cue}'
            elif index==1:text=f'{actor} did not {base} {obj} {cue}'
            else:text=positives[index].replace(aux+' ',aux+' not ',1)
            if polarity==2: text=f'{aux.capitalize()} {actor.lower()} {rest}'
        else:
            be=['is','was','will be','is being','was being','will be being','has been','had been','will have been','has been being','had been being','will have been being'][index]
            positive=f'{obj.capitalize()} {be} {pp} {cue}'
            first=be.split()[0]
            if polarity==0:text=positive
            elif polarity==1:text=positive.replace(first+' ',first+' not ',1)
            else:
                parts=be.split(' ',1);text=f"{first.capitalize()} {obj} {parts[1]+' ' if len(parts)>1 else ''}{pp} {cue}"
        return text.rstrip('.!?')+('?' if polarity==2 else '.')
    for si,s in enumerate(scenarios):
        s['cues']=cue_sets[si]
        s['tenses']=[]
        for ti,base_t in enumerate(matrix):
            cells={}
            for voice in ('active','passive'):
                cells[voice]=[forms(s,s['cues'][ti],ti,voice,p) for p in range(3)]
            s['tenses'].append(dict(name=base_t['name'],usage=base_t['usage'],formulas=base_t['formulas'],rare=base_t['rare'],note=base_t['note'],active=cells['active'],passive=cells['passive']))
    scenario_file.write_text(json.dumps(scenarios,ensure_ascii=False,indent=2)+'\n')
