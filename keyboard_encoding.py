import json
import logging
import sys
import unicodedata
from configparser import ConfigParser
from typing import List, Tuple, Dict, Union
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QRadioButton, QTextEdit, QPushButton, QButtonGroup, QMessageBox,
)
from PyQt5.QtGui import QIcon


class EncodeDecode:
    def __init__(self, layouts: 'LayoutFunctions') -> None:
        """
        Initialize the EncodeDecode class.

        Args:
            layouts (LayoutFunctions): An instance of the LayoutFunctions class.
        """
        self.layout_functions = LayoutFunctions()
        self.layouts = layouts
        self.encode_special_mappings, self.decode_special_mappings = self.layouts.get_special_mappings()
        self.encoding_dict: Dict[str, str] = {}
        self.decoding_dict: Dict[str, str] = {}
        self.layout_lowercase: List[List[str]] = []
        self.layout_uppercase: List[List[str]] = []

    def initialize_layout_dictionaries(self, layout_key: str) -> None:
        """
        Creates dictionaries used to encode and decode for both lowercase and uppercase layouts.

        Args:
            layout_key (str): The short name for the used layout.
        """
        if layout_key in self.encoding_dict:
            return  # Use cached dictionaries

        self.layout_lowercase, self.layout_uppercase = self.layouts.get_layout(layout_key)

        # Initialize encoding and decoding dictionaries
        for prefix, layout in (('0', self.layout_lowercase), ('1', self.layout_uppercase)):
            for row_idx, row in enumerate(layout):
                for col_idx, char in enumerate(row):
                    if char.strip():  # Ignore empty spaces in the layout
                        code = f"{prefix}{row_idx+1:01}x{col_idx+1:02}"
                        self.encoding_dict[char] = code
                        self.decoding_dict[code] = char

    def encode_text(self, text: str) -> str:
        """
        Encodes the given text using the encoding dictionary.

        Args:
            text (str): The text to encode.

        Returns:
            str: The encoded text.
        """
        encoded_text: List[str] = []
        normalized_text = unicodedata.normalize('NFD', text)  # Normalize the text using NFD

        i = 0
        while i < len(normalized_text):
            char = normalized_text[i]

            # Check if the code matches a layout key to switch layouts
            if char == '~':
                end_marker = normalized_text.find('~', i + 1)
                key = normalized_text[i + 1:end_marker]
                if key in dict(self.layout_functions.list_layouts()):
                    self.initialize_layout_dictionaries(key)
                    encoded_text.append(key)
                    i = end_marker + 1
            elif char in self.encoding_dict or self.encode_special_mappings:
                encoded_text.append(
                    self.encoding_dict.get(char) or 
                    self.encode_special_mappings.get(char)
                )
            else:
                logging.warning(f"Unknown character encountered: {char}")
                encoded_text.append('�')

            i += 1
        return ' '.join(encoded_text)

    def decode_text(self, encoded_text: str) -> str:
        """
        Decodes the given text using the decoding dictionary.

        Args:
            encoded_text (str): The text to decode.

        Returns:
            str: The decoded text.
        """
        decoded_text: List[str] = []
        codes = encoded_text.split()

        for code in codes:
            # Check if the code matches a layout key to switch layouts
            if code in dict(self.layout_functions.list_layouts()):
                self.initialize_layout_dictionaries(code)
                decoded_text.append(f"~{code}~")
            elif code in self.decoding_dict or self.decode_special_mappings:
                decoded_text.append(
                    self.decoding_dict.get(code) or 
                    self.decode_special_mappings.get(code)
                )
            else:
                logging.warning(f"Unknown code encountered: {code}")
                decoded_text.append('�')
        return ''.join(decoded_text)


