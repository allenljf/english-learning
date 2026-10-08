# Study library expansion design

## Goal

Expand the published workplace-English study site while keeping it static, self-contained, useful to beginners, and compatible with its GitHub Pages deployment. The work adds a 3,000-word example-based bank, at least 100 questions in each existing learning theme, five selectable tense scenarios, and a listening skills section with 100 practice cases.

## Current baseline

- `content/vocabulary.txt` contains vocabulary source rows; `tools/build.py` merges them into 1,139 unique headwords and emits `data.js` and Markdown vocabulary books.
- Vocabulary cards show definitions, parts of speech, collocations, and verb forms, but no per-headword example sentence.
- `content/questions.json` has 36 fill-in questions and 36 grammar questions. `content/reading.json` has 40 reading questions and 8 passage fill-in questions.
- The tense lab uses one sensor-checking scenario across 12 tenses, active/passive voice, and affirmative/negative/question forms.
- The app has no listening route or listening dataset.
- The deployed application is a static GitHub Pages site; scoring state is local to the current page session.

## Approved direction

Keep the app static and retain the current data-generation workflow. Store authored learning material in `content/`, generate the browser data and Markdown learning books from those sources, and preserve the existing navigation and visual system while adding the new listening theme.

All added questions and examples are original teaching material, not official TOEIC or company test questions. Vocabulary counts are unique base headwords; inflections do not count as separate words.

## Vocabulary bank

- Grow the bank from 1,139 to exactly 3,000 unique headwords, adding 1,861 unique entries.
- Keep the existing 23 context categories unless coverage review shows a clear reason to add categories; additions should cover general TOEIC, business, workplace, manufacturing, and electronics contexts.
- Every headword must have a part of speech, Traditional Chinese meaning, a common collocation, one natural English example sentence, and a Traditional Chinese translation of that example.
- The example must demonstrate the headword in a suitable inflected form and match the displayed sense. Multiple senses remain attached to one headword; examples should clarify the primary selected sense.
- Vocabulary cards and Markdown books must show the example and translation. Search should include example text, and the existing pagination and meaning-hide behavior should continue to work.

## Three learning themes

Each theme must expose at least 100 individually answerable practice questions with four choices, one answer, Chinese translation, a reason for each option, and a short learning tip.

- **Reading:** at least 100 questions across workplace messages and multi-document reading sets. Preserve evidence-based explanations and show the relevant text in each practice set.
- **Sentence and vocabulary cloze:** at least 100 single-sentence cloze questions, in addition to the existing passage cloze sets. Retain topic filters and explanations.
- **Grammar:** at least 100 grammar questions, retaining topic filters and explanations.

Present these questions in selectable practice groups so a learner can choose a manageable session. IDs must remain unique across all question types, and the home page and theme pages must show current counts.

## Tense lab

Add five selectable workplace/manufacturing scenarios. Each scenario supplies an actor, a transitive action, an object, and suitable time/context cues so it can be rendered through the existing 12 tense × active/passive × affirmative/negative/interrogative matrix. Keep the existing formula notes and warnings for rare or unnatural passive combinations. The current sensor-check scenario remains one of the five.

## Listening learning theme

- Add a navigation entry and a learning page with beginner-friendly answer strategies for TOEIC Listening Parts 1–4.
- Add 100 original cases, balanced at 25 per part. Each case has listening speech text, a prompt, four distinct choices, one answer, Chinese translation, per-choice explanations, and a tip. Part 1 cases include a scene cue; Parts 2–4 use short spoken prompts or dialogues.
- Use the browser's built-in English speech synthesis for playback, with repeat and stop controls and a conservative default rate. Keep transcripts and translations hidden until the learner asks to reveal them after answering.
- If speech synthesis is unavailable, provide a clear transcript fallback. Label the generated voice as practice playback, not authentic TOEIC audio or accent training.
- Listening scoring follows the app's existing in-session scoring behavior; no backend, account, or persistent cross-device progress is added.

## Data, build, and delivery

- Keep static runtime assets and avoid adding runtime libraries or external API dependencies.
- Extend the source data and `tools/build.py` so `data.js`, vocabulary books, question books, the complete Markdown book, README counts, verification notes, and the downloadable ZIP agree.
- Add a content validation test for the 3,000 unique headwords and complete examples; minimum question counts by theme; listening part balance and schema; five tense scenarios; and unique IDs/valid answer indexes.
- Keep all internal links valid and the GitHub Pages project-site paths working under `/english-learning/`.

## Acceptance criteria

1. The generated site displays exactly 3,000 unique vocabulary headwords, and every word card has a usable English example plus Traditional Chinese translation.
2. Reading, cloze, and grammar each provide at least 100 answerable items with their complete explanations; no IDs collide.
3. The tense lab lets the learner select five scenarios and render each across the current tense/voice/polarity controls.
4. The listening page teaches strategies and provides 100 playable cases, 25 for each TOEIC listening part; answers reveal transcript, translation, and explanations, and unsupported speech synthesis has a usable fallback.
5. Generated Markdown, full book, ZIP, navigation, counts, and public-path links agree with the browser data.
6. The repository validation command passes, JavaScript syntax checks pass, and a fresh browser check confirms vocabulary, all four learning themes, five tense scenarios, and the GitHub Pages base path.

## Out of scope

- Firebase, user accounts, remote storage, or cross-device progress.
- Official TOEIC recordings or copied company test questions.
- Publishing to another host or changing the GitHub repository's visibility.
