import argparse
import os
import zipfile
from pathlib import Path

import regex
from bs4 import BeautifulSoup


def main():
    args = _parse_args()

    if os.path.exists(args.output):
        response = input(
            f"Output file '{args.output}' already exists. It will be overwritten. "
            f"Continue? [Y/n] "
        )
        if response.lower() not in ["y", ""]:
            return

    process_epub(args.input, args.output)
    print(f"Conversion complete. Output saved to '{args.output}'.")


def process_epub(input_path, output_path):
    with zipfile.ZipFile(input_path, "r") as zip_ref:
        file_list = zip_ref.infolist()

        with zipfile.ZipFile(output_path, "w") as zip_out:
            for file_info in file_list:
                with zip_ref.open(file_info) as file:
                    content = file.read()

                    if file_info.filename.endswith((".xhtml", ".html", ".htm")):
                        content = _process_file(content)

                    zip_out.writestr(file_info, content)


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Reformats EPUB ebooks with bolded fixation points at the "
        "beginning of words to guide your eyes."
    )
    parser.add_argument("input", help="input EPUB file path")
    parser.add_argument("-o", "--output", help="output EPUB file path", required=False)
    args = parser.parse_args()

    args.input = Path(args.input)
    if args.output is None:
        args.output = args.input.with_stem(args.input.stem + "_robo")
    else:
        args.output = Path(args.output)

    return args


def _process_file(content):
    soup = BeautifulSoup(content, features="xml")

    skip_tags = {"script", "style", "pre", "code"}

    for element in soup.find_all(string=True):
        if element.parent.name not in skip_tags:
            new_text = _process_text(element.string)
            new_element = BeautifulSoup(new_text, "html.parser")
            element.replace_with(new_element)

    return str(soup)


def _process_text(text):
    word_pattern = regex.compile(r"\b[\p{L}\p{M}]+\b", regex.UNICODE)

    def replace_word(match):
        word = match.group(0)
        return _robotize_word(word)

    return word_pattern.sub(replace_word, text)


def _robotize_word(word):
    if len(word) <= 1:
        return word
    elif len(word) <= 3:
        return f"<b>{word[:1]}</b>{word[1:]}"
    else:
        midpoint = len(word) // 2
        return f"<b>{word[:midpoint]}</b>{word[midpoint:]}"


if __name__ == "__main__":
    main()