class LayoutFunctions:
    def __init__(self) -> None:
        """
        Initialize the LayoutFunctions class.
        """
        self.layouts = self.load_layouts()

    def load_layouts(self) -> Dict[str, Dict[str, Union[str, List[List[str]]]]]:
        """
        Load layouts from the JSON file.

        Returns:
            dict: The loaded layouts.
        """
        try:
            with open('layouts.json', 'r', encoding='utf-8') as file:
                layouts = json.load(file)
            return layouts
        except FileNotFoundError:
            logging.error("layouts.json file not found.")
            return {}
        except json.JSONDecodeError:
            logging.error("Error decoding layouts.json file.")
            return {}

    def get_layout(self, key: str) -> Tuple[List[List[str]], List[List[str]]]:
        """
        Retrieve the layout (both lowercase and uppercase) by its key.

        Args:
            key (str): The key for the desired layout (e.g., 'qy' for QWERTY).

        Returns:
            tuple: A tuple containing two lists, the lowercase and uppercase layouts.

        Raises:
            ValueError: If the layout with the specified key is not found.
        """
        layout = self.layouts.get(key)
        if layout:
            return layout['lowercase'], layout['uppercase']
        raise ValueError(f"Layout with key '{key}' not found")

    def get_layout_name(self, key: str) -> str:
        """
        Retrieve the name by its key.

        Args:
            key (str): The key for the desired layout (e.g., 'qy' for QWERTY).

        Returns:
            str: The human-readable name of the layout.

        Raises:
            ValueError: If the layout with the specified key is not found.
        """
        layout = self.layouts.get(key)
        if layout:
            return layout['name']
        raise ValueError(f"Layout with key '{key}' not found")

    def list_layouts(self) -> List[Tuple[str, str]]:
        """
        List all available keyboard layouts.

        Returns:
            list: A list of tuples containing the key and name of all layouts.
        """
        return [(key, layout['name']) for key, layout in self.layouts.items()]

    def add_layout(self, key: str, name: str, lowercase: List[List[str]], uppercase: List[List[str]]) -> None:
        """
        Add a new keyboard layout.

        Args:
            key (str): The key for the new layout (e.g., 'ck' for Colemak).
            name (str): The human-readable name of the layout.
            lowercase (list): A list of lists representing the lowercase keys.
            uppercase (list): A list of lists representing the uppercase keys.

        Raises:
            ValueError: If a layout with the given key already exists.
        """
        if key in self.layouts:
            raise ValueError(f"Layout with key '{key}' already exists")

        self.layouts[key] = {
            'name': name,
            'lowercase': lowercase,
            'uppercase': uppercase
        }

        with open('layouts.json', 'w', encoding='utf-8') as file:
            json.dump(self.layouts, file, indent=4)

    def get_special_mappings(self) -> Tuple[Dict[str, str], Dict[str, str]]:
        """
        Retrieve the special character mappings from a JSON file.

        Returns:
            tuple: A tuple containing two dictionaries, the encode and decode special mappings.
        """
        try:
            with open('special_mappings.json', 'r', encoding='utf-8') as file:
                encode_special_mappings = json.load(file)

            # Create the decode mapping by reversing the encode mapping
            decode_special_mappings = {v: k for k, v in encode_special_mappings.items()}

            return encode_special_mappings, decode_special_mappings

        except FileNotFoundError:
            logging.error(f"Special mappings file not found.")
            return {}, {}
        except json.JSONDecodeError:
            logging.error(f"Error decoding the special mappings file.")
            return {}, {}
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return {}, {}


