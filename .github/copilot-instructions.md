This repository is small and script-oriented. The goal is to convert text and TTF inputs into font assets using an external `fontgen` tool. The instructions below help an AI coding agent become productive quickly.

- **Start here**: read `txt2fnt.py`, `txt2fnt_gui.py`, and `build_dist.py` to understand the entry points and distribution steps.
- **Key directories**:
  - `in/` — input files: `ttf/`, `text/`, and `config/` presets used by the tools.
  - `_tools_/` — contains `fontgen` binaries and wrappers; these are required but must be downloaded manually.
  - `source/` — code under active development; `source/util/` holds helpers like `extract_char_set.py`, `fontgen.py`, and `read_xml_txt.py`.

- **Big picture / data flow**:
   1. TTF fonts are placed in `in/ttf/`.
   2. Text inputs (plain text or XML fragments) are in `in/text/`.
 3. Helper modules in `source/util` extract characters from text and produce character sets.
 4. `_tools_/fontgen` is invoked to create MSDF / bitmap font artifacts; `build_dist.py` copies `_tools_` and `config` into `dist/` for packaging.

**Project-specific conventions**:
  - Files are UTF-8 encoded; always open files with `encoding='utf-8'`.
  - The codebase prefers small, focused utility functions in `source/util` rather than large object hierarchies.
  - Tests (when added) live under `test/` and follow the existing pattern of inserting the repo root into `sys.path` so they can be executed directly (see `test/util/read_xml_txt.py`).

**Testing / running**:
  - Run a specific test file directly: `python test/util/read_xml_txt.py -v`.
  - Or run unittest discovery from project root (ensure `source` is importable):

```bash
python -m unittest discover -s test -p "test_*.py"
```

**When editing/parsing XML**:
  - Use `xml.etree.ElementTree` for simple, dependency-free parsing (see `source/util/read_xml_txt.py`).
  - Preserve document order: collect `element.text` and `element.tail` and strip whitespace; skip empty strings.

- **Build and packaging notes**:
  - `build_dist.py` prepares a minimal `dist/` by copying `_tools_` and `config`.
  - `fontgen` binaries are not checked into the repo. The README documents how to obtain them manually.

**Where to change behavior**:
  - To change how character sets are extracted and saved, modify `source/util/extract_char_set.py` (functions: `update_text_file`, `update_xml_file`, `split_char_set`, `save_char_set`).
  - To change XML text extraction, edit `source/util/read_xml_txt.py` (there is a unit test demonstrating expected behavior in `test/util/read_xml_txt.py`).

- **Helpful implementation tips for AI helpers**:
  - Keep changes small and focused (this repo favors simple utilities).
  - Add unit tests next to the utility, keep them runnable directly by adding the `ROOT` sys.path insertion shown in existing tests.
  - Respect UTF-8 and explicit encodings when reading/writing files.

If anything here is unclear or you'd like more examples (e.g., how `fontgen` is invoked from a script or how to build a `dist/` package), tell me which area to expand and I will iterate.
