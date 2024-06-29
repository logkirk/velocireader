"""
Copyright 2024 Logan Kirkland

This file is part of velocireader.

velocireader is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later version.

velocireader is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
velocireader. If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import os
import zipfile
from math import ceil
from pathlib import Path
from textwrap import fill

import regex
from bs4 import BeautifulSoup
from tqdm import tqdm

WRAP_WIDTH = 80


class TextEffect:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def main():
    args = _parse_args()

    if args.distance != 1:
        print(
            "Warning: the -d/--distance argument is not yet implemented and will be "
            "ignored."
        )

    if args.demo:
        demo(args)
        return

    if os.path.exists(args.output):
        response = input(
            f"Output file '{args.output}' already exists. It will be overwritten. "
            f"Continue? [Y/n] "
        )
        if response.lower() not in ["y", ""]:
            return

    process_epub(args)
    print(f"Conversion complete. Output saved to '{args.output}'.")


def demo(args):
    with open("resources/sample_peter_pan.txt", "r") as f:
        raw = f.read()

    paragraphs = [i for i in raw.split("\n") if i != ""]
    wrapped = [fill(i, width=WRAP_WIDTH, initial_indent="    ") for i in paragraphs]

    for paragraph in wrapped:
        print(paragraph)

    print()
    for paragraph in [_process_text(i, args) for i in wrapped]:
        print(paragraph)


def process_epub(args):
    with zipfile.ZipFile(args.input, "r") as zip_ref:
        file_list = zip_ref.infolist()

        with (
            zipfile.ZipFile(args.output, "w") as zip_out,
            tqdm(
                total=len(file_list), desc="Processing files", unit="file"
            ) as progress_bar,
        ):
            for file_info in file_list:
                with zip_ref.open(file_info) as file:
                    content = file.read()

                    if file_info.filename.endswith((".xhtml", ".html", ".htm")):
                        content = _process_file(content, args)

                    zip_out.writestr(file_info, content)

                progress_bar.update(1)
                progress_bar.set_postfix(current_file=file_info.filename)


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Reformats EPUB ebooks with bolded fixation points at the "
        "beginning of words to guide your eyes."
    )
    parser.add_argument("input", nargs="?", default=None, help="input EPUB file path")
    parser.add_argument("-o", "--output", required=False, help="output EPUB file path")
    parser.add_argument(
        "-s",
        "--strength",
        default=2,
        type=int,
        choices=range(1, 6),
        required=False,
        help="amount of text to bold at the beginning of each word, from 1-5. "
        "Default 2",
    )
    parser.add_argument(
        "-d",
        "--distance",
        default=1,
        type=int,
        choices=range(1, 6),
        required=False,
        help="distance between bolded words, from 1-5. Default 1",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        default=False,
        required=False,
        help="print a sample of text processed with the selected settings",
    )
    args = parser.parse_args()

    if not args.demo:
        if args.input is None:
            parser.error("the following arguments are required: input")

        args.input = Path(args.input)
        if args.output is None:
            args.output = args.input.with_stem(args.input.stem + "_robo")
        else:
            args.output = Path(args.output)

    return args


def _process_file(content, args):
    soup = BeautifulSoup(content, features="xml")

    skip_tags = {"script", "style", "pre", "code"}

    for element in soup.find_all(string=True):
        if element.parent.name not in skip_tags:
            new_text = _process_text(element.string, args)
            new_element = BeautifulSoup(new_text, "html.parser")
            element.replace_with(new_element)

    return str(soup)


def _process_text(text, args):
    word_pattern = regex.compile(r"\b[\p{L}\p{M}]+\b", regex.UNICODE)

    def replace_word(match):
        word = match.group(0)
        return _robotize_word(word, args)

    return word_pattern.sub(replace_word, text)


def _robotize_word(word, args):
    x = args.strength
    threshold = ceil((25.4 - 8.5 * x + 7.75 * x**2 - 0.75 * x**3) / 100 * len(word))
    if args.demo:
        return f"{TextEffect.BOLD}{word[:threshold]}{TextEffect.END}{word[threshold:]}"
    else:
        return f"<b>{word[:threshold]}</b>{word[threshold:]}"


if __name__ == "__main__":
    main()
