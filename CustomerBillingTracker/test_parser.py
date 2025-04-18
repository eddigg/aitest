
import unittest
from main import IntentParser

class TestIntentParser(unittest.TestCase):
    def setUp(self):
        self.parser = IntentParser()

    def test_schedule_intent(self):
        result = self.parser.parse_intent("Schedule a meeting at 3 PM")
        self.assertEqual(result["action"], "schedule")
        self.assertEqual(result["time"], "15:00")
        self.assertGreater(result["confidence"], 0.8)

    def test_unknown_intent(self):
        result = self.parser.parse_intent("Random text")
        self.assertEqual(result["action"], "unknown")
        self.assertLess(result["confidence"], 0.8)

if __name__ == '__main__':
    unittest.main()
