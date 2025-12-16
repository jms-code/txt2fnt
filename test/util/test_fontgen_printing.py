import io
import sys
import os
import tempfile
import unittest

from source.util import fontgen


class TestFontgenPrinting(unittest.TestCase):
    def test_use_fontgen_no_fontgen_folder_with_cp1252_stdout(self):
        # Simulate a cp1252 stdout that would raise on emoji printing
        original_stdout = sys.stdout
        buf = io.BytesIO()
        # TextIOWrapper with strict errors to replicate the crash behavior
        sys.stdout = io.TextIOWrapper(buf, encoding='cp1252', errors='strict')
        try:
            # Point fontgen.folder to a temp non-existent folder
            original_folder = fontgen.fontgen_folder
            fontgen.fontgen_folder = os.path.join(tempfile.gettempdir(), 'nonexistent_fontgen_folder_12345')
            # Call use_fontgen which will attempt to print emoji warnings and return False
            ok = fontgen.use_fontgen(char_chunk_file='doesnotmatter', ttf_file='foo.ttf')
            self.assertFalse(ok)
        finally:
            # restore state
            fontgen.fontgen_folder = original_folder
            sys.stdout.flush()
            sys.stdout = original_stdout


if __name__ == '__main__':
    unittest.main()
