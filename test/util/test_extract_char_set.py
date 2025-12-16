import os
import sys
import unittest
# Ensure repository root is on sys.path so `source` package can be imported when
# tests are executed directly.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from source.util.extract_char_set import update_xml_file, update_text_file


class TestExtractCharSet(unittest.TestCase):
    def test_update_xml_file_handles_cjk(self):
        import tempfile, os
        p = tempfile.TemporaryDirectory()
        path = os.path.join(p.name, "sample.xml")
        with open(path, "w", encoding="utf-8") as f:
            f.write("<root>hello<child>梁</child> tail</root>")

        char_set = set()
        result = update_xml_file(path, char_set)

        self.assertIn("梁", result)
        self.assertNotIn("hello", result)  # updates char_set with characters, not words

    def test_update_text_file_handles_cjk(self):
        import tempfile, os
        p = tempfile.TemporaryDirectory()
        path = os.path.join(p.name, "sample.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("abc梁def")

        char_set = set()
        result = update_text_file(path, char_set)

        self.assertIn("梁", result)
        self.assertIn("a", result)


if __name__ == "__main__":
    unittest.main()
