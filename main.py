import logging
import sys
from configparser import ConfigParser

from encode_decode import EncodeDecode
from layout_functions import LayoutFunctions


class ConsoleInterface:
    def __init__(self, config: ConfigParser, layouts: LayoutFunctions) -> None:
        """
        Initialize the ConsoleInterface class.

        :args:
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
                                      " 5 - exit\n").strip().lower()

            action = actions.get(choice)
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

    @staticmethod
    def handle_exit_program() -> None:
        """
        Handle the operation to exit the program.
        """
        print("Exiting the program.")
        sys.exit(0)

    def get_layout_input(self, case_type: str) -> list[list[str]]:
        """
        Get layout input from the user.

        :args:
            case_type (str): Either 'lowercase' or 'uppercase'.

        returns:
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

        :args:
            operation (str): Either 'encode' or 'decode'.

        :returns:
            input_text (str): The input text.
        """
        skip_input_type: bool = self.config.getboolean('ConsoleConfig', 'skip_input_type')
        actions: dict[str, operation: str] = {
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

            action: operation = actions.get(choice_type)
            if action:
                return action(operation)
            else:
                logging.info("Invalid input. Please try again.")
                return self.get_input_text(operation)

    @staticmethod
    def get_input_from_text(operation: str) -> str:
        """
        Get input directly from user as text.

        :args:
            operation (str): Either 'encode' or 'decode'.

        :returns:
            input_text (str): The input text.
        """
        return input(f"\nEnter the text to {operation}:\n")

    @staticmethod
    def get_input_from_file(operation: str) -> str:
        """
        Get input from a file.

        :args:
            operation (str): Either 'encode' or 'decode'.

        :returns:
            input_text (str | None): The content of the file as a string.
        """
        file_path: str = filedialog.askopenfilename(title=f'Select file to {operation}')
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            logging.error("File not found. Please try again.")


class Startup:
    def __init__(self) -> None:
        self.layout_functions = LayoutFunctions()
        self.config = ConfigParser()
        self.config.read('config.ini')
        self.setup_logging()
        self.validate_config()

    def setup_logging(self) -> None:
        """
        Set up the logging configuration.
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

    @staticmethod
    def help() -> None:
        """
        Display usage help for the command-line interface.
        """
        print("Usage:\n"
              " -c, --console:   Run the application in console mode.\n"
              " -h, --help:      Display this help message."
              )

    def main(self) -> None:
        """
        Determine which interface to run based on command-line arguments.
        """
        actions = {
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


if __name__ == '__main__':
    Startup().main()
