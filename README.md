# 職場英文練習室 / FAB English

為初學者準備的電子製造與職場英文教材。包含 3,000 個例句單字、閱讀、語句填空、文法、聽力與時態情境；網站採靜態資料，無登入、後端或執行期外部套件。

## 直接開始

- [公開網站](https://allenljf.github.io/english-learning/)
- [本機網頁](index.html)：保留同資料夾中的 `app.js`、`data.js`、`listening-audio.js`、`styles.css` 與 `docs/`。
- [完整 Markdown 全冊](docs/00-complete.md)
- [3,000 字分類索引](docs/07-vocabulary-index.md)
- [聽力策略與 100 題](docs/15-listening-practice.md)
- [YouTube 中文 TOEIC 影片資源（12 支）](docs/14-youtube-toeic-resources.md)
- [內容來源與授權](CONTENT-LICENSE.md)

若瀏覽器不方便直接開 HTML，在此資料夾執行：

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

再開 [本機學習網址](http://127.0.0.1:8765)。此網址只供自己的電腦使用；停止伺服器後即無法連線。

## 教材內容

| 內容 | 數量與範圍 |
| --- | --- |
| 單字 | 3,000 個不重複 headwords、23 類；每字附詞性、中文、搭配、英文例句與中文翻譯 |
| 閱讀 | 25 個職場閱讀題組、100 題，附文章、翻譯、答案證據與逐項解析 |
| 填空 | 100 道單句練習，另有 2 個段落填空題組；可分小組作答 |
| 文法 | 100 道練習，可依主題與小組篩選 |
| 聽力 | Parts 1–4 各 25 題；支援瀏覽器文字轉語音、重播、停止及作答後逐字稿 |
| 時態 | 5 個職場情境；每情境涵蓋 12 時態 × 主被動 × 肯定否定疑問，共 360 個變化句 |
| 動詞 | 詞庫動詞五態與 64 個常用不規則動詞 |

所有新增文章、題目、時態情境與聽力腳本均為原創教材，不是 ETS、台積電或其他企業的官方考題／錄音。公司測驗方式以招募通知為準。

## 網站操作

- 單字：搜尋英文、中文、搭配與例句；篩選分類、翻頁、遮住中文，例句仍可閱讀。
- 閱讀：選題組，先找原文證據，再看翻譯與逐項解析。
- 填空與文法：選擇小組或主題，作答後看每個選項的理由。
- 聽力：選 Part 與案例，播放或停止練習語音；逐字稿與中文在作答後顯示。瀏覽器不支援語音時仍可作答並查看逐字稿。
- 時態：選 5 個情境之一，再切換時態、語態與肯定／否定／疑問；罕見被動形式會提示。
- 教材：可閱讀章節、下載 Markdown 全冊與分冊。

答題紀錄只留在當次頁面記憶體；重新整理會清除紀錄。首次選擇後鎖定該題，「重做這組題目」會清除該組答案。計分只供自學，不換算 TOEIC 成績。

## 編輯與重新產生

`content/` 保存來源資料；`tools/build.py` 由這些固定資料產生 `data.js`、Markdown 分冊、完整全冊與 `english-study-pack.zip`。題庫 JSON 是內容來源，請直接編輯 `content/questions.json`、`content/reading.json`、`content/listening.json`，不要只改生成檔。

```bash
python3 tools/build.py
python3 -m unittest tests.test_learning_content -v
node --test tests/listening-audio.test.js
python3 tools/validate.py
node --check app.js
node --check data.js
```

## 來源與界線

補充單字以 wordfreq 頻率資料選取，中文釋義參照 ECDICT 並轉為繁體；授權與來源詳見 [內容來源與授權](CONTENT-LICENSE.md)。本教材不宣稱詞彙是任何公司的統計高頻詞，也不提供官方考試分數預測。
