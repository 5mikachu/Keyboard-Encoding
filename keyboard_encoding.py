import sys
import unicodedata
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QRadioButton, QTextEdit, QPushButton, QButtonGroup
from layouts import *  # Keyboard layouts from layouts.py

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
            encoded_text.append('�') # Unknown character

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
            decoded_text.append('�') # Unknown code

    return ''.join(decoded_text)

# Console interface
def console():
    global layout_lowercase, layout_uppercase

    layout = input("\nInsert Layout: \n").strip().lower()

    if layout in layouts:
        layout_lowercase, layout_uppercase = layouts[layout]
        make_dicts()

    else:
        print("\nInvalid input.")
        console()

    while True:
        choice = input("\nWhat would you like to do? \n 1 - encode \n 2 - decode \n 3 - switch layout \n 4 - exit \n").strip().lower()
        if choice == '1' or choice == 'encode':
            choice_type = input("\nWhat would you like to encode? \n 1 - text \n 2 - file \n")
            if choice_type == '1' or choice_type == 'text':
                text_to_encode = input("\nEnter the text to encode: \n")

            elif choice_type == '2' or choice_type == 'file':
                file = open(input("\nEnter the file name: \n"), 'r')
                text_to_encode = file.read()
                file.close()

            encoded = encode_text(text_to_encode)
            print("\nEncoded Text: \n", encoded)

        elif choice == '2' or choice == 'decode':
            choice_type = input("\nWhat would you like to decode? \n 1 - text \n 2 - file \n")
            if choice_type == '1' or choice_type == 'text':
                text_to_decode = input("\nEnter the encoded text to decode: \n")

            elif choice_type == '2' or choice_type == 'file':
                file = open(input("\nEnter the file name: \n"), 'r')
                text_to_decode = file.read()
                file.close()

            decoded = decode_text(text_to_decode)
            print("\nDecoded Text: \n", decoded)

        elif choice == '3' or choice == 'switch':
            console()

        elif choice == '4' or choice == 'exit':
            print("Exiting the program.")
            break

        else:
            print("\nInvalid input.")

# GUI interface
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Keyboard Encoding')

        # Layouts
        main_layout = QVBoxLayout()
        dropdown_layout = QHBoxLayout()
        radio_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # Layout dropdown
        self.dropdown = QComboBox()
        self.dropdown.addItem('AZERTY', 'ay')
        self.dropdown.addItem('Colemak', 'ck')
        self.dropdown.addItem('Dvorak', 'dk')
        self.dropdown.addItem('HCESAR', 'hr')
        self.dropdown.addItem('QWERTY', 'qy')
        self.dropdown.addItem('QWERTZ', 'qz')
        self.dropdown.addItem('Workman', 'wn')

        dropdown_label = QLabel('Keyboard Layout:')
        dropdown_layout.addWidget(dropdown_label)
        dropdown_layout.addWidget(self.dropdown)

        # Radio buttons
        self.encode_radio = QRadioButton('Encode')
        self.decode_radio = QRadioButton('Decode')
        self.encode_radio.setChecked(True)  # Set Encode as the default option

        self.radio_group = QButtonGroup()
        self.radio_group.addButton(self.encode_radio)
        self.radio_group.addButton(self.decode_radio)

        radio_layout.addWidget(self.encode_radio)
        radio_layout.addWidget(self.decode_radio)

        # Textbox with text to encode/decode
        self.textbox = QTextEdit()
        self.textbox.setPlaceholderText('Enter your text here')

        # Submit and Reset buttons
        self.submit_button = QPushButton('Submit')
        self.reset_button = QPushButton('Reset')

        self.submit_button.clicked.connect(self.submit)
        self.reset_button.clicked.connect(self.reset)

        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.reset_button)

        # Add layouts to the main layout
        main_layout.addLayout(dropdown_layout)
        main_layout.addLayout(radio_layout)
        main_layout.addWidget(self.textbox)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def submit(self):
        layout_key = self.dropdown.currentData()
        text = self.textbox.toPlainText()

        global layout_lowercase, layout_uppercase
        layout_lowercase, layout_uppercase = layouts[layout_key]
        
        make_dicts()
        
        if self.encode_radio.isChecked():
            encoded = encode_text(text)
            print(encoded)
            self.textbox.setText(encoded)

        elif self.decode_radio.isChecked():
            decoded = decode_text(text)
            print(decoded)
            self.textbox.setText(decoded)

    def reset(self):
        self.dropdown.setCurrentIndex(0)
        self.encode_radio.setChecked(True)
        self.textbox.clear()

# Main function to determine which interface to run
if __name__ == "__main__":    
    if len(sys.argv) <= 1:
        print(" No argument, use '-h' or '--help' for help \n")

    else:
        if sys.argv[1] == "-g" or sys.argv[1] == "--graphical":
            app = QApplication(sys.argv)
            window = MainWindow()
            window.show()
            sys.exit(app.exec_())
            
        elif sys.argv[1] == "-t" or sys.argv[1] == "--terminal":
            console()
        
        elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print(" -c, --console:   Open in console mode \n -t, --terminal:  Open in terminal mode \n -h, --help:      Get information about how to use this program \n")
            
        else:
            print(" Unknown argument, use '-h' or '--help' for help \n")
