import sys
import logging
from configparser import ConfigParser
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QRadioButton,
    QTextEdit, QPushButton, QButtonGroup, QMessageBox, QApplication
)
from encode_decode import EncodeDecode
from layout_functions import LayoutFunctions

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
        default_layout = self.config.get('GeneralConfig', 'default_layout')
        if default_layout is not None:
            self.encoder_decoder.initialize_layout_dictionaries(default_layout)
        else:
            self.handle_choose_layout()

        actions: dict[str, str] = {
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
            choice: str | int = input("\nWhat would you like to do?\n"
                           " 1 - encode\n"
                           " 2 - decode\n"
                           " 3 - switch layout\n"
                           " 4 - add layout\n"
                           " 5 - switch to GUI\n"
                           " 6 - exit\n").strip().lower()

            action: str = actions.get(choice)
            if action:
                action()
            else:
                logging.info("Invalid input. Please try again.")    

    def handle_encode(self) -> None:
        """
        Handle the encoding operation.
        """
        text_to_encode: str = self.get_input_text("encode")

        if not text_to_encode:
            logging.error("No text provided for encoding.")
            return

        try:
            encoded_text: str = self.encoder_decoder.encode_text(text_to_encode)
            print("\nEncoded Text:\n", encoded_text)
        except Exception as e:
            logging.error("Error during encoding", exc_info=True)
            print(f"An error occurred during encoding: {e}")

    def handle_decode(self) -> None:
        """
        Handle the decoding operation.
        """
        text_to_decode: str = self.get_input_text("decode")

        if not text_to_decode:
            logging.error("No text provided for decoding.")
            return

        try:
            decoded_text: str = self.encoder_decoder.decode_text(text_to_decode)
            print("\nDecoded Text:\n", decoded_text)
        except Exception as e:
            logging.error("Error during decoding", exc_info=True)
            print(f"An error occurred during decoding: {e}")

    def handle_choose_layout(self) -> None:
        """
        Handle the layout selection operation.
        """
        retry_count: int = self.config.getint('ConsoleConfig', 'prompt_for_retries')

        while retry_count > 0:
            layout: str = input("\nInsert Layout:\n").strip().lower()

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
        key: str = input("\nLayout key:  ").strip().lower()
        name: str = input("Layout name: ").strip()

        lowercase: list[list[str]] = self.get_layout_input("lowercase")
        uppercase: list[list[str]] = self.get_layout_input("uppercase")

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

    def get_layout_input(self, case_type: str) -> list[list[str]]:
        """
        Get layout input from the user.

        Args:
            case_type (str): Either 'lowercase' or 'uppercase'.

        Returns:
            layout (list): A list representing the layout.
        """
        max_row_num: int = self.config.getint('ConsoleConfig', 'max_row_num')
        layout: list[list[str]] = []

        for row_number in range(max_row_num):
            row = input(f"Enter row {row_number + 1} for {case_type}: ").strip()

            layout.append(list(row))
        return layout

    def get_input_text(self, operation: str) -> str:
        """
        Get the input text for encoding or decoding.

        Args:
            operation (str): Either 'encode' or 'decode'.

        Returns:
            input_text (str): The input text.
        """
        skip_input_type: bool = self.config.getboolean('ConsoleConfig', 'skip_input_type')
        actions: dict[str, str] = {
            '1': self.get_input_from_text,
            'text': self.get_input_from_text,
            '2': self.get_input_from_file,
            'file': self.get_input_from_file
        }

        if skip_input_type:
            return self.get_input_from_text(operation)
        else:
            choice_type: str | int = input(f"\nWhat would you like to {operation}\n"
                                 " 1 - text\n"
                                 " 2 - file\n").strip().lower()

            action: str = actions.get(choice_type)
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
            input_text (str): The input text.
        """
        return input(f"\nEnter the text to {operation}:\n")

    def get_input_from_file(self, operation: str) -> str:
        """
        Get input from a file.

        Args:
            operation (str): Either 'encode' or 'decode'.

        Returns:
            input_text (str | None): The content of the file as a string.
        """
        file_path: str = filedialog.askopenfilename(title=f'Select file to {operation}')
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            logging.error("File not found. Please try again.")


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
        self.default_layout: str = self.layout_functions.get_layout_name(config.get('GeneralConfig', 'default_layout'))
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

        # Dropdown
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
        layout_key: str = self.dropdown.currentData()
        input_text: str = self.textbox.toPlainText()

        if not input_text.strip():
            self.show_message("Error", "Input text cannot be empty.")
            logging.info("Input text cannot be empty.")
            return

        operation = 'encode' if self.encode_radio.isChecked() else \
                    'decode' if self.decode_radio.isChecked() else None
        if not operation:
            self.show_message("Error", "Please select an operation (encode/decode).")
            logging.info("Please select an operation (encode/decode).")
            return

    def handle_reset(self) -> None:
        """
        Handle the reset operation of the UI.
        """
        default_operation: str = self.config.get('GUIConfig', 'default_operation')
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
        msg_box.addButton("Copy", QMessageBox.ActionRole)
        msg_box.addButton(QMessageBox.Close)

        msg_box.buttonClicked.connect(lambda button: self.copy_to_clipboard(button, message))
        msg_box.exec_()

    def copy_to_clipboard(self, button, message: str) -> None:
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
        width: int = self.config.getint('GUIConfig', 'window_width')
        height: int = self.config.getint('GUIConfig', 'window_height')
        theme: str = self.config.get('GUIConfig', 'theme')
        themes: dict[str, str] = {
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
        try:
            self.config.getint('ConsoleConfig', 'max_row_num', fallback=4)
        except ValueError:
            self.config.set('ConsoleConfig', 'max_row_num', '4')
            logging.info("Invalid number of rows provided in config. Setting to default 4.")

        # Validate ConsoleConfig skip_input_type
        try:
            self.config.getboolean('ConsoleConfig', 'skip_input_type', fallback=False)
        except ValueError:
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
        try:
            self.config.getint('GUIConfig', 'window_width', fallback='400')
        except ValueError:
            self.config.set('GUIConfig', 'window_width', '500')
            logging.info("Invalid argument for window_width. Setting to 500")

        # Validate GUIConfig window_height
        try:
            self.config.getint('GUIConfig', 'window_height', fallback=400)
        except ValueError:
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
                logging.info("Defaulting to console interface")
                ConsoleInterface(self.config, self.layout_functions).main()
        except IndexError:
            logging.info("No argument provided. Use '-h' or '--help' for usage information.")
            logging.info("Defaulting to console interface")
            ConsoleInterface(self.config, self.layout_functions).main()
        except Exception:
            logging.error("Unexpected error occurred", exc_info=True)


if __name__ == '__main__':
    Startup().main()
