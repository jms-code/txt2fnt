# txt2fnt

A tool to convert text files to bitmap font files using fontgen.exe
All text files under in/text/ are processed to extract unique characters, which are then used to generate bitmap fonts. For xml files, only the text content is considered, any tags or attributes are ignored.
Some characters are always included like ASCII letters and digits, may support additional config later.




## manually download dependencies before running

### folder: `_tools_`

1. fontgen.exe and its dependencies
  ([Fontgen V1.1.0](https://github.com/Yanrishatum/fontgen/releases/tag/1.1.0))

### folder: `in\ttf`

1. Place your desired TTF font files in the `in/ttf/` folder.

## Building a Windows EXE

You can create a standalone Windows EXE using PyInstaller. A helper script is provided: `build_exe.ps1`.

Quick steps:

1. Install PyInstaller in your active Python environment: `python -m pip install pyinstaller`.
2. Run the build script from the repo root in PowerShell: `./build_exe.ps1`.

Notes:
- The `_tools_/fontgen` folder (contains `fontgen.exe`) and `in/` are bundled into the EXE. The code detects PyInstaller's runtime extraction folder and will locate bundled `fontgen.exe` automatically.
- On Windows use the same architecture of Python that matches the native `fontgen` binaries.


# Unit tests
```bash
python test/util/read_xml_txt.py -v
```



# txt2fnt supported arguments

-ttf <ttf_file_name> : Specify TTF filename (in in/ttf/ with extension name) to use for font generation
-o <output_name> : Custom output name for the .fnt and .png file (no extension)