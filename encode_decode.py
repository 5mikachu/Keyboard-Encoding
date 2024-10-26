import logging
import unicodedata

from layout_functions import LayoutFunctions


class EncodeDecode:
    def __init__(self, layouts: 'LayoutFunctions') -> None:
        """
        Initialize the EncodeDecode class.

        :args:
            layouts (LayoutFunctions): An instance of the LayoutFunctions class.
        """
        self.layout_functions = LayoutFunctions()
        self.layouts = layouts
        self.encode_special_mappings, self.decode_special_mappings = self.layouts.get_special_mappings()
        self.encoding_dict: dict[str, str] = {}
        self.decoding_dict: dict[str, str] = {}
        self.layout_lowercase: list[list[str]] = []
        self.layout_uppercase: list[list[str]] = []

    def initialize_layout_dictionaries(self, layout_key: str) -> None:
        """
        Creates dictionaries used to encode and decode for both lowercase and uppercase layouts.

        :args:
            layout_key (str): The short name for the used layout.
        """
        if layout_key in self.encoding_dict:
            return  # Use cached dictionaries

        self.layout_lowercase, self.layout_uppercase = self.layouts.get_layout(layout_key)

        for prefix, layout in (('0', self.layout_lowercase), ('1', self.layout_uppercase)):
            for row_idx, row in enumerate(layout):
                for col_idx, char in enumerate(row):
                    if char.strip():
                        code = f"{prefix}{row_idx + 1:01}x{col_idx + 1:02}"
                        self.encoding_dict[char] = code
                        self.decoding_dict[code] = char

    def encode_text(self, text: str) -> str:
        """
        Encodes the given text using the encoding dictionary.

        :args:
            text (str): The text to encode.

        :returns:
            encoded_text (str): The encoded text.
        """
        encoded_text: list[str] = []
        normalized_text: str = unicodedata.normalize('NFD', text)

        for i, char in enumerate(normalized_text):
            # Switch layout if special character "~" is detected with a valid layout key
            if char == '~':
                end_marker = normalized_text.find('~', i + 1)
                key = normalized_text[i + 1:end_marker]
                if key in dict(self.layout_functions.list_layouts()):
                    self.initialize_layout_dictionaries(key)
                    encoded_text.append(key)
            elif char in self.encoding_dict or self.encode_special_mappings:
                # Append encoded character or special mapping, falling back to "�" if missing
                encoded_char = self.encoding_dict.get(char) or self.encode_special_mappings.get(char, '�')
                encoded_text.append(encoded_char)
            else:
                logging.warning(f"Unknown character encountered: {char}")
                encoded_text.append('�')

        return ' '.join(encoded_text)

    def decode_text(self, encoded_text: str) -> str:
        """
        Decodes the given text using the decoding dictionary.

        :args:
            encoded_text (str): The text to decode.

        :returns:
            decoded_text (str): The decoded text.
        """
        decoded_text: list[str | None] = []
        codes: list[str] = encoded_text.split()

        for code in codes:
            # Switch layout if the code is a valid layout key
            if code in dict(self.layout_functions.list_layouts()):
                self.initialize_layout_dictionaries(code)
                decoded_text.append(f"~{code}~")
            elif code in self.decoding_dict or self.decode_special_mappings:
                # Append decoded character or special mapping, falling back to "�" if missing
                decoded_char = self.decoding_dict.get(code) or self.decode_special_mappings.get(code, '�')
                decoded_text.append(decoded_char)
            else:
                logging.warning(f"Unknown code encountered: {code}")
                decoded_text.append('�')

        return ''.join(decoded_text)
