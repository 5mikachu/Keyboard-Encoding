import logging
import sys
import unicodedata
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QRadioButton, QTextEdit, QPushButton, QButtonGroup, QMessageBox,
)
from layouts import KeyboardLayouts
from config import GeneralConfig, ConsoleConfig, GUIConfig


class EncodeDecode:
    def __init__(self):
        self.layouts = KeyboardLayouts
        self.encode_special_mappings, self.decode_special_mappings = self.layouts.get_special_mappings()
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
        """
        if layout_key in self.encoding_dict:
            return  # Avoid reinitializing if already done

        try:
            self.layout_lowercase, self.layout_uppercase = self.layouts.get_layout(layout_key)
        except ValueError as e:
            logging.error(str(e))
            raise ValueError(str(e))

        # Initialize encoding and decoding dictionaries
        for prefix, layout in (('0', self.layout_lowercase), ('1', self.layout_uppercase)):
            for row_idx, row in enumerate(layout):
                for col_idx, char in enumerate(row):
                    if char.strip():  # Ignore empty spaces in the layout
                        code = f"{prefix}{row_idx+1:01}x{col_idx+1:02}"
                        self.encoding_dict[char] = code
                        self.decoding_dict[code] = char

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
                logging.warning(f"Unknown character encountered: {char}")
                encoded_text.append('�')

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
            if code in self.layouts.list_layouts():  # Switch layout
                self.layout_lowercase, self.layout_uppercase = self.layouts.get_layout(code)
                decoded_text.append(f"~{code}~")
                self.initialize_layout_dictionaries(code)
            elif code in self.decoding_dict:
                decoded_text.append(self.decoding_dict[code])
            elif code in self.decode_special_mappings:
                decoded_text.append(self.decode_special_mappings[code])
            else:
                logging.warning(f"Unknown code encountered: {code}")
                decoded_text.append('�')

        return ''.join(decoded_text)


class ConsoleInterface:
    def __init__(self):
        self.encoder_decoder = EncodeDecode()
        self.valid_layouts = {key for key, _ in KeyboardLayouts.list_layouts()}

    def main(self):
        """
        Runs the console interface for encoding and decoding text.
        """
        if GeneralConfig.default_layout is not None:
            self.encoder_decoder.initialize_layout_dictionaries(GeneralConfig.default_layout)
        else:
            self.handle_choose_layout()
        
        actions = {
            '1': self.handle_encode,
            'encode': self.handle_encode,
            '2': self.handle_decode,
            'decode': self.handle_decode,
            '3': self.handle_choose_layout,
            'switch layout': self.handle_choose_layout,
            '4': self.handle_add_layout,
            'add layout': self.handle_add_layout,
            '5': self.handle_switch_to_gui,
            'switch to gui': self.handle_switch_to_gui,
            '6': self.handle_exit_program,
            'exit': self.handle_exit_program
        }

        while True:
            choice = input("\nWhat would you like to do?\n"
                           " 1 - encode\n"
                           " 2 - decode\n"
                           " 3 - switch layout\n"
                           " 4 - add layout\n"
                           " 5 - switch to GUI\n"
                           " 6 - exit\n").strip().lower()

            action = actions.get(choice)
            if action:
                action()
            else:
                logging.info("Invalid input. Please try again.")

    def handle_encode(self):
        text_to_encode = self.get_input_text("encode")

        try:
            encoded_text = self.encoder_decoder.encode_text(text_to_encode)
            print("\nEncoded Text:\n", encoded_text)
        except Exception:
            logging.error("Error during encoding", exc_info=True)

    def handle_decode(self):
        text_to_decode = self.get_input_text("decode")

        try:
            decoded_text = self.encoder_decoder.decode_text(text_to_decode)
            print("\nDecoded Text:\n", decoded_text)
        except Exception:
            logging.error("Error during decoding", exc_info=True)

    def handle_choose_layout(self):
        while True:
            layout = input("\nInsert Layout:\n").strip().lower()

            if layout in self.valid_layouts:
                self.encoder_decoder.initialize_layout_dictionaries(layout)
                break
            elif layout == 'add layout':
                self.handle_add_layout()
            else:
                logging.info("Invalid layout. Please try again.")

    def handle_add_layout(self):
        key = input("\nLayout key:  ").strip().lower()
        name = input("Layout name: ").strip()

        lowercase = self.get_layout_input("lowercase")
        uppercase = self.get_layout_input("uppercase")

        try:
            KeyboardLayouts.add_layout(key, name, lowercase, uppercase)
            logging.info(f"Layout '{name}' added successfully.")
        except ValueError as e:
            logging.error(str(e))

    def handle_switch_to_gui(self):
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())

    def handle_exit_program(self):
        print("Exiting the program.")
        sys.exit(0)

    def get_layout_input(self, case_type):
        layout = []
        row_number = 1

        while True:
            row = input(f"Enter row {row_number} for {case_type}: ").strip()
            row_number += 1
            
            if not row or row_number > ConsoleConfig.max_row_num:
                row_number == 1
                break
            layout.append(list(row))
        return layout

    def get_input_text(self, operation):
        actions = {
            '1': self.get_input_from_text,
            'text': self.get_input_from_text,
            '2': self.get_input_from_file,
            'file': self.get_input_from_file
        }
        
        if ConsoleConfig.skip_input_type == True:
            return  self.get_input_from_text(operation)
        else:
            choice_type = input(f"\nWhat would you like to {operation}\n"
                                 " 1 - text\n"
                                 " 2 - file\n").strip().lower()
            
            action = actions.get(choice_type)
            if action:
                return  action(operation)
            else:
                logging.info("Invalid input. Please try again.")
                return self.get_input_text(operation)
        
    def get_input_from_text(self, operation):
        return input(f"\nEnter the text to {operation}:\n")
    
    def get_input_from_file(self, operation):
        file_path = input(f"\nEnter the file to {operation}: \n")
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            logging.error("File not found. Please try again.")
        except Exception:
            logging.error("Error reading file", exc_info=True)
 

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.encoder_decoder = EncodeDecode()
        if GeneralConfig.default_layout != None:
            self.default_layout = KeyboardLayouts.get_layout_name(GeneralConfig.default_layout)
        else:
            self.default_layout = 'QWERTY'
        self.initUI()
        self.handle_reset()

    def initUI(self):
        self.setWindowTitle('Keyboard Encoding')

        # Layouts
        main_layout = QVBoxLayout()
        dropdown_layout = QHBoxLayout()
        radio_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # Layout dropdown
        self.dropdown = QComboBox()
        for key, name in self.encoder_decoder.layouts.list_layouts():
            self.dropdown.addItem(name, key)

        dropdown_label = QLabel('Keyboard Layout:')
        dropdown_layout.addWidget(dropdown_label)
        dropdown_layout.addWidget(self.dropdown)

        # Radio buttons
        self.encode_radio = QRadioButton('Encode')
        self.decode_radio = QRadioButton('Decode')

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
        input_text = self.textbox.toPlainText()

        try:
            self.encoder_decoder.initialize_layout_dictionaries(layout_key)

            if self.encode_radio.isChecked():
                output_text = self.encoder_decoder.encode_text(input_text)
            elif self.decode_radio.isChecked():
                output_text = self.encoder_decoder.decode_text(input_text)
            
            self.show_message("Output", output_text)

        except Exception:
            logging.error("Error during processing", exc_info=True)
            self.show_message("Error", "An error occurred during processing.")

    def handle_reset(self):
        self.dropdown.setCurrentIndex(0)
        self.encode_radio.setChecked(GUIConfig.default_operation == 'encode')
        self.decode_radio.setChecked(GUIConfig.default_operation == 'decode')
        self.dropdown.setCurrentText(self.default_layout)
        self.textbox.clear()

    def show_message(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()


def validate_config():
    # Validate GeneralConfig.default_layout
    valid_layouts = {key for key, _ in KeyboardLayouts.list_layouts()}
    if GeneralConfig.default_layout not in valid_layouts:
        GeneralConfig.default_layout = None
        logging.info("Invalid layout in config. Setting to None.")

    # Validate ConsoleConfig.max_row_num
    try:
        ConsoleConfig.max_row_num = int(ConsoleConfig.max_row_num)
    except (TypeError, ValueError):
        ConsoleConfig.max_row_num = 4
        logging.info("Invalid number of rows provided in config. Setting to default 4.")

    # Validate ConsoleConfig.skip_input_type
    if not isinstance(ConsoleConfig.skip_input_type, bool):
        ConsoleConfig.skip_input_type = False
        logging.info("Invalid argument for skip_input_type. Setting to default False.")


def main():
    """
    Determine which interface to run.
    """
    try:
        argument = sys.argv[1].lower()
        if argument in ("-g", "--graphical"):
            app = QApplication(sys.argv)
            window = MainWindow()
            window.show()
            sys.exit(app.exec_())
        elif argument in ("-c", "--console"):
            ConsoleInterface().main()
        elif argument in ("-h", "--help"):
            print("Usage:\n"
                  " -g, --graphical: Launch the application in graphical user interface (GUI) mode.\n"
                  " -c, --console:   Run the application in console mode.\n"
                  " -h, --help:      Display this help message.")
        else:
            logging.info("Invalid argument. Use '-h' or '--help' for help.")
    except IndexError:
        logging.error("No argument provided. Use '-h' or '--help' for usage information.")
    except Exception:
        logging.error("Unexpected error occurred", exc_info=True)


if __name__ == "__main__":
    # Setting up logging for error tracking and debugging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    validate_config()

    main()
