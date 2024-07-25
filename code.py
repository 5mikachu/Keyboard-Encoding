import unicodedata
from layouts import * # Keyboard layouts from layouts.py

# Function to create encoding and decoding dictionaries for a given layout
def create_encoding_dicts(layout, prefix):
    encode_dict = {}
    decode_dict = {}

    for row_idx, row in enumerate(layout):
        for col_idx, char in enumerate(row):
            if char.strip():  # Ignore empty spaces in the layout
                code = f"{prefix}{row_idx+1:01}x{col_idx+1:02}"
                encode_dict[char] = code
                decode_dict[code] = char

    return encode_dict, decode_dict

# Create dictionaries for encoding and decoding
def make_dicts():
    # Create encoding and decoding dictionaries for lowercase and uppercase
    encode_dict_lower, decode_dict_lower = create_encoding_dicts(layout_lowercase, '0')
    encode_dict_upper, decode_dict_upper = create_encoding_dicts(layout_uppercase, '1')

    # Merge the dictionaries for ease of use
    global encode_dict, decode_dict
    encode_dict = {**encode_dict_lower, **encode_dict_upper}
    decode_dict = {**decode_dict_lower, **decode_dict_upper}

# Function to encode text
def encode_text(text):
    # Normalize the text using NFD
    normalized_text = unicodedata.normalize('NFD', text)
    
    encoded_text = []
    for char in normalized_text:
        if char in encode_dict:
            encoded_text.append(encode_dict[char])
        elif char in encode_special_mappings:
            encoded_text.append(encode_special_mappings[char])
        else:
            encoded_text.append('�')  # Unknown character

    return ' '.join(encoded_text)

# Function to decode text
def decode_text(encoded_text):
    decoded_text = []
    codes = encoded_text.split()

    for code in codes:
        if code in decode_dict:
            decoded_text.append(decode_dict[code])
        elif code in decode_special_mappings:
            decoded_text.append(decode_special_mappings[code])
        else:
            decoded_text.append('�')  # Unknown code

    return ''.join(decoded_text)

# prompt user for keyboard layout to use
def start():
    global layout_lowercase, layout_uppercase

    layouts = {
        'ay': (azerty_lowercase, azerty_uppercase),
        'ck': (colemak_lowercase, colemak_uppercase),
        'dk': (dvorak_lowercase, dvorak_uppercase),
        'hr': (hcesar_lowercase, hcesar_uppercase),
        'qy': (qwerty_lowercase, qwerty_uppercase),
        'qz': (qwertz_lowercase, qwertz_uppercase),
        'wm': (workman_lowercase, workman_uppercase)
    }

    layout = input("Insert Layout: \n").strip().lower()

    if layout in layouts:
        layout_lowercase, layout_uppercase = layouts[layout]
    else:
        print("\nInvalid input.")
        start()

    make_dicts()
    main()


# Main function to prompt user for input
def main():
    while True:
        choice = input("\nWhat would you like to do? \n 1 - encode \n 2 - decode \n 3 - switch layout \n 4 - exit \n").strip().lower()
        if (choice == '1' or choice == 'encode'):
            choice_type = input("\nWhat would you like to encode? \n 1 - text \n 2 - file \n")
            if choice_type == '1' or choice_type == 'text':
                text_to_encode = input("\nEnter the text to encode: \n")
            elif choice_type == '2' or choice_type == 'file':
                file = open(input("\nEnter the file name: \n"), 'r')
                text_to_encode = file.read()
                file.close()
            encoded = encode_text(text_to_encode)
            print("\nEncoded Text: \n",encoded)
        elif choice == '2' or choice == 'decode':
            choice_type = input("\nWhat would you like to decode? \n 1 - text \n 2 - file \n")
            if choice_type == '1' or choice_type == 'text':
                text_to_decode = input("\nEnter the encoded text to decode: \n")
            elif choice_type == '2' or choice_type == 'file':
                file = open(input("\nEnter the file name: \n"), 'r')
                text_to_encode = file.read()
                file.close()
            decoded = decode_text(text_to_decode)
            print("\nDecoded Text: \n",decoded)
        elif choice == '3' or choice == 'switch':
            start()
        elif choice == '4' or choice == 'exit':
            print("Exiting the program.")
            break
        else:
            print("\nInvalid input.")

# Run the start function at start
if __name__ == "__main__":
    start()
