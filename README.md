# Keyboard Encoding Thingy

Are your text files too easy to read? Is plain-text too optimized for you?

**THEN THIS PROGRAM IS MADE FOR YOU!!**

This Python program allows you to 'encode' and 'decode' text using various keyboard layouts. It supports multiple layouts and can handle both individual text input and text files.

# Features

* **Multiple Keyboard Layouts**: Supports AZERTY, Colemak, Dvorak, HCESAR, QWERTY, QWERTZ, Workman and more.
* **Encoding and Decoding**: Converts text to encoded format and vice versa.
* **Layout Switching**: It is possible to switch layout mid de/encode.
* **Adding custom Layouts**: It is possible to add your own layout.

# Examples

Unless stated otherwise, QWERTY was used.

## Encode and Decode

**in**: The quick brown fox jumps over the lazy dog.!?  
**out**: 12x05 03x06 02x03 00x00 02x01 02x07 02x08 04x03 03x08 00x00 04x05 02x04 02x09 02x02 04x06 00x00 03x04 02x09 04x02 00x00 03x07 02x07 04x07 02x10 03x02 00x00 02x09 04x04 02x03 02x04 00x00 02x05 03x06 02x03 00x00 03x09 03x01 04x01 02x06 00x00 03x03 02x09 03x05 04x09 11x02 14x10

**in**: 04x06 02x03 00x02 02x03 04x08 00x00 02x03 04x06 02x05 02x04 02x03 02x10 02x09 00x03 02x05 04x08 00x00 14x01 02x09 02x03 00x09 04x08 00x00 03x04 03x01 04x03 00x13 03x01 03x03 02x03 04x08 00x00 13x02 02x03 04x06 00x04 02x09 02x04 04x08 00x00 03x06 03x01 00x02 04x03 00x0D 02x03 03x08  
**out**: née, entrepôt, Zoë, façade, Señor, háček

## Switching layout

**in**: 13x03 02x08 03x03 00x00 02x06 02x09 02x07 00x00 03x08 04x06 02x09 02x02 00x00 jn 00x00 02x01 02x02 02x03 02x04 02x05 02x06 00x00 qy 00x00 02x08 03x02 00x00 04x06 02x09 02x05 00x00 03x01 00x00 02x02 02x09 02x04 03x03 14x10  
**out**: Did you know ~jn~ йцукен ~qy~ is not a word?

# Requirements

* Python 3.x
* layouts.json file containing keyboard layout definitions
* special_layouts.json file containing special mappings
* Flask
* Usage

# Usage

## Starting the Program

To install requirements:
``` sh
pip install -r requirements.txt 
```

To start the program:
``` sh
python app.py
```

## Web Interface

The Flask-based web interface is available at http://127.0.0.1:5000/. Accessing this will allow you to interact with the encoding/decoding features through a graphical interface, including:

* Selecting a keyboard layout
* Viewing selected layout
* Encoding or decoding text
* Adding custom layouts

When running the program, you will be asked to select a keyboard layout. Available options include:

* ay: AZERTY
* ck: Colemak
* dk: Dvorak
* hr: HCESAR
* qy: QWERTY
* qz: QWERTZ
* wn: Workman

# Documentation

## Layouts

Layouts are imported from layouts.json, which must contain the name and the data for lowercase and uppercase letters for
each layout.

``` json
"qy": {
  "name": "QWERTY",
  "lowercase": [
    ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="],
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'"],
    ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/"]
  ],
  "uppercase": [
    ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+"],
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}", "|"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":", "\""
    ],
    ["Z", "X", "C", "V", "B", "N", "M", "<", ">", "?"]
  ]
},
```

## UPPERCASE vs lowercase

Characters are stored as 'text-nibbles' formatted as 00x00:

| 0         | 0                 | x | 0         | 0         |
|-----------|-------------------|---|-----------|-----------|
| Def. case | column num. (1-3) |   | Row num.1 | Row num.2 |

## Special characters

Special characters can be found in special_mappings.json and are structured as seen below.

``` json
{
  " ": "00x00",
  "\n": "10x00",
  "\t": "10x01",
  "\r": "10x02",
  "\b": "10x03",
  "\f": "10x04",
  "\u0300": "00x01",
  "\u0301": "00x02",
  "\u0302": "00x03",
  "\u0303": "00x04",
  "\u0304": "00x05",
  "\u0305": "00x06",

  // And so on...
}
```

## Adding layouts

More can be added if needed, this can be done by hardcoding or by using add_layout().

As example, if the user wants to add QWERTY (they wouldn't be able to, as it already exists...), the user needs to do
the following.

``` sh
layout key:  qy
Layout name: QWERTY
Enter row 1 for lowercase: ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="]
Enter row 2 for lowercase: ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"]
Enter row 3 for lowercase: ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", " "]
Enter row 4 for lowercase: ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/", " ", " "]
Enter row 1 for uppercase: ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+"]
Enter row 2 for uppercase: ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "{", "}", "|"]
Enter row 3 for uppercase: ["A", "S", "D", "F", "G", "H", "J", "K", "L", ":", "\""]
Enter row 4 for uppercase: ["Z", "X", "C", "V", "B", "N", "M", "<", ">", "?"]
```
