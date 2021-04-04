# Koob

A CLI utility to extract information from Kobo db.

## Features

- Lists books with reading status
- Lists highlights
- Extracts highlights in markdown
- Auto detects Kobo devices (based on lsblk)

## Installation

Currently `koob` isn't available on the pip so so manual installation is required to use it.

```
python setup.py bdist_wheel
pip3 install dist/koob-0.0.0-py3-none-any.whl --user
```

## Usage

Lists last ten books.

```
koob books -n 10
```

Lists all books and specifies which database to use.

```
koob books --db path/to/db.sqlite
```

Lists all highlights.

```
koob annotations
```

Lists all highlights of books starting with *"ten"*.

```
koob annotations ten
```

Lists highlights of last annotated book in markdown format.

```
koob annotations -l --md
```

