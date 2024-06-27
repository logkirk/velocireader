"""
Copyright 2024 Logan Kirkland

This file is part of roboreader.

roboreader is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later version.

roboreader is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
roboreader. If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import os
import zipfile
from math import ceil
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

    process_epub(args)
    print(f"Conversion complete. Output saved to '{args.output}'.")


def process_epub(args):
    with zipfile.ZipFile(args.input_path, "r") as zip_ref:
        file_list = zip_ref.infolist()

        with zipfile.ZipFile(args.output_path, "w") as zip_out:
            for file_info in file_list:
                with zip_ref.open(file_info) as file:
                    content = file.read()

                    if file_info.filename.endswith((".xhtml", ".html", ".htm")):
                        content = _process_file(content, args)

                    zip_out.writestr(file_info, content)


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Reformats EPUB ebooks with bolded fixation points at the "
        "beginning of words to guide your eyes."
    )
    parser.add_argument("input", help="input EPUB file path")
    parser.add_argument("-o", "--output", help="output EPUB file path", required=False)
    parser.add_argument(
        "-f",
        "--fixation",
        default=2,
        choices=range(1, 6),
        help="amount of text to embolden at the beginning of each word, from 1-5. "
        "Default 2",
        required=False,
    )
    args = parser.parse_args()

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
    x = args.fixation
    threshold = ceil((25.4 - 8.5 * x + 7.75 * x**2 - 0.75 * x**3) / 100 * len(word))
    return f"<b>{word[:threshold]}</b>{word[threshold:]}"


if __name__ == "__main__":
    main()
