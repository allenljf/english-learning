import json
import pathlib
import unittest

from tools.content_contracts import find_contract_violations

ROOT = pathlib.Path(__file__).resolve().parents[1]


class LearningContentContracts(unittest.TestCase):
    def test_vocabulary_count_and_examples(self):
        words = json.loads((ROOT / "content/vocabulary.json").read_text())
        self.assertEqual(len(words), 3000)
        self.assertEqual(len({word["word"].casefold() for word in words}), 3000)
        for word in words:
            self.assertTrue(word.get("example"), word["word"])
            self.assertTrue(word.get("exampleZh"), word["word"])
            forms = [word["word"], *word.get("forms", [])]
            self.assertTrue(any(form.lower() in word["example"].lower() for form in forms), word["word"])

    def test_all_content_contracts(self):
        self.assertEqual(find_contract_violations(ROOT), [])

    def test_scenario_matrix_covers_all_forms(self):
        scenarios = json.loads((ROOT / "content/tense-scenarios.json").read_text())
        self.assertEqual(len(scenarios), 5)
        for scenario in scenarios:
            self.assertEqual(len(scenario["tenses"]), 12)
            for tense in scenario["tenses"]:
                for voice in ("active", "passive"):
                    self.assertEqual(len(tense[voice]), 3)
                    self.assertTrue(all(item.endswith((".", "?")) for item in tense[voice]))


if __name__ == "__main__":
    unittest.main()
