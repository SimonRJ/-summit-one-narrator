import copy
from itertools import permutations
import json
import unittest

from score import HERE, VERDICTS, evaluate, read_json, unique_keys, validate


class ReviewerBenchmark(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.key = read_json(HERE / "key.json")

    def test_blind_packet_and_key_agree(self):
        cases = read_json(HERE / "packet.json")["cases"]
        ids = [case["id"] for case in cases]
        self.assertEqual(len(ids), len(set(ids)))
        for case in cases:
            self.assertEqual(set(case), {"id", "material"})
            self.assertTrue(case["material"].strip())
        validate(self.key, set(ids))
        self.assertEqual({item["verdict"] for item in self.key.values()}, VERDICTS)
        self.assertEqual(sum(item["verdict"] == "ready" for item in self.key.values()), 4)
        counts, differences = evaluate(self.key, self.key)
        self.assertEqual((counts["exact"], differences), (8, []))

    def test_misses_false_alarms_and_misclassified_defects(self):
        response = copy.deepcopy(self.key)
        response["M52"]["verdict"] = "ready"
        response["M67"]["verdict"] = "unclear"
        response["M46"]["verdict"] = "repeat"
        counts, differences = evaluate(self.key, response)
        self.assertEqual(counts, {"exact": 5, "detected": 3, "misses": 1, "false_alarms": 1, "wrong_category": 1})
        self.assertEqual(set(differences), {"M46", "M52", "M67"})

    def test_invalid_reports_fail(self):
        for invalid in [{}, [], {"made-up": {}}, {**self.key, "M14": {"verdict": [], "reason": "x"}},
                        {**self.key, "M14": {"verdict": "unclear", "reason": " "}}]:
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                evaluate(self.key, invalid)
        with self.assertRaises(ValueError):
            json.loads('{"M14":1,"M14":2}', object_pairs_hook=unique_keys)

    def test_arrangement_examples_by_enumeration(self):
        distances = [abs(order.index(0) - order.index(1)) for order in permutations(range(6))]
        self.assertEqual((distances.count(1), distances.count(2)), (240, 192))
        talks = [order for order in permutations("ABCD") if order.index("A") < order.index("B")
                 and order.index("D") == order.index("C") + 1]
        self.assertEqual(len(talks), 3)


if __name__ == "__main__":
    unittest.main()
