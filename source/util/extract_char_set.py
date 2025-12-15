import os
import re
import time


# need to pass previousSet by reference
def update_text_file(text_file:str, char_set:set[str]) -> set[str]:
    with open(text_file, "r", encoding="utf-8") as file:
        content = file.read()
        char_set.update(content)

    first_10_chars = list(char_set)[:10]
    print(f"File: {text_file}")
    print(f"First 10 characters: {first_10_chars}")
    print()

    return char_set

def update_xml_file(xml_file:str, char_set:set[str]) -> set[str]:
    from source.util.read_xml_txt import read_xml_texts

    texts = read_xml_texts(xml_file)
    for text in texts:
        char_set.update(text)

    first_10_chars = list(char_set)[:10]
    print(f"File: {xml_file}")
    print(f"First 10 characters: {first_10_chars}")
    print()

    return char_set


# split char_set into 2 sets
# one for supported characters
# one for unsupported characters
# unsupported regex: [©\t\nA-Za-z0-9 `~!@#$%^&*\(\)-_=+\[\{\]\}\\|;:'",<.>/?｀～！＠＃＄％＾＆＊（）－＿＝＋［］｛｝＼｜；：＇＂，＜．＞／？｢｣《》｟｠“”･·。｡､、…—]+
def split_char_set(char_set):
    regexSkip = r"[\t\n]+"
    regexIgnore = r"[©\t\nA-Za-z0-9 `~!@#$%^&*\(\)-_=+\[\{\]\}\\|;:'\",<.>/?｀～！＠＃＄％＾＆＊（）－＿＝＋［］｛｝＼｜；：＇＂，＜．＞／？｢｣《》｟｠“”･·。｡､、…—]+"
    found = set()
    ingored = set()
    for char in char_set:
        if re.match(regexSkip, char):
            continue

        if not re.match(regexIgnore, char):
            found.add(char)
        else:
            ingored.add(char)

    # sort the supported characters by their unicode code point
    found = sorted(found)
    ingored = sorted(ingored)

    return found, ingored


def save_char_set(char_set, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        # each line 64 characters
        for i, char in enumerate(char_set):
            file.write(char)
            if (i + 1) % 64 == 0:
                file.write("\n")

    print(f"Saved to {output_file}")
