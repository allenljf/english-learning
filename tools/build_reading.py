import json,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sets=[]
def passage(id,title,level,genre,text,zh,strategy,items):
    qs=[]
    for n,item in enumerate(items,1):
        topic,stem,translation,*answers=item
        pairs=[a.split('~',1) for a in answers]
        assert len(pairs)==4
        order=list(range(4));random.Random(len(sets)*10+n+32).shuffle(order)
        qs.append(dict(id=f'{id}-{n}',kind='段落填空' if id.startswith('C') else '閱讀',topic=topic,stem=stem,zh=translation,options=[pairs[i][0] for i in order],answer=order.index(0),reasons=[pairs[i][1] for i in order],tip=strategy))
    sets.append(dict(id=id,title=title,level=level,genre=genre,text=text,zh=zh,strategy=strategy,questions=qs))
passage('R01','無塵室入口通知','基礎','公告', '''Cleanroom Access Notice
Starting Monday, October 5, all visitors to Building C must use the east entrance. The west entrance will be closed for floor repairs until October 9. Employees may continue to use the north entrance with their regular badges.
Visitors must present photo identification at the east reception desk and wait for their host. Reception staff will issue a temporary badge after confirming the appointment. A temporary badge does not allow visitors to enter the cleanroom alone. Hosts must accompany them at all times. Protective clothing is available at the changing area; visitors do not need to bring their own. Please allow an additional fifteen minutes for registration.''','''自十月五日週一起，C 棟訪客須走東入口。西入口因地板維修關閉至十月九日。員工仍可持原識別證走北入口。
訪客須在東側接待處出示有照片的身分證件並等接待人。櫃台確認預約後發臨時證。臨時證不允許訪客獨自進無塵室，接待人必須全程陪同。更衣區提供防護衣，訪客不用自備。登記請多預留十五分鐘。''','先區分 visitors 與 employees，再圈 must、may、do not need。',[
('細節','Which entrance should visitors use starting October 5?','十月五日起訪客應走哪個入口？','The east entrance.~第一句明確指 all visitors ... east entrance。','The north entrance.~北入口只說員工可繼續使用。','The west entrance.~西入口維修關閉。','Any entrance with a badge.~臨時證不表示任何入口皆可。'),
('細節','What must visitors present?','訪客必須出示什麼？','Photo identification.~第二段第一句的直接要求。','Their own protective clothing.~文章說不用自備防護衣。','A repair invoice.~未提及請款單。','An employee badge.~訪客取得的是臨時證，不是員工證。'),
('推論','What can be concluded about a temporary badge?','臨時證可以得出什麼結論？','It does not replace the need for a host.~文章明說仍須全程由 host 陪同。','It permits unaccompanied cleanroom access.~與 does not allow ... alone 相反。','It is valid at every company site.~未提其他廠區適用範圍。','It must be purchased online.~未提購買或費用。'),
('目的','Why should visitors arrive fifteen minutes early?','為何建議訪客提早十五分鐘？','To allow time for registration.~最後一句直接說 for registration。','To repair the floor.~訪客不是修繕人員。','To buy protective clothing.~防護衣現場提供。','To attend a mandatory safety lecture.~本文未提課程，不可用常識補。')])
passage('R02','維護排程與下一步','基礎','內部郵件','''To: Line B Team
Subject: Revised pump inspection
The inspection originally planned for Tuesday has been moved to Thursday, October 8. The replacement pressure sensor will not arrive until Wednesday afternoon, and the maintenance team needs time to install it before the inspection.
Please keep Pump B2 offline until the inspection is complete and the supervisor gives written approval. Production may continue on Pump B1, which passed its inspection last week. Do not move the sensor from B1 to B2. If you need additional capacity before Thursday, contact Planning by noon today. Planning will check whether work can be transferred to Line A; no transfer has been approved yet.''','''原訂週二的檢查改到十月八日週四，因替換壓力感測器週三下午才到，維護團隊須先安裝。B2 幫浦須保持停機，直到檢查完成且主管書面核准。上週通過檢查的 B1 可繼續生產，不可把 B1 感測器移至 B2。週四前需要額外產能者，今天中午前聯絡生管。生管將查是否可轉至 A 線，目前尚未批准任何轉線。''','把已完成、計畫中、尚未批准分成三欄。',[
('細節','When is the inspection now scheduled?','檢查現在排何時？','Thursday, October 8.~moved to Thursday 是新日期。','Tuesday.~Tuesday 是原日期。','Wednesday morning.~週三下午是感測器到貨，不是檢查。','Last week.~上週是 B1 的檢查。'),
('原因','Why was the inspection moved?','檢查為何改期？','A required sensor will arrive later.~零件週三下午才到，須先安裝。','Pump B1 failed its inspection.~B1 是 passed。','The supervisor is on leave.~未提主管請假。','Line A has already accepted the work.~本文說尚未核准轉線。'),
('條件','What is required before restarting B2?','B2 重啟前需要什麼？','A completed inspection and written approval.~until 後有兩個條件，以 and 連接。','Only the arrival of the new sensor.~到貨不是足夠條件。','Permission from the supplier alone.~核准者是 supervisor，不是供應商。','A transfer of the B1 sensor.~文中明確禁止移動 B1 感測器。'),
('推論','Which statement is supported?','何者有原文支持？','A transfer to Line A is still uncertain.~will check whether 加 no transfer ... approved，仍未定。','Line A will definitely start the work today.~把待確認改成確定。','Both pumps must remain offline.~B1 可繼續。','B2 can restart Wednesday afternoon.~未滿足檢查與書面核准。')])
passage('R03','採購單與分批出貨','中階','雙文件','''Document A — Purchase order PO-184
Item: pressure sensors, model PS-8
Quantity: 20; unit price: $45
Standard shipping: included
Requested arrival: October 12
Note: Contact us before substituting another model.

Document B — Supplier email
Thank you for order PO-184. We have twelve PS-8 sensors ready for dispatch on October 7. The remaining eight will be dispatched on October 14. Standard delivery takes two business days after dispatch. Our business days are Monday through Friday, and there are no holidays in this period. We can offer model PS-9 for immediate dispatch instead, but it requires a different connector. Please confirm whether you prefer a split shipment or a substitute. We will not make a substitution without your approval. There is no extra shipping charge for a split shipment.''','''A：訂單 PO-184，PS-8 壓力感測器二十個，每個四十五元，含標準運送，要求十月十二日到貨；換型號前先聯絡。
B：十二個 PS-8 可十月七日出貨，其餘八個十月十四日出貨。標準配送自出貨後需兩個工作天，工作日週一至週五，此期間無假日。可改 PS-9 立即出貨，但需不同連接器。請確認分批或替代方案，未核准前不替換。分批不加運費。''','先對單號，再區分 dispatch 出貨與 arrival 到貨。',[
('計算','What is the total price of the sensors in the original order?','原訂感測器總價多少？','$900.~20 × 45 = 900；標準運送包含在內。','$540.~這只算先寄十二個。','$360.~這只算剩下八個。','$945.~多加一個四十五元，文中沒有此費用。'),
('跨文推論','Why can the full original order not arrive by October 12 using the stated schedule?','依此時程，整筆原訂單為何無法十二日前到齊？','Eight units will not be dispatched until October 14.~其餘八個連出貨都在十四日，超過要求到貨日。','All twenty units are out of stock.~有十二個可先寄。','The buyer ordered the wrong connector.~只說替代型號需不同連接器，未說買錯。','Standard shipping is not available.~有標準運送。'),
('細節','What is true of the PS-9?','PS-9 有何特點？','It requires a different connector.~供應商信中的明確差異。','It costs less than the PS-8.~未提供 PS-9 價格。','It has already been shipped.~等待確認，未說已寄。','It is identical to the PS-8 in every way.~連接器需求不同。'),
('行動','What does the supplier ask the buyer to do?','供應商要求買方做什麼？','Choose a split shipment or a substitute.~Please confirm whether ... 明確請求。','Pay an extra split-shipment fee.~分批不加運費。','Cancel all twenty sensors.~不是要求取消。','Approve a price increase.~未提漲價。')])
passage('R04','技術員職缺','基礎','徵才廣告','''Maintenance Technician — Day Shift
We are seeking a technician to maintain automated packaging equipment. Applicants must have at least one year of relevant maintenance experience and be able to read English operating instructions. A technical diploma is preferred but not required. Experience with vacuum pumps is an advantage.
The regular schedule is Monday to Friday, 8 a.m. to 5 p.m. Occasional weekend work may be necessary during planned shutdowns. Training on our equipment will be provided. To apply, email a resume and a brief description of one maintenance problem you have solved to the recruitment team by October 16. Only shortlisted applicants will be contacted for an interview. Please do not visit the site without an appointment.''','''招募日班維護技術員，維護自動包裝設備。必須有至少一年相關維護經驗且能讀英文操作說明。技術文憑為優先條件，非必要；真空幫浦經驗加分。正常週一至週五八點至五點，計畫停機時偶爾可能週末工作，公司提供設備訓練。十月十六日前寄履歷及一個自己解決過的維護問題簡述。僅通知入選者面試，未預約勿直接到廠。''','把 required、preferred、an advantage 分開，不能把加分條件當必要。',[
('必要條件','Which qualification is required?','哪項是必備資格？','At least one year of relevant experience.~must have 是必要條件。','A technical diploma.~preferred but not required。','Vacuum pump experience.~an advantage，僅加分。','Five years of management experience.~未提五年或管理。'),
('細節','What should be sent with the resume?','履歷須附什麼？','A description of a maintenance problem the applicant solved.~申請方式明確要求。','A copy of a passport.~未提護照。','A complete training manual.~未要求交手冊。','A weekend work schedule.~未要求自行排班。'),
('推論','What does the advertisement suggest about weekends?','廣告對週末工作有何暗示？','Some weekend work is possible.~occasional ... may be necessary。','Every weekend is a regular workday.~把偶爾誇大成每週。','Weekend work is prohibited.~與文字相反。','Applicants must work only on weekends.~不是正常週一至週五班表。'),
('限制','Who will be contacted for an interview?','誰會收到面試通知？','Only shortlisted applicants.~Only shortlisted 是明確範圍。','Everyone who sends a resume.~不是所有人。','Only applicants with a diploma.~文憑不是必要，不能推出此限制。','Everyone who visits without an appointment.~明確不鼓勵無預約到廠。')])
passage('R05','費用報銷規則','中階','政策','''Travel Reimbursement — Effective October 1
Employees must obtain manager approval before booking business travel. The company reimburses economy-class transportation and hotel costs up to $120 per night. Meals are covered up to $35 per day, excluding alcohol. Original receipts must be submitted within ten calendar days after the trip ends.
If a hotel costs more than the standard limit, written approval from the Finance Director is required before booking. A manager's general approval for the trip does not automatically authorize a higher hotel rate. Lost receipts should be reported to Finance; reimbursement in these cases is reviewed individually and is not guaranteed. Claims received after the deadline will be returned unless Finance has approved an extension.''','''十月一日生效：預訂出差前須主管核准。補助經濟艙交通，住宿每晚最高一百二十元；餐費每日最高三十五元，不含酒精。旅程結束後十個日曆天內提交原始收據。住宿超標須預訂前取得財務總監書面核准，一般主管核准出差不自動核准超額房價。收據遺失須向財務報告，逐案審查且不保證報銷。逾期申請會退回，除非已批准延期。''','把基本規則、例外核准者及保證程度各畫一條線。',[
('細節','What is the standard hotel limit?','一般住宿上限多少？','$120 per night.~明確寫 up to $120 per night。','$120 per trip.~單位是每晚，不是整趟。','$35 per night.~35 是每日餐費額度。','There is no limit with manager approval.~一般核准不自動允許超額。'),
('條件','What is needed for a higher hotel rate?','超額住宿需什麼？','Written approval from the Finance Director before booking.~三要素：書面、財務總監、預訂前。','Only a manager’s general trip approval.~第二段明確否定。','A receipt submitted after booking.~收據不是事前例外核准。','A request from the hotel receptionist.~與權限無關。'),
('推論','What happens if an original receipt is lost?','原始收據遺失怎麼辦？','Finance reviews the case without guaranteeing reimbursement.~reviewed individually and not guaranteed。','Reimbursement is always approved.~把不保證改成保證。','Reimbursement is always rejected.~也不能從不保證推出一律拒絕。','The employee must cancel the completed trip.~行程已結束，不合文意。'),
('例外','When may a late claim avoid being returned?','逾期申請何時可能不被退回？','When Finance has approved an extension.~unless 後是唯一說明的例外。','Whenever the hotel is expensive.~房價不是逾期例外。','When alcohol is included.~酒精費用不補助。','When the employee submits a photocopy only.~未說影本可免除期限。')])
passage('R06','三文件：訓練名額與時間','中階','三文件','''Document A — Training announcement, October 1
Calibration Basics has two sessions: October 8, 9–11 a.m., and October 9, 2–4 p.m. Each session has twelve places. Register for only one session. Participants must complete the online safety module before attending. The workshop is in Room 204.

Document B — Registration confirmation to Mei Chen, October 2
You are confirmed for the October 9 afternoon session. You are on the waiting list for October 8; your original request was for that date. We will contact you if a place opens. Your safety module is marked complete.

Document C — Update to Mei Chen, October 6
A place is now available on October 8. To switch, reply by noon on October 7. If we do not hear from you, your October 9 booking will remain active. The October 8 session has moved to Room 310 because Room 204 is being repaired. The October 9 session will still be in Room 204.''','''A：校正基礎課有十月八日九至十一點、十月九日十四至十六點兩梯，每梯十二人，只能報一梯；課前須完成線上安全課，原教室 204。
B：Mei 已確認十月九日下午，原想報八日但候補；安全課已完成。
C：八日有空位了，若改梯須十月七日中午前回覆，未回則保留九日。八日因維修改教室 310，九日仍在 204。''','依時間排序更新，再分清「有空位」與「已改成功」。',[
('跨文細節','Which session is confirmed before Mei responds to the update?','Mei 回覆更新前，確定的是哪一梯？','October 9, 2–4 p.m.~B 已確認，C 說未回則保留。','October 8, 9–11 a.m.~只是可轉入，尚需回覆。','Both sessions.~A 規定只報一梯。','Neither session.~已有九日確認。'),
('跨文條件','What must Mei do to switch to October 8?','Mei 要改八日須做什麼？','Reply by noon on October 7.~C 的明確期限及動作。','Attend both sessions first.~不合只報一梯。','Repeat the completed safety module.~B 顯示已完成，無重做要求。','Arrive at Room 204 on October 8 without replying.~要先回覆且八日教室已改。'),
('跨文細節','Where will the October 8 session be held?','八日梯次在哪？','Room 310.~C 更新八日地點。','Room 204.~舊資訊，只適用九日。','The online safety portal.~線上安全課不是實體工作坊地點。','The location has not been announced.~已明確公告 310。'),
('推論','Which requirement has Mei already satisfied?','Mei 已滿足哪項要求？','Completing the online safety module.~B 明確 marked complete。','Replying to accept the October 8 place.~未提供她已回覆的文件。','Attending the workshop.~文件日期都在工作坊前。','Obtaining a refund.~未提收費或退款。')])
passage('R07','供應商品質處置','中階','品質報告','''Quality Review — Lot K17
We inspected a random sample of 80 connectors from the 800-unit lot received on October 2. Six sampled connectors had damaged pins. The rest of the sample passed the visual inspection. Electrical testing has not yet been completed.
The entire lot has been placed on hold. Please do not release any units to production until Quality gives written approval. The supplier has been asked to investigate the packaging process and send a corrective-action plan by October 10. This request does not establish that packaging caused the damage; it is one possible cause under review. A full inspection will determine how many units require replacement. The six defective sample units have been stored separately for further analysis.''','''十月二日收八百個連接器，抽驗八十個，其中六個針腳受損，其餘抽樣品通過外觀檢查。電性測試尚未完成。整批暫停放行，品保書面核准前不得投產。要求供應商調查包裝流程並在十月十日前交改善計畫，但這並不證明包裝是原因，只是可能原因之一。全檢後才能確定需更換數量，六個不良抽樣品另存分析。''','區分樣本與母體、外觀與電性、假設與已證實原因。',[
('數量','How many connectors were in the inspected sample?','抽驗樣本多少個？','80.~random sample of 80。','800.~800 是整批数量。','6.~6 是樣本中受損數。','74.~74 是外觀通過的樣本數。'),
('推論','Which conclusion is justified?','哪個結論合理？','The total number of defective units is not yet known.~需全檢才能定更換數，不能把樣本結果當整批實際數。','Exactly sixty units in the lot are defective.~以比例估計不能說 exactly。','Packaging has been proven to be the cause.~文章明確說未證實。','All electrically tested units passed.~電測還沒完成。'),
('行動','When may units be released to production?','什麼時候可放行投產？','After written approval from Quality.~until Quality gives written approval。','As soon as the supplier replies.~回覆不等於品保核准。','Immediately, except for the six sample units.~整批 on hold。','Automatically on October 10.~十日是計畫提交期限，不是放行日。'),
('目的','Why were six units stored separately?','六個樣品為何另存？','For further analysis.~最後一句直接指出。','To ship them to customers.~未說出貨，且是不良樣本。','To replace all eight hundred units.~六個不可能代表已更換全批，文中也沒說。','To demonstrate that the lot passed all tests.~測試未完且有不良。')])
passage('R08','資安維護公告','基礎','系統通知','''Scheduled System Maintenance
The purchasing portal will be unavailable on Saturday from 8 p.m. to 10 p.m. Local time is used throughout this notice. Orders submitted before 8 p.m. will remain in the system, but staff will not be able to view or change them during the maintenance window. Unsaved drafts may be lost, so please save your work and log out before 8 p.m.
Email and the inventory dashboard will remain available. For an urgent purchase during the outage, call the duty manager; do not send account passwords by email. The IT team will post a completion notice on the dashboard when the portal is available again. If maintenance finishes early, the portal may reopen before 10 p.m.''','''採購入口週六晚間八至十點維護，均為當地時間。八點前已提交訂單仍留存，但期間無法看或改；未儲存草稿可能遺失，八點前存檔登出。電子郵件與庫存儀表板仍可用。停機時緊急採購請打值班主管，勿透過電郵傳帳密。IT 在入口恢復時於儀表板公告，提前完成則可能十點前開放。''','remain、may、before 描述不同保證程度，不要互換。',[
('細節','Which service will remain available?','哪項服務仍可用？','The inventory dashboard.~第二段明確說保持可用。','The purchasing portal throughout maintenance.~入口維護不可用。','Editing submitted orders during maintenance.~明確說不能改。','Every company system.~文中只列兩項可用，不能擴大。'),
('細節','What may be lost?','什麼可能遺失？','Unsaved drafts.~原文限定 unsaved drafts may be lost。','All submitted orders.~已提交訂單仍在系統。','Every email.~郵件仍可用，未說遺失。','The completion notice.~未說公告會遺失。'),
('行動','What should staff do for an urgent purchase during the outage?','停機時緊急採購怎麼做？','Call the duty manager.~明確指示。','Email their password to IT.~文中禁止傳密碼。','Create an unsaved draft and close the browser.~不是公告提出的處理方法。','Wait until Monday in every case.~未規定一律等週一。'),
('推論','What is stated about reopening?','對恢復時間的敘述為何？','The portal might reopen before 10 p.m.~may reopen，可能而非保證。','It will definitely reopen at 9 p.m.~沒有九點保證。','It cannot reopen before 10 p.m.~與可提早相反。','The dashboard will be unavailable until then.~儀表板仍可用。')])
passage('R09','會議改期即時訊息','中階','對話與語意','''09:10 — Leo: Our supplier cannot join the 2 p.m. call. Could we move it to 3:30?
09:12 — Ada: I have a safety review until 3. That works for me, provided we finish by 4:15.
09:14 — Leo: We only need thirty minutes. I will send a revised invitation once Nila confirms.
09:16 — Nila: I can join remotely at 3:30, but I will not be at the office. Please include the video link.
09:18 — Ada: Good. Leo, could you also attach the latest quotation? The one in yesterday's invitation does not include freight.
09:20 — Leo: Certainly. The supplier sent a new quote this morning. Freight is listed separately, and the total is higher. I will attach that version and send the invitation now.''','''供應商無法參加下午兩點電話會議，Leo 提議三點半。Ada 三點前有安全審查，若四點十五分前結束就可。Leo 表示只需三十分鐘，待 Nila 確認才寄更新。Nila 可三點半遠端參加，請加視訊連結。Ada 請附最新報價，昨日版本不含運費。Leo 說今早新版運費另列，總額較高，將附新版並寄出邀請。''','代名詞 That 指前面提議；provided 表附帶條件。',[
('語意推理','What does Ada mean by “That works for me”?','Ada 這句話什麼意思？','The proposed time is acceptable with her stated condition.~That 指改到三點半，但須四點十五分前結束。','She has repaired the equipment.~works 此處不是設備運作。','She will work at the supplier’s office.~未提去供應商辦公室。','She approves every future meeting time.~只對此提議，不是所有未來會議。'),
('跨句推論','When would a thirty-minute call starting at 3:30 end?','三點半開始、三十分鐘的會議何時結束？','4:00 p.m.~3:30 + 30 分鐘，且在 Ada 限制前。','4:15 p.m.~這是 Ada 最晚結束要求，不是預定時長。','3:00 p.m.~這是安全審查結束。','2:30 p.m.~用了舊的兩點起始時間。'),
('細節','Why is a video link needed?','為何需要視訊連結？','Nila will join remotely.~Nila 明確說不在辦公室、遠端參加。','Ada cannot attend at 3:30.~Ada 已附條件同意。','The supplier requires a recorded presentation.~沒有此要求。','The office has permanently closed.~未提辦公室關閉。'),
('細節','How does the new quotation differ?','新報價有何不同？','Freight is listed separately and the total is higher.~Leo 最後訊息明確說明。','It removes all freight charges.~相反，新版列入。','It is identical to yesterday’s quotation.~昨日版本不含運費。','It offers a lower total price.~文中是 higher。')])
passage('R10','客服退款與替換條件','中階','雙文件','''Document A — Return policy
Unused standard items may be returned within thirty days of delivery. A return authorization number is required before shipment. Customers pay return freight unless the item is defective or we shipped the wrong model. Customized items cannot be returned for a refund, but confirmed manufacturing defects are covered by our repair-or-replacement warranty. Please contact support before sending any item back.

Document B — Customer email
We received ten customized brackets on September 21. Two have cracks, which we noticed before installation. The other eight appear fine. We would like replacements for the two damaged brackets. Attached are photographs and the order number. Please advise us on the next steps. We have not shipped anything back yet.''','''A：未使用標準品可於交貨三十日內退回，寄回前須退貨授權號。非不良或寄錯型號者由客戶負擔回程運費。客製品不可退款，但已確認製造缺陷受維修或更換保固。退回前請聯絡客服。
B：九月二十一日收十個客製支架，安裝前發現兩個裂痕，其餘八個看似正常。想換兩個受損品，已附照片及單號，請告知下一步，尚未寄回。''','客製品「不可退款」不等於「沒有維修更換保固」。',[
('跨文推論','Which policy is most relevant to the customer’s request?','客戶請求最相關的政策是什麼？','The repair-or-replacement warranty for confirmed manufacturing defects.~客製品不能一般退款，但製造缺陷可能適用保固。','Unconditional refunds for customized items.~明確不提供客製品退款。','Automatic refunds for all ten brackets.~沒這規定，且客戶只要求兩個替換。','The policy for items shipped to the wrong address.~未涉及寄錯地址。'),
('細節','How many brackets does the customer want replaced?','客戶要換幾個？','Two.~明確 two damaged brackets。','Eight.~八個看來正常。','Ten.~十個是收到總數。','Thirty.~三十是標準品退貨天數。'),
('證據界線','What has NOT yet been established by the two documents?','兩份文件還沒確立什麼？','That the cracks are confirmed manufacturing defects.~客戶觀察裂痕，不等於供應商已確認製造原因。','That the items are customized.~B 已說 customized。','That photographs were attached.~B 已說 attached photographs。','That nothing has been shipped back yet.~B 最後一句已說。'),
('下一步','What should the customer do before shipping items back?','寄回前應做什麼？','Obtain return authorization through support.~A 要求先聯絡並取得授權號，客戶已開始詢問。','Send all ten units immediately without a number.~與事前授權相反。','Demand an automatic cash refund.~客製品不適用此退款。','Install the cracked parts to prove the defect.~無此要求，不可自行補。')])
passage('C01','新人訓練段落填空','基礎','四格段落填空','''Welcome to the maintenance team. Your orientation will begin [1] 9 a.m. on Monday. Please bring photo identification. A temporary badge will be [2] at reception.
The first session covers safety procedures. [3], you will meet your supervisor for a tour of the workshop. You do not need to bring tools; all necessary equipment is provided. [4] If you have any questions about the schedule, contact Human Resources.''','''歡迎加入維護團隊。新人訓練週一九點開始。請帶照片證件，接待處會核發臨時證。第一節涵蓋安全程序，接著與主管參觀工作間，不須自備工具，所需設備均提供。插入句應承接提供的工具／設備，再接有問題可聯絡人資。''','先讀整段時間順序，句子插入看 these 指回誰。',[
('段落文法','Choose the best answer for [1].','第 1 空應填什麼？','at~具體鐘點 9 a.m. 用 at。','on~後面是鐘點，不是 Monday。','in~不配 9 a.m.。','for~不是長度或目的。'),
('段落文法','Choose the best answer for [2].','第 2 空應填什麼？','issued~will be issued 被動，證件被發給。','issuing~證件不會主動發東西。','issue~被動要過去分詞。','issuance~名詞不能構成 will be 的此被動。'),
('段落邏輯','Choose the best answer for [3].','第 3 空應填什麼？','Afterward~第一節之後再參觀，時間順序。','Nevertheless~沒有前後讓步。','Otherwise~沒有相反條件的結果。','Instead~參觀是後續，不是取代第一節。'),
('句子插入','Which sentence best fits [4]?','第 4 空插哪句最連貫？','These items must remain in the workshop after use.~These items 指剛提的工具與設備，接續使用規則。','The hotel canceled all room reservations.~未引入飯店，突然離題。','However, the applicant rejected the offer last year.~人物與時間突變。','The invoice is overdue by two months.~發票未出現，無指代。')])
passage('C02','出貨延誤段落填空','中階','四格段落填空','''Dear Ms. Lin,
We are writing about order A-62. During the final inspection yesterday, our technicians [1] a defect in one of the connectors. The affected units have been placed on hold. [2], we cannot dispatch the full order today.
We can send the unaffected units now and the remaining units after they pass inspection. There will be no [3] shipping charge for this split shipment. [4] Once we receive your reply, we will update the delivery schedule.
Sincerely,
Customer Support''','''關於 A-62 訂單：昨天最後檢驗發現連接器缺陷，受影響品暫停放行，因此今天無法整筆出貨。可先寄未受影響品，其餘待通過檢驗再寄，分批不加運費。插入句應要求客戶回覆方案，才能接收到回覆後更新時程。''','yesterday 管第一空；因此管第二空；your reply 需要前面的回覆請求。',[
('段落時態','Choose the best answer for [1].','第 1 空應填什麼？','found~yesterday 明確過去；find 的過去式 found。','find~現在式不合。','will find~未來不合。','have find~完成式也要 found，且此處有已結束時間。'),
('段落邏輯','Choose the best answer for [2].','第 2 空應填什麼？','Therefore~受影響品暫停放行，導致不能全出貨。','Nevertheless~不是克服前述障礙反而全出。','Similarly~不是列相似例子。','For example~不是舉例。'),
('段落詞性','Choose the best answer for [3].','第 3 空應填什麼？','additional~修飾 shipping charge 用形容詞。','additionally~副詞不能直接修飾名詞 charge。','addition~不是此處額外的形容詞。','add~動詞不合。'),
('句子插入','Which sentence best fits [4]?','第 4 空插哪句最連貫？','Please confirm whether this arrangement is acceptable.~提出分批後要求確認，承接下一句 your reply。','Your order was delivered in full last week.~與今天不能全寄矛盾。','We never inspect connectors.~與第一段昨天檢驗矛盾。','All customers must apply for a job online.~招聘與出貨離題。')])
(ROOT/'content/reading.json').write_text(json.dumps(sets,ensure_ascii=False,indent=2))
print('題組',len(sets),'題目',sum(len(s['questions']) for s in sets))
