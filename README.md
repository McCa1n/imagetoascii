# imagetoascii

Turn images in the current folder into ASCII art in the terminal.

## Features

- Converts `.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`, and `.webp`
- Prints colored ANSI ASCII art to the terminal
- Saves a plain text ASCII version as `*_ascii.txt`
- Supports custom output width

## Requirements

- Python 3.10+
- Pillow

## Install

```powershell
pip install -r requirements.txt
```

## Usage

Put one or more images in the same folder as `image_to_ascii.py`, then run:

```powershell
py image_to_ascii.py
```

Set a custom width:

```powershell
py image_to_ascii.py 160
```

## Notes

- ANSI color output looks best in Windows Terminal or terminals with ANSI color support.
- The generated `*_ascii.txt` files are ignored by Git by default.
