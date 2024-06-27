roboreader
==========

[project](https://sr.ht/~logankirkland/roboreader/) / 
[repo](https://git.sr.ht/~logankirkland/roboreader) / 
[mailing list](https://lists.sr.ht/~logankirkland/roboreader) /
[issues](https://todo.sr.ht/~logankirkland/roboreader)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![builds.sr.ht status](https://builds.sr.ht/~logankirkland/roboreader.svg)](https://builds.sr.ht/~logankirkland/roboreader?)

Reformats EPUB ebooks with bolded fixation points at the beginning 
of words to guide your eyes.

> ℹ️ **Note**  
> The canonical project locations are linked above. Other locations are mirrors.

Installation
------------

### Clone the repo

```shell
git clone https://sr.ht/~logankirkland/roboreader/
```

### Install Python dependencies

```shell
python -m pip install -r requirements.txt
```

Usage
-----

```shell
python roboreader.py INPUTFILE
```

```
usage: roboreader.py [-h] [-o OUTPUT] input

Reformats EPUB ebooks with bolded fixation points at the beginning of 
words to guide your eyes.

positional arguments:
  input                 input EPUB file path

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output EPUB file path
```

Thanks
------

This project is based on 
[dobrosketchkun/bionic-reading-epub-converter](https://github.com/dobrosketchkun/bionic-reading-epub-converter), 
which is licensed under 
[The Uncertain Commons License](https://github.com/dobrosketchkun/bionic-reading-epub-converter/blob/main/LICENSE).
Thank you for your contribution.
