import sys
import unicodedata
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QRadioButton, QTextEdit, QPushButton, QButtonGroup, QMessageBox
from layouts import *  # Keyboard layouts from layouts.py

class EncodeDecode:
    def __init__(self, layouts, encode_special_mappings, decode_special_mappings):
        self.layouts = layouts
        self.encode_special_mappings = encode_special_mappings
        self.decode_special_mappings = decode_special_mappings
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

    def initialize_layout_dictionaries(self, layout_key):
        """
        Creates dictionaries used to encode and decode for both lowercase and uppercase layouts.

        Args:
            layout_key (str): The short name for the used layout.
        
        Returns:
            tuple: A tuple containing two dictionaries:
                - encoding_dict (dict): Dictionary for encoding characters to codes.
                - decoding_dict (dict): Dictionary for decoding codes to characters.

        """
        self.layout_lowercase, self.layout_uppercase = self.layouts[layout_key]

        lowercase_encoding_dict, lowercase_decoding_dict = self.generate_layout_dicts(self.layout_lowercase, '0')
        uppercase_encoding_dict, uppercase_decoding_dict = self.generate_layout_dicts(self.layout_uppercase, '1')

        self.encoding_dict = {**lowercase_encoding_dict, **uppercase_encoding_dict}
        self.decoding_dict = {**lowercase_decoding_dict, **uppercase_decoding_dict}

    def encode_text(self, text):
        """
        Encodes the given text using the encoding dictionary.

        Args:
            text (str): The text to encode.

        Returns:
            str: The encoded text.
        """
        encoded_text = []
        normalized_text = unicodedata.normalize('NFD', text)  # Normalize the text using NFD

        for char in normalized_text:
            if char in self.encoding_dict:
                encoded_text.append(self.encoding_dict[char])
            elif char in self.encode_special_mappings:
                encoded_text.append(self.encode_special_mappings[char])
            else:
                encoded_text.append('�')  # Unknown character

        return ' '.join(encoded_text)

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
            if code in self.layouts:
                self.layout_lowercase, self.layout_uppercase = self.layouts[code]
                decoded_text.append(f"~{code}~")
                self.initialize_layout_dictionaries(code)
            elif code in self.decoding_dict:
                decoded_text.append(self.decoding_dict[code])
            elif code in self.decode_special_mappings:
                decoded_text.append(self.decode_special_mappings[code])
            else:
                decoded_text.append('�')  # Unknown code

        return ''.join(decoded_text)

def console_interface(layouts, encode_special_mappings, decode_special_mappings):
    """
    Runs the console interface for encoding and decoding text.

    Args:
        encode_special_mappings (): 
        decode_special_mappings (): 
    """
    encoder_decoder = EncodeDecode(layouts, encode_special_mappings, decode_special_mappings)

    while True:
        layout = input("\nInsert Layout: \n").strip().lower()

        if layout in layouts:
            encoder_decoder.initialize_layout_dictionaries(layout)
            break
        else:
            handle_error('InvalidLayoutError')

    while True:
        choice = input("\nWhat would you like to do?\n 1 - encode\n 2 - decode\n 3 - switch layout\n 4 - exit\n").strip().lower()
        if choice in {'1', 'encode'}:
            text_to_encode = get_input_text("encode")
            try:
                encoded_text = encoder_decoder.encode_text(text_to_encode)
                print("\nEncoded Text: \n", encoded_text)
            except Exception as error:
                handle_error(error)
        elif choice in {'2', 'decode'}:
            text_to_decode = get_input_text("decode")
            try:
                decoded_text = encoder_decoder.decode_text(text_to_decode)
                print("\nDecoded Text:\n", decoded_text)
            except Exception as error:
                handle_error(error)
        elif choice in {'3', 'switch'}:
            layout = input("\nInsert Layout: \n").strip().lower()
            if layout in layouts:
                encoder_decoder.initialize_layout_dictionaries(layout)
            else:
                handle_error('InvalidLayoutError')
        elif choice in {'4', 'exit'}:
            print("Exiting the program.")
            break
        else:
            handle_error("InvalidInputError")

def get_input_text(operation):
    choice_type = input(f"\nWhat would you like to {operation} \n 1 - text\n 2 - file\n").strip().lower()
    if choice_type in {'1', 'text'}:
        return input(f"\nEnter the text to {operation}:\n")
    elif choice_type in {'2', 'file'}:
        file_path = input("\nEnter the file name: \n")
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except Exception as error:
            handle_error(error)
    else:
        handle_error("InvalidInputError")

class MainWindow(QWidget):  # GUI interface
    def __init__(self, layouts, encode_special_mappings, decode_special_mappings):
        super().__init__()
        self.encoder_decoder = EncodeDecode(layouts, encode_special_mappings, decode_special_mappings)
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
        self.populate_dropdown()

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

    def populate_dropdown(self):
        for name, key in [('Arabic', 'ar'), ('AZERTY', 'ay'), ('Colemak', 'ck'), ('Dvorak', 'dk'), ('Greek', 'gr'), ('Hebrew', 'he'), ('HCESAR', 'hr'), ('JCUKEN', 'jn'), ('QWERTY', 'qy'), ('QWERTZ', 'qz'), ('Workman', 'wn')]:
            self.dropdown.addItem(name, key)

    def handle_submit(self):
        layout_key = self.dropdown.currentData()
        input_text = self.textbox.toPlainText()

        try:
            self.encoder_decoder.initialize_layout_dictionaries(layout_key)

            if self.encode_radio.isChecked():
                output_text = self.encoder_decoder.encode_text(input_text)
            elif self.decode_radio.isChecked():
                output_text = self.encoder_decoder.decode_text(input_text)
            
            self.textbox.setText(output_text)

        except Exception as error:
            handle_error(error)
            self.show_message("Error", "An error occurred during processing.")

    def handle_reset(self):
        self.dropdown.setCurrentIndex(0)
        self.encode_radio.setChecked(True)
        self.textbox.clear()

    def show_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

def handle_error(error):
    errors = {
        FileNotFoundError:      "File not found. Please try again.",
        IndexError:             "No argument provided. Use '-h' or '--help' for usage information.",
        'InvalidArgumentError': "Invalid argument. Use '-h' or '--help' for help.",
        'InvalidInputError':    "Invalid input. Please try again.",
        'InvalidLayoutError':   "Invalid layout. Please try again.",
        UnboundLocalError:      "Cannot access local variable. This may be caused by invalid input."
    }

    if isinstance(error, Exception):
        print(f"{type(error).__name__}: {errors.get(type(error), str(error))}")
    elif isinstance(error, str):
        print(f"{error}: {errors.get(error, 'An unknown error occurred.')}")
    else:
        print("Error: An unknown error occurred.")

def main():
    """
    Determine which interface to run.
    """
    try:
        argument = sys.argv[1].lower()  # Ensure case-insensitive handling
        if argument in ("-g", "--graphical"):
            app = QApplication(sys.argv)
            window = MainWindow(layouts, encode_special_mappings, decode_special_mappings)
            window.show()
            sys.exit(app.exec_())
        elif argument in ("-c", "--console"):
            console_interface(layouts, encode_special_mappings, decode_special_mappings)
        elif argument in ("-h", "--help"):
            print('Usage:\n -g, --graphical: Launch the application in graphical user interface (GUI) mode.\n -c, --console:   Run the application in console mode.\n -h, --help:      Display this help message.')
        else:
            handle_error('InvalidArgumentError')
    except Exception as error:
        handle_error(error)

if __name__ == "__main__":
    main()
