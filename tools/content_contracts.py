"""Cross-file contracts for the generated learning material."""
from __future__ import annotations

import json
import pathlib
import re
from collections import Counter


def find_contract_violations(root: pathlib.Path) -> list[str]:
    """Return user-readable content errors without stopping at the first one."""
    root = pathlib.Path(root)
    problems: list[str] = []

    def read(name: str, default):
        try:
            return json.loads((root / "content" / name).read_text())
        except (OSError, json.JSONDecodeError) as exc:
            problems.append(f"content/{name}: cannot read JSON ({exc})")
            return default

    words = read("vocabulary.json", [])
    normalized = [str(w.get("word", "")).casefold() for w in words]
    if len(words) != 3000:
        problems.append(f"Vocabulary must contain exactly 3,000 headwords; found {len(words)}.")
    if len(set(normalized)) != len(words):
        problems.append("Vocabulary contains duplicate headwords ignoring case.")
    forms_by_word = {w.get("word", "").casefold(): w.get("forms", []) for w in words}
    for word in words:
        label = word.get("word", "(missing word)")
        if not word.get("example", "").strip() or not word.get("exampleZh", "").strip():
            problems.append(f"{label}: English example and Traditional Chinese translation are required.")
        if word.get("example") and not word["example"].strip().endswith((".", "?", "!")):
            problems.append(f"{label}: English example must be a complete punctuated sentence.")
        if word.get("exampleZh") and not re.search(r"[\u3400-\u9fff]", word["exampleZh"]):
            problems.append(f"{label}: example translation must contain Chinese text.")
        forms = [label, *forms_by_word.get(label.casefold(), [])]
        if word.get("example") and not any(re.search(rf"\b{re.escape(str(form))}\b", word["example"], re.I) for form in forms if form):
            problems.append(f"{label}: example must use the headword or one of its recorded verb forms.")
        if not word.get("senses") or not word.get("category") or not word.get("categories"):
            problems.append(f"{label}: category and at least one sense are required.")

    questions = read("questions.json", [])
    reading = read("reading.json", [])
    all_q = questions + [q for passage in reading for q in passage.get("questions", [])]
    counts = Counter(q.get("kind") for q in questions)
    counts["閱讀"] = sum(len(p.get("questions", [])) for p in reading if p.get("id", "").startswith("R"))
    for kind, minimum in (("填空", 100), ("文法", 100), ("閱讀", 100)):
        if counts[kind] < minimum:
            problems.append(f"{kind} must have at least {minimum} questions; found {counts[kind]}.")
    for q in all_q:
        if len(q.get("options", [])) != 4 or len(set(q.get("options", []))) != 4:
            problems.append(f"{q.get('id')}: exactly four distinct choices are required.")
        if len(q.get("reasons", [])) != 4:
            problems.append(f"{q.get('id')}: each choice needs its own explanation.")
        if not isinstance(q.get("answer"), int) or not 0 <= q["answer"] < 4:
            problems.append(f"{q.get('id')}: answer must be an index from 0 to 3.")
        if not q.get("zh") or not q.get("tip"):
            problems.append(f"{q.get('id')}: translation and learning tip are required.")
    groups = Counter(q.get("set", "(ungrouped)") for q in questions if q.get("kind") in {"填空", "文法"})
    for name, size in groups.items():
        if size > 10:
            problems.append(f"Practice group {name} has {size} items; groups may contain at most 10.")

    scenarios = read("tense-scenarios.json", [])
    if len(scenarios) != 5:
        problems.append(f"Tense lab must define exactly five scenarios; found {len(scenarios)}.")
    for scenario in scenarios:
        if len(scenario.get("cues", [])) != 12:
            problems.append(f"Tense scenario {scenario.get('id')} must have 12 context cues.")

    listening = read("listening.json", [])
    ids = [q.get("id") for q in all_q + listening]
    if len(ids) != len(set(ids)):
        problems.append("Question IDs must be unique across all themes.")
    parts = Counter(item.get("part") for item in listening)
    if len(listening) != 100 or any(parts[p] != 25 for p in range(1, 5)):
        problems.append(f"Listening must contain 100 cases (25 per part); found {len(listening)} ({dict(parts)}).")
    for q in listening:
        if len(q.get("options", [])) != 4 or len(set(q.get("options", []))) != 4 or len(q.get("reasons", [])) != 4:
            problems.append(f"{q.get('id')}: listening requires four distinct choices and four explanations.")
        if not q.get("segments") or not q.get("scene") or not q.get("tip"):
            problems.append(f"{q.get('id')}: listening scene, audio segments, and tip are required.")
    return problems
