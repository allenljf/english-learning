# Study Library Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Expand the static English study site to 3,000 example-based vocabulary entries, 100 questions in each existing learning theme, five tense scenarios, and 100 listening practice cases.

**Architecture:** Keep `content/` as the source of truth and generate `data.js`, Markdown books, and the complete study pack from the existing Python build. Extend the existing SPA with a listening route and scenario selectors; use browser speech synthesis with transcript fallback, and keep all data and scoring client-side.

**Tech Stack:** HTML, CSS, vanilla JavaScript, Python 3 standard library, JSON, Markdown.

**Spec:** `docs/superpowers/specs/2026-10-08-study-library-expansion-design.md`

## Global Constraints

- Grow the bank from 1,139 to exactly 3,000 unique headwords, adding 1,861 unique entries.
- Every headword must have a part of speech, Traditional Chinese meaning, a common collocation, one natural English example sentence, and a Traditional Chinese translation of that example.
- Each theme must expose at least 100 individually answerable practice questions with four choices, one answer, Chinese translation, a reason for each option, and a short learning tip.
- Add 100 original listening cases, balanced at 25 per part.
- Use the browser's built-in English speech synthesis for playback; if unavailable, provide a clear transcript fallback.
- Keep static runtime assets and avoid adding runtime libraries or external API dependencies.
- All added questions and examples are original teaching material, not official TOEIC or company test questions.

## Review Focus

1. Duplicate headwords differing only by case or repeated across existing and added source files must still count once, without dropping a valid sense.
2. Vocabulary examples must be a complete sentence that demonstrates the displayed sense and whose Traditional Chinese translation matches.
3. Four-choice questions must have four distinct options, exactly one indexed answer, and explanations aligned to all options.
4. Tense scenarios need transitive actions and context cues that keep every generated sentence grammatical; rare passive forms retain the existing warning.
5. Speech synthesis can be absent or interrupted; answer choice must remain usable and transcript fallback must not falsely claim audio played.

---

