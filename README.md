velocireader
============

[project](https://sr.ht/~logankirkland/velocireader/) / 
[repo](https://git.sr.ht/~logankirkland/velocireader) / 
[mailing list](https://lists.sr.ht/~logankirkland/velocireader) /
[issues](https://todo.sr.ht/~logankirkland/velocireader)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![builds.sr.ht status](https://builds.sr.ht/~logankirkland/velocireader.svg)](https://builds.sr.ht/~logankirkland/velocireader?)

Reformats EPUB ebooks with bolded fixation points at the beginning 
of words to guide your eyes.

> ℹ️ **Note**  
> The canonical project locations are linked above. Other locations are 
> mirrors.

Installation
------------

### Clone the repo

```shell
git clone https://sr.ht/~logankirkland/velocireader/
```

### Install Python dependencies

```shell
python -m pip install -r requirements.txt
```

Usage
-----

```shell
python velocireader.py INPUTFILE
```

```
usage: velocireader.py [-h] [-o OUTPUT] [-s {1,2,3,4,5}] [-d {1,2,3,4,5}] [--demo] [input]

Reformats EPUB ebooks with bolded fixation points at the beginning of words to guide your eyes.

positional arguments:
  input                 input EPUB file path

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output EPUB file path
  -s {1,2,3,4,5}, --strength {1,2,3,4,5}
                        amount of text to bold at the beginning of each word, from 1-5. Default 2
  -d {1,2,3,4,5}, --distance {1,2,3,4,5}
                        distance between bolded words, from 1-5. Default 1
  --demo                print a sample of text processed with the selected settings
```

Thanks
------

This project is based on 
[dobrosketchkun/bionic-reading-epub-converter](https://github.com/dobrosketchkun/bionic-reading-epub-converter), 
which is licensed under 
[The Uncertain Commons License](https://github.com/dobrosketchkun/bionic-reading-epub-converter/blob/main/LICENSE).
Thank you for your contribution.
