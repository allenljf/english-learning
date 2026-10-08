# 驗證紀錄

驗證日期：2026-10-08。

## 內容與交付物

- `python3 tools/build.py` 成功產生網站資料、分冊、完整全冊與下載 ZIP。
- `python3 -m unittest tests.test_learning_content -v` 通過；確認 3,000 個不重複 headwords 都有英文例句與中文翻譯、100 題閱讀、100 題單句填空、100 題文法、Parts 1–4 各 25 題，以及五組完整時態矩陣。
- `node --test tests/listening-audio.test.js` 通過；涵蓋瀏覽器不支援、依序播放、停止、中斷重播與語音錯誤狀態。
- `node --check app.js`、`node --check listening-audio.js`、`node --check data.js` 通過。
- `python3 tools/validate.py` 通過；核對題號、選項解析、分組大小、文章內連結與靜態依賴。
- `git diff --check` 與 `unzip -t english-study-pack.zip` 通過。
- 本機 HTTP 與 DOM smoke test 通過，包括根目錄與模擬 GitHub Pages `/english-learning/` 專案子路徑：首頁、單字搜尋／遮中文、閱讀作答、分組填空、時態情境切換、聽力播放狀態與作答後逐字稿均可載入；以模擬語音 API 執行時沒有 JavaScript 錯誤。

## 內容界線

自動檢查能確認資料完整與結構一致，不等於逐字語言編輯。題目與例句為教材情境，不是 ETS 或公司官方考題。瀏覽器的實際英文語音由使用者裝置提供；不支援時仍能作答並查看逐字稿。
