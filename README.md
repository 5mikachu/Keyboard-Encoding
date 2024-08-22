# Keyboard Encoding Thingy

Are your text files to easy to read? Is plain-text to optimized for you?

THEN THIS PROGRAM IS MADE FOR YOU!!

This Python program allows you to 'encode' and 'decode' text using various keyboard layouts. It supports multiple layouts and can handle both individual text input and text files.

# Features

* **Multiple Keyboard Layouts**: Supports AZERTY, Colemak, Dvorak, HCESAR, QWERTY, QWERTZ, Workman and more.
* **Encoding and Decoding**: Converts text to encoded format and vice versa.
* **File Handling**: Can 'encode' and 'decode' text from files.
* **Interactive Menu**: Both a GUI and console based interface.
* **Layout Switching**: It is possible to switch layout (when decoding).
* **Adding custom Layouts**: It is posable to ad your own layout.
* **Customization**: If by customization you mean changing values in a config...

# Examples

_Unless stated otherwise, QWERTY was used._

## Encode and Decode

**in**: The quick brown fox jumps over the lazy dog.!?  
**out**: 12x05 03x06 02x03 00x00 02x01 02x07 02x08 04x03 03x08 00x00 04x05 02x04 02x09 02x02 04x06 00x00 03x04 02x09 04x02 00x00 03x07 02x07 04x07 02x10 03x02 00x00 02x09 04x04 02x03 02x04 00x00 02x05 03x06 02x03 00x00 03x09 03x01 04x01 02x06 00x00 03x03 02x09 03x05 04x09 11x02 14x10

**in**: 04x06 02x03 00x02 02x03 04x08 00x00 02x03 04x06 02x05 02x04 02x03 02x10 02x09 00x03 02x05 04x08 00x00 14x01 02x09 02x03 00x09 04x08 00x00 03x04 03x01 04x03 00x13 03x01 03x03 02x03 04x08 00x00 13x02 02x03 04x06 00x04 02x09 02x04 04x08 00x00 03x06 03x01 00x02 04x03 00x0D 02x03 03x08  
**out**: née, entrepôt, Zoë, façade, Señor, háček

## Switching layout

**NOT YET POSSIBLE WHEN ENCODING**

**in**: 13x03 02x08 03x03 00x00 02x06 02x09 02x07 00x00 03x08 04x06 02x09 02x02 00x00 ru 00x00 02x01 02x02 02x03 02x04 02x05 02x06 00x00 qy 00x00 02x08 03x02 00x00 04x06 02x09 02x05 00x00 03x01 00x00 02x02 02x09 02x04 03x03 14x10  
**out**: Did you know ~ru~ йцукен ~qy~ is not a word?

# Requirements

* Python 3.x
* layouts.py file containing keyboard layout definitions

# Usage

## Starting the Program

To start the program, run one of the following commands:

To start the program in GUI mode:
``` sh
python keyboard_encoding.py -g
```

To start the program in console mode:
``` sh
python keyboard_encoding.py -c
```

To get information on how to run the program:
``` sh
python keyboard_encoding.py -h
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

1. encode
2. decode
3. switch layout
4. add layout
5. switch to GUI
6. Exit (My favorite)

When either Encode or Decode is chosen you will be prompted if you want to encode/decode text or text from a file.

# Documentation

## Layouts

Layouts are imported from layouts.py, which must contain the name and the data for lowercase and uppercase letters for each layout.

``` py
'qy': {
    'name': 'QWERTY',
    'lowercase': [
        ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
        ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
        ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', ' '],
        ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', ' ', ' ']
    ],
    'uppercase': [
        ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'],
        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"', ' '],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?', ' ', ' ']
    ]
```

## UPPERCASE vs lowercase

Characters are stored as 'text-nibbles' formatted as 00x00:

|0  |0  |x  |0  |  0|
|---|---|---|---|---|
|Def. case|column num. (1-3)||Row num.1|Row num.2|

## Special characters

``` py
encode_special_mappings = {
    ' ': '00x00',  # SPACE
    '\n': '10x00', # Newline
    '\t': '10x01', # Tab
    '\r': '10x02', # Carriage return
    '\b': '10x03', # Backspace
    '\f': '10x04', # Form feed
    '\v': '10x05', # Vertical tab
    '\a': '10x06', # Bell/alert
    '̀': '00x01',   # Grave accent
    '́': '00x02',   # Acute accent
    '̂': '00x03',   # Circumflex
    '̃': '00x04',   # Tilde
    '̄': '00x05',   # Macron
    
    # And so on...
}
```

## Adding layouts

More can be added if needed, this can be done by hardcoding or by using add_layout().  

As example, if the user wants to add QWERTY (they wouldn't be able to, as it already exists...), the user needs to do the following.

``` sh
layout key:  qy
Layout name: QWERTY
Enter row 1 for lowercase: ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=']
Enter row 2 for lowercase: ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\']
Enter row 3 for lowercase: ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', ' ']
Enter row 4 for lowercase: ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', ' ', ' ']
Enter row 1 for uppercase: ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+']
Enter row 2 for uppercase: ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|']
Enter row 3 for uppercase: ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"', ' ']
Enter row 4 for uppercase: ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?', ' ', ' ']
```

To get to the add_layout() function, simply type 'add layout' when prompted for a layout or choose 4 in the main menu.