### Task 1: Expand and display the 3,000-word example bank

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/test_learning_content.py`
- Create: `tools/content_contracts.py`
- Create: `content/vocabulary-extra.json` (1,861 added entries)
- Create: `content/vocabulary-examples.json` (examples for the existing 1,139 unique headwords)
- Modify: `tools/build.py`
- Modify: `app.js`
- Modify: `tools/validate.py`
- Generated: `content/vocabulary.json`, `data.js`, `docs/07-vocabulary-index.md`, `docs/vocabulary/*.md`, `docs/00-complete.md`

**Interfaces:**
- `tools/content_contracts.py` exposes `find_contract_violations(root: pathlib.Path) -> list[str]`; it reads generated `content/*.json` after `tools/build.py`.
- `tools/validate.py` exits nonzero and prints every returned violation; `tests/test_learning_content.py` calls the same function and asserts the returned list is empty.
- Vocabulary examples use `example` and `exampleZh` string fields on each generated headword.
- Each added entry is `{word, category, senses:[{pos, zh, phrase}], example, exampleZh}`; categories must match the existing category names.
- Existing headword examples are keyed by the exact normalized `word` string and contain `{example, exampleZh}`.
- Generated vocabulary items retain `id`, `word`, `category`, `categories`, `senses`, and optional verb `forms`, and add `example` and `exampleZh`.

- [x] **Step 1: Write failing tests that require exactly 3,000 case-insensitive unique headwords and nonempty `example`/`exampleZh` fields, with each example containing the headword or one of its recorded verb forms.**
- [x] **Step 2: Run `python3 -m unittest tests.test_learning_content -v` and confirm it fails because the content-contract module does not exist yet.**
- [x] **Step 3: Implement `find_contract_violations(root: pathlib.Path) -> list[str]` for the vocabulary requirements and call it from `tools/validate.py`; run tests to see the current word count/example violations explicitly.**
- [x] **Step 4: Populate examples for existing headwords and add 1,861 new curated entries across the established TOEIC/workplace/manufacturing categories.** Check every new headword against the existing word set case-insensitively before keeping it; use natural beginner-appropriate sentences and matching Traditional Chinese translations.
- [x] **Step 5: Extend `tools/build.py` to merge added entries without inflating counts for inflections or duplicate senses, attach examples, and emit examples in vocabulary cards' source Markdown books.**
- [x] **Step 6: Update `app.js` vocabulary cards and search to show example/translation while preserving pagination, category filtering, and hide-meaning behavior.**
- [x] **Step 7: Run `python3 -m unittest tests.test_learning_content -v` and `python3 tools/validate.py`; confirm exactly 3,000 unique headwords and complete examples.**
- [x] **Step 8: Manually verify the vocabulary UI: an English example and Chinese translation appear on cards, example search works, hiding meanings leaves the English example available, and pagination/category filters still work.**
- [x] **Step 9: Commit as `feat: expand vocabulary bank to 3000 exampled words`.**

### Task 2: Bring reading, cloze, and grammar practice to 100 items each

**Files:**
- Modify: `content/questions.json` (add 64 cloze and 64 grammar items)
- Modify: `content/reading.json` (add 15 reading sets × 4 questions)
- Modify: `app.js`
- Modify: `tools/build.py`
- Generated: `docs/10-cloze-practice.md`, `docs/11-grammar-practice.md`, `docs/12-reading-practice.md`, `docs/00-complete.md`, `data.js`

**Interfaces:**
- Reuse the current question fields: `id`, `kind`/`topic`, `stem`, `zh`, `options`, `answer`, `reasons`, and `tip`.
- Add a `set` label to every single-sentence cloze and grammar item; no session group contains more than 10 items.
- Reading sets retain `id`, `title`, `level`, `genre`, `text`, `zh`, `strategy`, and four `questions`.
- Keep reading IDs sequential after the existing R10 sets; keep question IDs globally unique across all datasets.

- [x] **Step 1: Add failing tests asserting at least 100 reading, 100 single-sentence cloze, and 100 grammar questions, complete per-option explanations, and no more than 10 questions in any single-sentence practice group.**
- [x] **Step 2: Run those tests and confirm the count assertions fail on the current datasets.**
- [x] **Step 3: Author 64 new cloze items, 64 new grammar items, and 15 original reading sets with four evidence-based questions each.** Ensure answer distractors are distinct, each option has an accurate reason, and the reading answer is supported by its passage.
- [x] **Step 4: Update practice selection so each theme has manageable groups while exposing all questions; keep the existing topic filters and reading evidence/translation layout.** Add a session selector for the `set` labels and retain first-answer scoring/reset behavior.
- [x] **Step 5: Update home and theme counts to derive from data rather than fixed numbers.**
- [x] **Step 6: Run question tests and `python3 tools/validate.py`; confirm the three themes each meet 100 and all question IDs/answer records validate.** Manually answer, change set, and reset one session in each theme.
- [x] **Step 7: Commit as `feat: add 100-item reading cloze and grammar practice`.**

### Task 3: Add five selectable tense scenarios

**Files:**
- Create: `content/tense-scenarios.json`
- Modify: `tools/build_transformations.py`
- Modify: `app.js`
- Modify: `tools/validate.py`
- Generated: `content/tenses.json`, `docs/05-transformations.md`, `docs/00-complete.md`, `data.js`

**Interfaces:**
- A scenario has a stable `id`, a Chinese/English label, an actor, a transitive base action with authored verb forms, an object, and context cues for the 12 existing tense definitions.
- Each action supplies `base`, `thirdPerson`, `past`, `pastParticiple`, and `ing` forms; each scenario supplies one context cue for each of the 12 tenses.
- The build exposes five scenarios in `data.js`; each scenario contains 12 tense entries with three active and three passive forms. The app renders the selected scenario using the existing voice and polarity controls.

- [x] **Step 1: Add failing tests for five scenarios and 12 × 2 × 3 generated forms per scenario, including sentence-ending punctuation and required time cues.**
- [x] **Step 2: Run the tests and confirm they fail because only the original single sensor scenario exists.**
- [x] **Step 3: Add four transitive workplace/manufacturing cases alongside the sensor check; include authored forms/time cues so no runtime conjugation guesses are needed.**
- [x] **Step 4: Generate scenario-specific tense matrices while retaining the original formulas, usage notes, and rare-passive warnings.**
- [x] **Step 5: Add the scenario selector and display the selected actor/object context in the tense lab.**
- [x] **Step 6: Run the tense tests and validator; manually inspect one regular, one continuous, one perfect, and one rare passive scenario.**
- [x] **Step 7: Commit as `feat: add five tense lab scenarios`.**

### Task 4: Add listening strategy and 100 playable cases

**Files:**
- Create: `content/listening.json`
- Create: `listening-audio.js`
- Create: `tests/listening-audio.test.js`
- Modify: `index.html`
- Modify: `app.js`
- Modify: `styles.css`
- Modify: `tools/build.py`
- Modify: `tools/validate.py`
- Generated: `data.js`, `docs/15-listening-practice.md`, `docs/00-complete.md`

**Interfaces:**
- Each case is `{id, part, scene, segments, stem, zh, options, answer, reasons, tip}`. `segments` is an ordered array of `{speaker, kind, text}` strings used by speech playback and transcript reveal; `kind` is `prompt`, `dialogue`, `announcement`, or `choice`.
- Part 1 cases have a scene cue and four spoken descriptions; Part 2 cases have a spoken question and four spoken responses; Parts 3–4 have a short spoken conversation/announcement and a printed question with four printed choices.
- Listening cases participate in global answer scoring through the existing question interface. `listening-audio.js` exposes `createSpeechController({synthesis, Utterance, onStatus})`, returning `isSupported()`, `play(segments, rate = 0.85)`, and `stop()`; tests use injected fake browser speech APIs without external files.

- [x] **Step 1: Add failing tests for 100 cases, exactly 25 per part, case schema, choice/explanation integrity, and `createSpeechController` support, ordered playback, interruption, and stop behavior.**
- [x] **Step 2: Run `node --test tests/listening-audio.test.js` and the content tests; confirm failures identify the absent audio controller/data.**
- [x] **Step 3: Author 100 original cases balanced across Parts 1–4, with beginner-facing Traditional Chinese strategy notes, translations, option explanations, and tips.**
- [x] **Step 4: Add listening data to the generated `data.js` and global question map/score without changing existing question IDs.**
- [x] **Step 5: Add the listening navigation entry, strategy tab, part filters, playable case UI, repeat/stop controls, post-answer transcript/translation reveal, and unsupported-speech fallback.** Cancel active speech when the learner changes cases or leaves the route.
- [x] **Step 6: Run the audio unit tests and content validator; manually test a case from each part in a browser and simulate unsupported speech synthesis to verify the fallback.**
- [x] **Step 7: Commit as `feat: add listening strategy and 100 practice cases`.**

### Task 5: Refresh generated deliverables and verify the published path

**Files:**
- Modify: `README.md`, `VERIFICATION.md`
- Generated: `data.js`, `docs/00-complete.md`, `docs/07-vocabulary-index.md`, `docs/10-cloze-practice.md`, `docs/11-grammar-practice.md`, `docs/12-reading-practice.md`, `docs/15-listening-practice.md`, `english-study-pack.zip`
- Verify: `index.html`, `app.js`, `styles.css`, GitHub Pages project path

**Interfaces:**
- `tools/build.py` remains the single command that regenerates all derived files and the downloadable pack.
- The deployed site remains rooted at `https://allenljf.github.io/english-learning/`; internal CSS, script, Markdown, and download links stay relative to that project path.

- [x] **Step 1: Add failing checks for the README/verification counts, generated listening Markdown, all vocabulary examples in the full book, and valid internal relative links under the project path.**
- [x] **Step 2: Run the checks and confirm they identify stale generated totals/artifacts.**
- [x] **Step 3: Update README and verification summaries from actual generated counts; extend `tools/build.py` to regenerate the full book, article registry, vocabulary books, practice books, listening book, and ZIP from an explicit file manifest.**
- [x] **Step 4: Run `python3 tools/build.py`, `python3 -m unittest tests.test_learning_content -v`, `python3 tools/validate.py`, `node --check app.js`, and `node --check data.js`.**
- [x] **Step 5: Verify with a fresh browser session at the GitHub Pages project path: all four themes load, 3,000 vocabulary entries are searchable, all question types answer/reset, five tense scenarios switch, listening cases play/fallback, and no JavaScript errors appear.**
- [x] **Step 6: Commit as `docs: refresh study pack counts and verification`.**
- [x] **Step 7: The user has already authorized commit, push, and GitHub Pages deployment; commit the completed feature, fast-forward `main`, push, and verify the published project path.**
