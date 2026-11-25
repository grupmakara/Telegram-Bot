import json, os, sys, tempfile, unittest
from unittest import mock
sys.path.insert(0, os.path.dirname(__file__))
import synth


class SynthTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.item = {"key": "abc", "text": "Merhaba", "voice": "tr-TR-AhmetNeural", "pitch": "+0Hz", "rate": "+0%"}

    def test_skips_cached(self):
        for ext in ("mp3", "json"):
            open(os.path.join(self.d, f"abc.{ext}"), "w").write("{}")
        with mock.patch.object(synth, "synth_one") as m:
            synth.run({"items": [self.item], "outDir": self.d})
            m.assert_not_called()

    def test_retries_then_fails(self):
        with mock.patch.object(synth, "synth_one", side_effect=RuntimeError("ağ yok")) as m, \
             mock.patch.object(synth.time, "sleep"):
            with self.assertRaises(SystemExit) as cm:
                synth.run({"items": [self.item], "outDir": self.d})
            self.assertEqual(cm.exception.code, 1)
            self.assertEqual(m.call_count, 3)

    def test_words_from_boundaries(self):
        chunks = [{"type": "WordBoundary", "offset": 1_000_000, "duration": 5_000_000, "text": "Merhaba"}]
        self.assertEqual(synth.words_from(chunks), [{"text": "Merhaba", "startMs": 100, "endMs": 600}])


if __name__ == "__main__":
    unittest.main()
