# Keyboard Encoding Thingy

Are your text files to easy to read? Is plain-text to optimized for you?

THEN THIS PROGRAM IS MADE FOR YOU!!

This Python program allows you to 'encode' and 'decode' text using various keyboard layouts. It supports multiple layouts and can handle both individual text input and text files.

# Features

* **Multiple Keyboard Layouts**: Supports AZERTY, Colemak, Dvorak, HCESAR, QWERTY, QWERTZ, and Workman.
* **Encoding and Decoding**: Converts text to encoded format and vice versa.
* **File Handling**: Can 'encode' and 'decode' text from files.
* **Interactive Menu**: Both a GUI and console based interface.

# Examples

_Unless stated otherwise, QWERTY was used._

**in**: The quick brown fox jumps over the lazy dog.!?  
**out**: 12x05 03x06 02x03 00x00 02x01 02x07 02x08 04x03 03x08 00x00 04x05 02x04 02x09 02x02 04x06 00x00 03x04 02x09 04x02 00x00 03x07 02x07 04x07 02x10 03x02 00x00 02x09 04x04 02x03 02x04 00x00 02x05 03x06 02x03 00x00 03x09 03x01 04x01 02x06 00x00 03x03 02x09 03x05 04x09 11x02 14x10

**in**: 04x06 02x03 00x02 02x03 04x08 00x00 02x03 04x06 02x05 02x04 02x03 02x10 02x09 00x03 02x05 04x08 00x00 14x01 02x09 02x03 00x09 04x08 00x00 03x04 03x01 04x03 00x13 03x01 03x03 02x03 04x08 00x00 13x02 02x03 04x06 00x04 02x09 02x04 04x08 00x00 03x06 03x01 00x02 04x03 00x0D 02x03 03x08
**out**: née, entrepôt, Zoë, façade, Señor, háček

# Requirements

* Python 3.x
* layouts.py file containing keyboard layout definitions

# Usage

## Starting the Program

To start the program, run one of the following commands:

To start the program in GUI mode:
``` BASH
python keyboard_encoding.py -g
```

To start the program in console mode:
``` BASH
python keyboard_encoding.py -t
```

## Main Menu

_At the moment this is the only menu, but Main Menu sound better._

When running the program, you will be prompted to select a keyboard layout. Currently available options are:

* ar: Arabic
* ay: AZERTY
* ck: Colemak
* dk: Dvorak
* gr: Greek
* he: Hebrew
* hr: HCESAR
* qy: QWERTY
* qz: QWERTZ
* ru: Cyrillic
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
    'ar': (arabic_lowercase, arabic_uppercase),
    'ay': (azerty_lowercase, azerty_uppercase),
    'ck': (colemak_lowercase, colemak_uppercase),
    'dk': (dvorak_lowercase, dvorak_uppercase),
    'gr': (greek_lowercase, greek_uppercase),
    'he': (hebrew_lowercase, hebrew_uppercase),
    'hr': (hcesar_lowercase, hcesar_uppercase),
    'qy': (qwerty_lowercase, qwerty_uppercase),
    'qz': (qwertz_lowercase, qwertz_uppercase),
    'ru': (cyrillic_lowercase, cyrillic_uppercase),
    'wn': (workman_lowercase, workman_uppercase)
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
    ' ': '00x00',  # SPACE
    '\n': '10x00', # Newline
    '\t': '10x01', # Tab
    '\\': '10x02', # Backslash
    '\'': '10x03', # Single quote
    '\"': '10x04', # Double quote
    '\r': '10x05', # Carriage return
    '\b': '10x06', # Backspace
    '\f': '10x07', # Form feed
    '\v': '10x08', # Vertical tab
    '\a': '10x09', # Bell/alert
    '̀': '00x01',   # Grave accent
    '́': '00x02',   # Acute accent
    '̂': '00x03',   # Circumflex
    '̃': '00x04',   # Tilde
    '̄': '00x05',   # Macron
    '̅': '00x06',   # Overline
    '̆': '00x07',   # Breve
    '̇': '00x08',   # Dot above
    '̈': '00x09',   # Diaeresis (Umlaut)
    '̉': '00x0A',   # Hook above
    '̊': '00x0B',   # Ring above
    '̋': '00x0C',   # Double acute accent
    '̌': '00x0D',   # Caron (Hacek)
    '̍': '00x0E',   # Vertical line above
    '̎': '00x0F',   # Double vertical line above
    '̐': '00x10',   # Candrabindu
    '̑': '00x11',   # Inverted breve
    '̒': '00x12',   # Turned comma above
    '̧': '00x13',   # Cedilla
    '̨': '00x14',   # Ogonek
    '̱': '00x15',   # Macron below
    '̲': '00x16',   # Low line (underscore)
    '̳': '00x17',   # Double low line
    '̹': '00x18',   # Left half ring below
    '̺': '00x19',   # Right half ring below
    '̻': '00x1A',   # Inverted bridge below
    '̼': '00x1B',   # Seagull below
    'ͅ': '00x1C',   # Greek iota subscript
}
```

More can be added if needed, can be found in layouts.py