class ConsoleInterface:
    def __init__(self, config: ConfigParser, layouts: LayoutFunctions) -> None:
        """
        Initialize the ConsoleInterface class.

        Args:
            config (ConfigParser): The configuration parser instance.
            layouts (LayoutFunctions): An instance of the LayoutFunctions class.
        """
        self.encoder_decoder = EncodeDecode(layouts)
        self.layout_functions = layouts
        self.valid_layouts: set = {key for key, _ in self.layout_functions.list_layouts()}
        self.config = config
        self.startup = Startup()

    def main(self) -> None:
        """
        Runs the console interface for encoding and decoding text.
        """
        default_layout = self.config.get('GeneralConfig', 'default_layout', fallback=None)
        if default_layout is not None:
            self.encoder_decoder.initialize_layout_dictionaries(default_layout)
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
            '5': self.startup.start_graphical,
            'switch to gui': self.startup.start_graphical,
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

    def handle_encode(self) -> None:
        """
        Handle the encoding operation.
        """
        text_to_encode = self.get_input_text("encode")

        if not text_to_encode:
            logging.error("No text provided for encoding.")
            return

        try:
            encoded_text = self.encoder_decoder.encode_text(text_to_encode)
            print("\nEncoded Text:\n", encoded_text)
        except Exception as e:
            logging.error("Error during encoding", exc_info=True)
            print(f"An error occurred during encoding: {e}")

    def handle_decode(self) -> None:
        """
        Handle the decoding operation.
        """
        text_to_decode = self.get_input_text("decode")

        if not text_to_decode:
            logging.error("No text provided for decoding.")
            return

        try:
            decoded_text = self.encoder_decoder.decode_text(text_to_decode)
            print("\nDecoded Text:\n", decoded_text)
        except Exception as e:
            logging.error("Error during decoding", exc_info=True)
            print(f"An error occurred during decoding: {e}")

    def handle_choose_layout(self) -> None:
        """
        Handle the layout selection operation.
        """
        retry_count: int = self.config.getint('ConsoleConfig', 'prompt_for_retries', fallback=3)

        while retry_count > 0:
            layout = input("\nInsert Layout:\n").strip().lower()

            if layout in self.valid_layouts:
                self.encoder_decoder.initialize_layout_dictionaries(layout)
                break
            elif layout == 'add layout':
                self.handle_add_layout()
            else:
                logging.info("Invalid layout. Please try again.")
                retry_count -= 1

        if retry_count == 0:
            logging.error("Exceeded maximum retries for selecting layout.")

    def handle_add_layout(self) -> None:
        """
        Handle the operation to add a new layout.
        """
        key = input("\nLayout key:  ").strip().lower()
        name = input("Layout name: ").strip()

        lowercase = self.get_layout_input("lowercase")
        uppercase = self.get_layout_input("uppercase")

        try:
            self.layout_functions.add_layout(key, name, lowercase, uppercase)
            logging.info(f"Layout '{key}', '{name}' added successfully.")
        except ValueError as e:
            logging.error(str(e))

    def handle_exit_program(self) -> None:
        """
        Handle the operation to exit the program.
        """
        print("Exiting the program.")
        sys.exit(0)

    def get_layout_input(self, case_type: str) -> List[List[str]]:
        """
        Get layout input from the user.

        Args:
            case_type (str): Either 'lowercase' or 'uppercase'.

        Returns:
            list: A list representing the layout.
        """
        max_row_num: int = self.config.getint('ConsoleConfig', 'max_row_num', fallback=4)
        layout: List[List[str]] = []
        row_number: int = 1

        while True:
            row = input(f"Enter row {row_number} for {case_type}: ").strip()
            row_number += 1

            if not row or row_number > max_row_num:
                row_number = 1
                break
            layout.append(list(row))
        return layout

    def get_input_text(self, operation: str) -> str:
        """
        Get the input text for encoding or decoding.

        Args:
            operation (str): Either 'encode' or 'decode'.

        Returns:
            str: The input text.
        """
        skip_input_type: bool = self.config.getboolean('ConsoleConfig', 'skip_input_type', fallback=False)
        actions = {
            '1': self.get_input_from_text,
            'text': self.get_input_from_text,
            '2': self.get_input_from_file,
            'file': self.get_input_from_file
        }

        if skip_input_type:
            return self.get_input_from_text(operation)
        else:
            choice_type = input(f"\nWhat would you like to {operation}\n"
                                 " 1 - text\n"
                                 " 2 - file\n").strip().lower()

            action = actions.get(choice_type)
            if action:
                return action(operation)
            else:
                logging.info("Invalid input. Please try again.")
                return self.get_input_text(operation)

    def get_input_from_text(self, operation: str) -> str:
        """
        Get input directly from user as text.

        Args:
            operation (str): Either 'encode' or 'decode'.

        Returns:
            str: The input text.
        """
        return input(f"\nEnter the text to {operation}:\n")

    def get_input_from_file(self, operation: str) -> Union[str, None]:
        """
        Get input from a file.

        Args:
            operation (str): Either 'encode' or 'decode'.

        Returns:
            str: The content of the file as a string.
        """
        file_path = input(f"\nEnter the file to {operation}: \n")
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            logging.error("File not found. Please try again.")
        except Exception:
            logging.error("Error reading file", exc_info=True)
        return None


