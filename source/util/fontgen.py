# use the _tools_/fontgen/fontgen.exe to generate font atlas from ttf file and char chunk file and predefined charset


import os
import shutil
import string


fontgen_folder = os.path.join("_tools_", "fontgen")


def create_fontgen_config_json(
    char_chunk_file: str,
    ttf_file: str,
    output_fnt: str,
    font_size: int = 23,
) -> dict:

    config = {
        "inputs": [ttf_file],
        "output": output_fnt + ".fnt",
        "charset": [
            char_chunk_file,
            # "0123456789",
            # "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            # "abcdefghijklmnopqrstuvwxyz",
            string.digits,
            string.ascii_letters,
            " ",
            "`~!@#$%^&*()-_=+[]{}\\|;:'\",<.>/?",
            "０１２３４５６７８９",
            "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ",
            "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ",
            "　",
            "｀～！＠＃＄％＾＆＊（）－＿＝＋［］｛｝＼｜；：＇＂，＜．＞／？",
            "｢｣《》｟｠“”･·。｡､、…—",
            "©",
        ],
        "dfSize": 6,
        "fontSize": font_size,
        "mode": "msdf",
        "options": ["fixwinding", "allownonprint"],
        "padding": {"bottom": 0, "left": 0, "right": 0, "top": 0},
        "spacing": {"x": 1, "y": 1},
    }

    return config


def use_fontgen(
    char_chunk_file: str,
    ttf_file: str,
    font_size: int = 23,
    custom_fnt_output_folder: str | None = None,
    custom_fnt_output_name: str | None = None,
) -> bool:
    import subprocess
    import json

    fontgen_exe = os.path.join(fontgen_folder, "fontgen.exe")
    ttf_file_basename = os.path.basename(ttf_file)
    ttf_file_name = os.path.splitext(ttf_file_basename)[0]

    output_fnt = ""
    output_fnt_folder = ""
    if custom_fnt_output_folder:
        output_fnt_folder = custom_fnt_output_folder
    else:
        output_fnt_folder = os.path.join("workspace", "fnt")

    if custom_fnt_output_name:
        output_fnt = os.path.join(output_fnt_folder, custom_fnt_output_name)
    else:
        output_fnt = os.path.join(output_fnt_folder, ttf_file_name)

    # ensure workspace/fnt folder exists
    if not os.path.exists(output_fnt_folder):
        os.makedirs(output_fnt_folder)

    # create config json and save to temp file in workspace folder
    config = create_fontgen_config_json(
        char_chunk_file=char_chunk_file,
        ttf_file=ttf_file,
        output_fnt=output_fnt,
        font_size=font_size,
    )

    config_json_path = os.path.join("temp_fontgen_config.json")
    with open(config_json_path, "w", encoding="utf-8") as json_file:
        json.dump(config, json_file, indent=2)

    foundOriAndDelete = False
    # delete original output_fnt .fnt and .png if exists
    if os.path.exists(output_fnt + ".fnt"):
        os.remove(output_fnt + ".fnt")
        foundOriAndDelete = True
    if os.path.exists(output_fnt + ".png"):
        os.remove(output_fnt + ".png")
        foundOriAndDelete = True

    if foundOriAndDelete:
        print(
            f"🚮  Deleted existing output files for clean generation. ({output_fnt}.fnt and {output_fnt}.png)"
        )

    # run fontgen exe with config json
    print()
    print(f"⏳  Generating font: {output_fnt}.fnt using TTF: {ttf_file_basename}")

    # fontgen_folder check if folder exists, if not, create folder, exit with error and ask user to add fontgen tool
    if not os.path.exists(fontgen_folder):
        os.makedirs(fontgen_folder)
        print(
            f"⚠️  fontgen folder not found at {fontgen_folder}. Please ensure the tool is present."
        )
        return False

    # if fontgen exe not found, exit with error
    if not os.path.exists(fontgen_exe):
        print(f"⚠️  fontgen.exe not found at {fontgen_exe}. Please ensure the tool is present.")
        return False

    print(f"fontgen_exe: {fontgen_exe}")
    print(f"config_json_path: {config_json_path}")
    result = subprocess.run(
        [
            ".\\" + fontgen_exe,
        ]
        + [
            ".\\" + config_json_path,
        ],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    print(result.stderr)

    # check if output fnt file is created
    if os.path.exists(output_fnt + ".fnt"):
        print("✅  Font generation completed. Please check the workspace/fnt/ folder.")
        return True
    else:
        print("⚠️  Font generation failed.")
        return False
