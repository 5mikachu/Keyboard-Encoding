import unicodedata
import logging
from typing import List, Dict
from layout_functions import LayoutFunctions


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

        for i in range(len(normalized_text)):
            char: str = normalized_text[i]

            # Check if the code matches a layout key to switch layouts
            if char == '~':
                end_marker: int = normalized_text.find('~', i + 1)
                key: str = normalized_text[i + 1:end_marker]
                if key in dict(self.layout_functions.list_layouts()):
                    self.initialize_layout_dictionaries(key)
                    encoded_text.append(key)
            elif char in self.encoding_dict or self.encode_special_mappings:
                encoded_text.append(
                    self.encoding_dict.get(char) or 
                    self.encode_special_mappings.get(char)
                )
            else:
                logging.warning(f"Unknown character encountered: {char}")
                encoded_text.append('�')

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
        codes: str = encoded_text.split()

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