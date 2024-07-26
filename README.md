# Keyboard Encoding Thingy

Are your text files to easy to read? Is plain-text to optimized for you?

THEN THIS PROGRAM IS MADE FOR YOU!!

This Python program allows you to 'encode' and 'decode' text using various keyboard layouts. It supports multiple layouts and can handle both individual text input and text files.

# Features

* **Multiple Keyboard Layouts**: Supports AZERTY, Colemak, Dvorak, HCESAR, QWERTY, QWERTZ, and Workman.
* **Encoding and Decoding**: Converts text to encoded format and vice versa.
* **File Handling**: Can 'encode' and 'decode' text from files.
* **Interactive Menu**: (Kind of) User-friendly interface to select actions and keyboard layouts.

# Examples

_Unless stated otherwise, I probably used QWERTY. I might not have though._

**in**: The quick brown fox jumps over the lazy dog.!?  
**out**: 12x05 03x06 02x03 00x00 02x01 02x07 02x08 04x03 03x08 00x00 04x05 02x04 02x09 02x02 04x06 00x00 03x04 02x09 04x02 00x00 03x07 02x07 04x07 02x10 03x02 00x00 02x09 04x04 02x03 02x04 00x00 02x05 03x06 02x03 00x00 03x09 03x01 04x01 02x06 00x00 03x03 02x09 03x05 04x09 11x02 14x10

## To: The Devil

If one layer of confusion is not enough for you, consider switching keyboard layouts and then decoding it with that.

The quick brown fox jumps over the lazy dog.!?  
--qy--> 12x05 03x06 02x03 00x00 02x01 02x07 02x08 04x03 03x08 00x00 04x05 02x04 02x09 02x02 04x06 00x00 03x04 02x09 04x02 00x00 03x07 02x07 04x07 02x10 03x02 00x00 02x09 04x04 02x03 02x04 00x00 02x05 03x06 02x03 00x00 03x09 03x01 04x01 02x06 00x00 03x03 02x09 03x05 04x09 11x02 14x10  
--dk-> Yd. 'gcjt xpr,b urq hgmlo rk.p yd. na;f eriv!Z  
--qz-> 14x01 03x03 04x09 00x00 13x12 03x05 04x03 03x07 02x05 00x00 04x02 02x10 02x04 04x08 04x05 00x00 02x07 02x04 02x01 00x00 03x06 03x05 04x07 03x09 02x09 00x00 02x04 03x08 04x09 02x10 00x00 04x01 03x03 04x09 00x00 04x06 03x01 14x08 03x04 00x00 02x03 02x04 02x08 04x04 11x02 12x06  
--qy-> Zd. �gcjt xpr,b urq hgmlo rk.p zd. na<f eriv!Y

# Requirements

* Python 3.x
* layouts.py file containing keyboard layout definitions

# Usage

## Starting the Program

To start the program, run the following command:

```
python keyboard_encoding.py
```

## Main Menu

_At the moment this is the only menu, but Main Menu sound better._

When running the program, you will be prompted to select a keyboard layout. Currently available options are:

* ay: AZERTY
* ck: Colemak
* dk: Dvorak
* hr: HCESAR
* qy: QWERTY
* qz: QWERTZ
* wn: Workman

After selecting a layout, the main menu will provide the following options:

1. Encode
2. Decode
3. Switch Layout
4. Exit (My favorite)

When either Encode or Decode is chosen you will be prompted if you want to encode/decode text or text from a file.

# Documentation

## Layouts

Layouts are imported from layouts.py, which must contain the table for lowercase and uppercase for each layout.

``` py
qwerty_lowercase = [
    ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', ' '],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', ' ', ' ']
]

qwerty_uppercase = [
    ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"', ' '],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?', ' ', ' ']
]
```

Layouts are then defined in _layouts_, which you can find at the bottom of the layouts.py file.

``` py
layouts = {
    'ay': (azerty_lowercase, azerty_uppercase),
    'ck': (colemak_lowercase, colemak_uppercase),
    'dk': (dvorak_lowercase, dvorak_uppercase),
    'hr': (hcesar_lowercase, hcesar_uppercase),
    'qy': (qwerty_lowercase, qwerty_uppercase),
    'qz': (qwertz_lowercase, qwertz_uppercase),
    'wm': (workman_lowercase, workman_uppercase)
}
```

## UPPERCASE vs lowercase

Characters are stored as 'text-nibbles' formatted as 00x00:

|0  |0  |x  |0  |  0|
|---|---|---|---|---|
|Uppercase if 1|column num. (1-3)||Row num.1|Row num.2|

## Special characters

``` py
encode_special_mappings = {
    ' ': '00x00',
    '\n': '10x00',
    '̀': '00x01',
    '́': '00x02',
    '̂': '00x03',
    '̃': '00x04',
    '̄': '00x05',
    '̎': '00x06'
}
```

More can be added if needed, can be found in layouts.py
