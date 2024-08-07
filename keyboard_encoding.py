import sys
import unicodedata
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QRadioButton, QTextEdit, QPushButton, QButtonGroup
from layouts import *  # Keyboard layouts from layouts.py

class EncodeDecode:
    def __init__(self):
        self.encoding_dict = {}
        self.decoding_dict = {}
        self.layout_lowercase = []
        self.layout_uppercase = []

    def generate_layout_dicts(self, layout, prefix):
        """
        Generates encoding and decoding dictionaries for a given keyboard layout.

        Args:
            layout (list): The keyboard layout as a list of strings.
            prefix (str): The prefix for encoding codes.

        Returns:
            tuple: A tuple containing two dictionaries:
                - encoding_dict (dict): Dictionary for encoding characters to codes.
                - decoding_dict (dict): Dictionary for decoding codes to characters.
        """
        
        encoding_dict = {}
        decoding_dict = {}

        for row_idx, row in enumerate(layout):
            for col_idx, char in enumerate(row):
                if char.strip():  # Ignore empty spaces in the layout
                    code = f"{prefix}{row_idx+1:01}x{col_idx+1:02}"
                    encoding_dict[char] = code
                    decoding_dict[code] = char

        return encoding_dict, decoding_dict
        pass

    def initialize_dictionaries(self, layout_key):
        """
        Creates dictionaries used to encode and decode for both lowercase and uppercase layouts.

        Args:
            layout_key (str): The short name for the used layout.
        
        Returns:
            tuple: A tuple containing two dictionaries:
                - encoding_dict (dict): Dictionary for encoding characters to codes.
                - decoding_dict (dict): Dictionary for decoding codes to characters.

        """

        self.layout_lowercase, self.layout_uppercase = layouts[layout_key]

        # Create encoding and decoding dictionaries for lowercase and uppercase
        lowercase_encoding_dict, lowercase_decoding_dict = self.generate_layout_dicts(EncodeDecode, self.layout_lowercase, '0')
        uppercase_encoding_dict, uppercase_decoding_dict = self.generate_layout_dicts(EncodeDecode, self.layout_uppercase, '1')

        # Merge the dictionaries for ease of use
        self.encoding_dict = {**lowercase_encoding_dict, **uppercase_encoding_dict}
        self.decoding_dict = {**lowercase_decoding_dict, **uppercase_decoding_dict}

        return(self.encoding_dict, self.decoding_dict)
        pass

    def encode_text(self, text):
        """
        Encodes the given text using the encoding dictionary.

        Args:
            text (str): The text to encode.

        Returns:
            str: The encoded text.
        """
        
        encoded_text = []
        normalized_text = unicodedata.normalize('NFD', text) # Normalize the text using NFD

        for char in normalized_text:
            if char in self.encoding_dict:
                encoded_text.append(self.encoding_dict[char])
            elif char in encode_special_mappings:
                encoded_text.append(encode_special_mappings[char])
            else:
                encoded_text.append('�') # Unknown character

        return ' '.join(encoded_text)
        pass

    def decode_text(self, encoded_text):
        """
        Decodes the given text using the decoding dictionary.

        Args:
            encoded_text (str): The text to decode.

        Returns:
            str: The decoded text.
        """

        decoded_text = []
        codes = encoded_text.split()

        for code in codes:
            if code in layouts:
                self.layout_lowercase, self.layout_uppercase = layouts[code]
                decoded_text.append(f"~{code}~")
                self.initialize_dictionaries(code)
            elif code in self.decoding_dict:
                decoded_text.append(self.decoding_dict[code])
            elif code in decode_special_mappings:
                decoded_text.append(decode_special_mappings[code])
            else:
                decoded_text.append('�') # Unknown code

        return ''.join(decoded_text)
        pass

