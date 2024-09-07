import json
import logging
from typing import List, Tuple, Dict, Union


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
                encode_special_mappings: Dict[str, str] = json.load(file)
            # Create the decode mapping by reversing the encode mapping
            decode_special_mappings: Dict[str, str] = {v: k for k, v in encode_special_mappings.items()}
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