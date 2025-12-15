import os
import argparse
from source.util.extract_char_set import save_char_set, split_char_set, update_text_file, update_xml_file


def parse_args():
    parser = argparse.ArgumentParser(description="Generate font files from text and TTF inputs")
    parser.add_argument("-ttf", dest="ttf", help="Specify TTF filename (in in/ttf/ with/without extension name) to use for font generation")
    parser.add_argument("-o", "--output-name", dest="output_name", help="Custom output name for the .fnt file (no extension)")
    parser.add_argument("-fs", "--font-size", dest="font_size", type=int, default=23, help="Specify font size (default 23)")
    return parser.parse_args()


def main():
    args = parse_args()

    pwd = os.getcwd()
    # log present working directory
    print("Present Working Directory:", pwd)



    textFolder = "in/text/"
    textFolderFilesRaw = os.listdir(textFolder)


    char_set = set()

    for file_name in textFolderFilesRaw:
        file_path = os.path.join(textFolder, file_name)
        ext = os.path.splitext(file_name)[1].lower()
        if ext == '.txt':
            char_set = update_text_file(file_path, char_set)
        elif ext == '.xml':
            char_set = update_xml_file(file_path, char_set)

    accepted_chars, excluded_chars = split_char_set(char_set)

    acceptedCount = len(accepted_chars)
    excludedCount = len(excluded_chars)

    char2chunkFolder = os.path.join("workspace", "char2chunk")
    if not os.path.exists(char2chunkFolder):
        os.makedirs(char2chunkFolder)
    else:
        # clean up existing files in char2chunkFolder
        for file in os.listdir(char2chunkFolder):
            os.remove(os.path.join(char2chunkFolder, file))


    accepted_file = f"extracted_chunk_{acceptedCount}.txt"
    outFileAccepted = os.path.join(char2chunkFolder, accepted_file)
    print(f"Accepted Characters ({acceptedCount}): saved to {outFileAccepted}")
    outFileIgnored = os.path.join(char2chunkFolder, f"igored_{excludedCount}.txt")


    save_char_set(accepted_chars, outFileAccepted)
    save_char_set(excluded_chars, outFileIgnored)


    print()
    print()
    print("=== Selecting TTF File for Font Generation ===")
    ttfFolder = "in/ttf/"
    # create the folder if not exists
    if not os.path.exists(ttfFolder):
        os.makedirs(ttfFolder)
        # ask user to add ttf files in the folder and exit
        print(f"TTF folder created at {ttfFolder}. Please add TTF files and run again.")
        exit(1)

    # list all ttf files in ttfFolder
    ttfFiles = [f for f in os.listdir(ttfFolder) if f.endswith('.ttf')]
    totalTtfFiles = len(ttfFiles)
    # log total number of ttf files found
    print("Total TTF Files Found:", totalTtfFiles)
    # if no ttf files found, exit
    if totalTtfFiles == 0:
        print("No TTF files found in the specified folder. (in/ttf/)")
        exit(1)

    print("Available TTF Files:")
    # list all ttf files with counter
    for i, f in enumerate(ttfFiles):
        print(f"{i + 1}. {f}")

    # default: pick the first ttf file found
    selectedTtfFile = ttfFiles[0]

    # If user provided -ttf, try to use that (supports basename or full path)
    if args.ttf:
        candidate = args.ttf
        if candidate in ttfFiles:
            selectedTtfFile = candidate
        elif candidate + ".ttf" in ttfFiles:
            selectedTtfFile = candidate + ".ttf"
        else:
            print(f"Could not find specified TTF file '{candidate}' in in/ttf/.")
            # exit if not found
            exit(1)

    ttf_file = os.path.join(ttfFolder, selectedTtfFile)


    print()
    print()
    print("=== Starting Font Generation ===")
    char_chunk_file = outFileAccepted
    custom_fnt_output_name = args.output_name if args.output_name else None
    # char_chunk_file
    print("Using Character Chunk File:", char_chunk_file)

    print("Using TTF File:", ttf_file)
    # print("TTF File Full Path:", ttf_file_full_path)

    if custom_fnt_output_name:
        print("Custom FNT Output Name:", custom_fnt_output_name)
    else:
        print(f"Using default FNT output name based on TTF filename. ({selectedTtfFile})")


    from source.util.fontgen import use_fontgen
    use_fontgen(
        char_chunk_file=char_chunk_file,
        ttf_file=ttf_file,
        custom_fnt_output_name=custom_fnt_output_name,
        font_size=args.font_size,
    )


if __name__ == "__main__":
    main()