def console_interface():
    """
    Runs the console interface for encoding and decoding text.
    """

    while True:
        layout = input("\nInsert Layout: \n").strip().lower()

        if layout in layouts:
            EncodeDecode.layout_lowercase, EncodeDecode.layout_uppercase = layouts[layout]
            EncodeDecode.initialize_dictionaries(EncodeDecode, layout)
            break
        else:
            print("\nInvalid layout. Please try again.")

    while True:
        choice = input("\nWhat would you like to do?\n 1 - encode\n 2 - decode\n 3 - switch layout\n 4 - exit\n").strip().lower()
        if choice in {'1', 'encode'}:
            choice_type = input("\nWhat would you like to encode?\n 1 - text\n 2 - file\n")
            if choice_type in {'1', 'text'}:
                text_to_encode = input("\nEnter the text to encode:\n")
            elif choice_type in {'2', 'file'}:
                file_path = input("\nEnter the file name: \n")
                try:
                    with open(file_path, 'r') as file:
                        text_to_encode = file.read()
                except FileNotFoundError:
                    print("\nFile not found. Please try again.")
                    continue
    
            encoded_text = EncodeDecode.encode_text(EncodeDecode, text_to_encode)
            print("\nEncoded Text: \n", encoded_text)
        elif choice in {'2', 'decode'}:
            choice_type = input("\nWhat would you like to decode?\n 1 - text\n 2 - file\n")
            if choice_type in {'1', 'text'}:
                text_to_decode = input("\nEnter the encoded text to decode:\n")
            elif choice_type in {'2', 'file'}:
                file_path = input("\nEnter the file name: \n")
                try:
                    with open(file_path, 'r') as file:
                        text_to_decode = file.read()
                except FileNotFoundError:
                    print("\nFile not found. Please try again.")
                    continue

            decoded_text = EncodeDecode.decode_text(EncodeDecode, text_to_decode)
            print("\nDecoded Text:\n", decoded_text)
        elif choice in {'3', 'switch'}:
            return console_interface()
        elif choice in {'4', 'exit'}:
            print("Exiting the program.")
            break
        else:
            print("\nInvalid input. Please try again")

class MainWindow(QWidget): # GUI interface
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
        self.dropdown.addItem('Arabic', 'ar')
        self.dropdown.addItem('AZERTY', 'ay')
        self.dropdown.addItem('Colemak', 'ck')
        self.dropdown.addItem('Dvorak', 'dk')
        self.dropdown.addItem('Greek', 'gr')
        self.dropdown.addItem('Hebrew', 'he')
        self.dropdown.addItem('HCESAR', 'hr')
        self.dropdown.addItem('JCUKEN', 'jn')
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

        self.submit_button.clicked.connect(self.handle_submit)
        self.reset_button.clicked.connect(self.handle_reset)

        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.reset_button)

        # Add layouts to the main layout
        main_layout.addLayout(dropdown_layout)
        main_layout.addLayout(radio_layout)
        main_layout.addWidget(self.textbox)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def handle_submit(self):
        layout_key = self.dropdown.currentData()
        text = self.textbox.toPlainText()

        EncodeDecode.layout_lowercase, EncodeDecode.layout_uppercase = layouts[layout_key]
        
        EncodeDecode.initialize_dictionaries(EncodeDecode, layout_key)
        
        if self.encode_radio.isChecked():
            encoded_text = EncodeDecode.encode_text(EncodeDecode, text)
            print(encoded_text)
            self.textbox.setText(encoded_text)
        elif self.decode_radio.isChecked():
            decoded_text = EncodeDecode.decode_text(EncodeDecode, text)
            print(decoded_text)
            self.textbox.setText(decoded_text)

    def handle_reset(self):
        self.dropdown.setCurrentIndex(0)
        self.encode_radio.setChecked(True)
        self.textbox.clear()

def main(): # Main function to determine which interface to run
    if len(sys.argv) <= 1:
        print("No argument provided. Use '-h' or '--help' for usage information.\n")
    else:
        argument = sys.argv[1].lower()  # Ensure case-insensitive handling
        if argument in ("-g", "--graphical"):
            app = QApplication(sys.argv)
            window = MainWindow()
            window.show()
            sys.exit(app.exec_())
        elif argument in ("-c", "--console"):
            console_interface()
        elif argument in ("-h", "--help"):
            print('Usage:\n -g, --graphical: Launch the application in graphical user interface (GUI) mode.\n -c, --console:   Run the application in console mode.\n -h, --help:      Display this help message.')
        else:
            print(f"Unknown argument: '{argument}'. Use '-h' or '--help' for valid options.\n")

if __name__ == "__main__":
    main()