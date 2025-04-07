import unittest
from prompt_tracking_package.tracker import PromptTracker

class TestPromptTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = PromptTracker()

    def test_track(self):
        self.tracker.track("Hello, how are you?")
        self.assertGreater(len(self.tracker.data), 0)
        self.assertEqual(self.tracker.data.iloc[-1]["prompt"], "Hello, how are you?")

if __name__ == "__main__":
    unittest.main()