class MainWindow(QWidget):
    def __init__(self, config: ConfigParser, layouts: LayoutFunctions) -> None:
        """
        Initialize the MainWindow class.

        Args:
            config (ConfigParser): The configuration parser instance.
            layouts (LayoutFunctions): An instance of the LayoutFunctions class.
        """
        super().__init__()
        self.encoder_decoder = EncodeDecode(layouts)
        self.layout_functions = layouts
        self.default_layout: str = self.layout_functions.get_layout_name(config.get('GeneralConfig', 'default_layout', fallback='qy'))
        self.config = config
        self.apply_theme()
        self.init_UI()
        self.handle_reset()

    def init_UI(self) -> None:
        """
        Initialize the UI components of the main window.
        """
        self.setWindowTitle('Keyboard Encoding')
        self.setWindowIcon(QIcon('./icon.svg'))

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

    def handle_submit(self) -> None:
        """
        Handle the submission of text for encoding or decoding.
        """
        layout_key = self.dropdown.currentData()
        input_text = self.textbox.toPlainText()

        if not input_text.strip():
            self.show_message("Error", "Input text cannot be empty.")
            return

        try:
            self.encoder_decoder.initialize_layout_dictionaries(layout_key)

            if self.encode_radio.isChecked():
                output_text = self.encoder_decoder.encode_text(input_text)
            elif self.decode_radio.isChecked():
                output_text = self.encoder_decoder.decode_text(input_text)
            else:
                self.show_message("Error", "Please select an operation (encode/decode).")
                return

            self.show_message("Output", output_text)
        except Exception as e:
            logging.error("Error during processing", exc_info=True)
            self.show_message("Error", f"An error occurred during processing: {e}")

    def handle_reset(self) -> None:
        """
        Handle the reset operation of the UI.
        """
        default_operation = self.config.get('GUIConfig', 'default_operation', fallback='encode')
        self.encode_radio.setChecked(default_operation == 'encode')
        self.decode_radio.setChecked(default_operation == 'decode')
        self.dropdown.setCurrentText(self.default_layout)
        self.textbox.clear()

    def show_message(self, title: str, message: str) -> None:
        """
        Display a message box with the specified title and message.

        Args:
            title (str): The title of the message box.
            message (str): The message to display.
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.addButton("Copy", QMessageBox.ActionRole)  # Add the Copy button
        msg_box.addButton(QMessageBox.Close)  # Add the OK button

        msg_box.buttonClicked.connect(lambda button: self.copy_to_clipboard(button, message))
      
        msg_box.exec_()

    def copy_to_clipboard(self, button: 'QAbstractButton', message: str) -> None:
        """
        Copy the provided message to the clipboard if the "Copy" button is clicked.

        Args:
            button (QAbstractButton): The button clicked by the user.
            message (str): The message to copy to the clipboard.
        """
        if button.text() == "Copy":
            clipboard = QApplication.clipboard()
            clipboard.setText(message)

    def apply_theme(self) -> None:
        """
        Apply the selected theme to the UI.
        """
        width: int = self.config.getint('GUIConfig', 'window_width', fallback=500)
        height: int = self.config.getint('GUIConfig', 'window_height', fallback=400)
        theme: str = self.config.get('GUIConfig', 'theme', fallback='light')
        themes = {
            'dark': "background-color: #2E2E2E; color: white;",
            'light': "background-color: white; color: black;"
        }

        self.resize(width, height)
        self.setStyleSheet(themes.get(theme))


class Startup:
    def __init__(self) -> None:
        """
        Initialize the Startup class.
        """
        self.layout_functions = LayoutFunctions()
        self.config = ConfigParser()
        self.config.read('config.ini')
        self.setup_logging()
        self.validate_config()

    def setup_logging(self) -> None:
        """
        Setup the logging configuration.
        """
        log_level_str: str = self.config.get('GeneralConfig', 'logging_level', fallback='INFO').upper()
        log_level = getattr(logging, log_level_str, logging.INFO)
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

    def validate_config(self) -> None:
        """
        Validate the configuration settings and set defaults if necessary.
        """
        # Validate GeneralConfig default_layout
        valid_layouts: set = {key for key, _ in self.layout_functions.list_layouts()}
        default_layout: str = self.config.get('GeneralConfig', 'default_layout', fallback=None)
        if default_layout not in valid_layouts:
            self.config.set('GeneralConfig', 'default_layout', 'qy')
            logging.info("Invalid layout in config. Setting to QWERTY.")

        # Validate ConsoleConfig max_row_num
        max_row_num: int = self.config.getint('ConsoleConfig', 'max_row_num', fallback=4)
        if not isinstance(max_row_num, int):
            self.config.set('ConsoleConfig', 'max_row_num', '4')
            logging.info("Invalid number of rows provided in config. Setting to default 4.")

        # Validate ConsoleConfig skip_input_type
        skip_input_type: bool = self.config.getboolean('ConsoleConfig', 'skip_input_type', fallback=False)
        if not isinstance(skip_input_type, bool):
            self.config.set('ConsoleConfig', 'skip_input_type', 'False')
            logging.info("Invalid argument for skip_input_type. Setting to default False.")

        # Validate GUIConfig default_operation
        default_operation: str = self.config.get('GUIConfig', 'default_operation', fallback='encode')
        if default_operation not in ('encode', 'decode'):
            self.config.set('GUIConfig', 'default_operation', 'encode')
            logging.info("Invalid argument for default_operation. Setting to default Encode.")

        # Validate GUIConfig theme
        theme: str = self.config.get('GUIConfig', 'theme', fallback='light')
        if theme not in ('dark', 'light'):
            self.config.set('GUIConfig', 'theme', 'light')
            logging.info("Invalid argument for theme. Setting to Light")

        # Validate GUIConfig window_width
        window_width: int = self.config.getint('GUIConfig', 'window_width', fallback='400')
        if not isinstance(window_width, int):
            self.config.set('GUIConfig', 'window_width', '400')
            logging.info("Invalid argument for window_width. Setting to 400")

        # Validate GUIConfig window_height
        window_height: int = self.config.getint('GUIConfig', 'window_height', fallback='400')
        if not isinstance(window_height, int):
            self.config.set('GUIConfig', 'window_height', '400')
            logging.info("Invalid argument for window_height. Setting to 400")

    def start_graphical(self) -> None:
        """
        Start the graphical user interface (GUI).
        """
        app = QApplication(sys.argv)
        window = MainWindow(self.config, self.layout_functions)
        window.show()
        sys.exit(app.exec_())

    def help(self) -> None:
        """
        Display usage help for the command-line interface.
        """
        print("Usage:\n"
                " -g, --graphical: Launch the application in graphical user interface (GUI) mode.\n"
                " -c, --console:   Run the application in console mode.\n"
                " -h, --help:      Display this help message."
        )

    def main(self) -> None:
        """
        Determine which interface to run based on command-line arguments.
        """
        actions = {
            '-g': self.start_graphical,
            '--graphical': self.start_graphical,
            '-c': ConsoleInterface(self.config, self.layout_functions).main,
            '--console': ConsoleInterface(self.config, self.layout_functions).main,
            '-h': self.help,
            '--help': self.help
        }

        try:
            action = actions.get(sys.argv[1].lower())
            if action:
                action()
            else:
                logging.info("Invalid argument. Use '-h' or '--help' for help.")
        except IndexError:
            logging.error("No argument provided. Use '-h' or '--help' for usage information.")
        except Exception:
            logging.error("Unexpected error occurred", exc_info=True)


if __name__ == '__main__':
    Startup().main()
