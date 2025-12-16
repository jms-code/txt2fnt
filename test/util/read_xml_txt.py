import os
import sys
import unittest
# Ensure repository root is on sys.path so `source` package can be imported when
# tests are executed directly.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from source.util.read_xml_txt import read_xml_texts_from_string


class TestReadXmlLeftTxt(unittest.TestCase):
    def test_simple(self):
        xml = """
        <root>
            <a>hello</a>
            <b>world</b>
        </root>
        """
        self.assertEqual(read_xml_texts_from_string(xml), ["hello", "world"])

    def test_nested_and_tail(self):
        xml = """
        <root>
            <a>hello<b>inner</b> tail</a>
        </root>
        """
        self.assertEqual(read_xml_texts_from_string(xml), ["hello", "inner", "tail"])

    def test_attributes_ignored(self):
        xml = """
        <root>
            <a attr="value">text</a>
            <b attr="x"/>
        </root>
        """
        self.assertEqual(read_xml_texts_from_string(xml), ["text"])

    def test_cdata(self):
        xml = """
        <root><![CDATA[this is <cdata> & special]]></root>
        """
        self.assertEqual(read_xml_texts_from_string(xml), ["this is <cdata> & special"])

    def test_whitespace(self):
        xml = """
        <root>
            <a>   lots of whitespace   </a>
            <b>\n\ttrimmed\t\n</b>
        </root>
        """
        self.assertEqual(read_xml_texts_from_string(xml), ["lots of whitespace", "trimmed"])

    def test_malformed_xml_fallback(self):
        import tempfile, os
        p = tempfile.TemporaryDirectory()
        path = os.path.join(p.name, "bad.xml")
        # unescaped & will cause a ParseError in strict XML parsers
        with open(path, "w", encoding="utf-8") as f:
            f.write("<root>hello & world<child>more & things</child></root>")

        with open(path, "r", encoding="utf-8") as f:
            xml_content = f.read()
        texts = read_xml_texts_from_string(xml_content)
        # Fallback should still extract the visible text chunks in order
        self.assertEqual(texts, ["hello & world", "more & things"])

if __name__ == "__main__":
    unittest.main()
