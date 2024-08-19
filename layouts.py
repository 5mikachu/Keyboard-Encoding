class KeyboardLayouts:
    # Define encode and decode special mappings
    encode_special_mappings = {
        ' ': '00x00',  # SPACE
        '\n': '10x00', # Newline
        '\t': '10x01', # Tab
        '\r': '10x02', # Carriage return
        '\b': '10x03', # Backspace
        '\f': '10x04', # Form feed
        '\v': '10x05', # Vertical tab
        '\a': '10x06', # Bell/alert
        '̀': '00x01',   # Grave accent
        '́': '00x02',   # Acute accent
        '̂': '00x03',   # Circumflex
        '̃': '00x04',   # Tilde
        '̄': '00x05',   # Macron
        '̅': '00x06',   # Overline
        '̆': '00x07',   # Breve
        '̇': '00x08',   # Dot above
        '̈': '00x09',   # Diaeresis (Umlaut)
        '̉': '00x0A',   # Hook above
        '̊': '00x0B',   # Ring above
        '̋': '00x0C',   # Double acute accent
        '̌': '00x0D',   # Caron (Hacek)
        '̍': '00x0E',   # Vertical line above
        '̎': '00x0F',   # Double vertical line above
        '̐': '00x10',   # Candrabindu
        '̑': '00x11',   # Inverted breve
        '̒': '00x12',   # Turned comma above
        '̧': '00x13',   # Cedilla
        '̨': '00x14',   # Ogonek
        '̱': '00x15',   # Macron below
        '̲': '00x16',   # Low line (underscore)
        '̳': '00x17',   # Double low line
        '̹': '00x18',   # Left half ring below
        '̺': '00x19',   # Right half ring below
        '̻': '00x1A',   # Inverted bridge below
        '̼': '00x1B',   # Seagull below
        'ͅ': '00x1C',   # Greek iota subscript
    }
    
    decode_special_mappings = {v: k for k, v in encode_special_mappings.items()}

    # Layouts data
    layouts = {
        'ay': {
            'name': 'AZERTY',
            'lowercase': [
                ['²', '&', 'é', '"', '\'', '(', '-', 'è', '_', 'ç', 'à', ')', '='],
                ['a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '^', '$', '\\'],
                ['q', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'ù', '*'],
                ['w', 'x', 'c', 'v', 'b', 'n', ',', ';', ':', '!', ' ', ' ']
            ],
            'uppercase': [
                ['³', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '°', '+'],
                ['A', 'Z', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '¨', '£', 'µ'],
                ['Q', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', '%', '¤'],
                ['W', 'X', 'C', 'V', 'B', 'N', '?', '.', '/', '§', ' ', ' ']
            ]
        },
        'ck': {
            'name': 'Colemak',
            'lowercase': [
                ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
                ['q', 'w', 'f', 'p', 'g', 'j', 'l', 'u', 'y', ';', '[', ']', '\\'],
                ['a', 'r', 's', 't', 'd', 'h', 'n', 'e', 'i', 'o', '\'', ' '],
                ['z', 'x', 'c', 'v', 'b', 'k', 'm', ',', '.', '/', ' ', ' ']
            ],
            'uppercase': [
                ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'],
                ['Q', 'W', 'F', 'P', 'G', 'J', 'L', 'U', 'Y', ':', '{', '}', '|'],
                ['A', 'R', 'S', 'T', 'D', 'H', 'N', 'E', 'I', 'O', '"', ' '],
                ['Z', 'X', 'C', 'V', 'B', 'K', 'M', '<', '>', '?', ' ', ' ']
            ]
        },
        'dk': {
            'name': 'Dvorak',
            'lowercase': [
                ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '[', ']'],
                ['\'', ',', '.', 'p', 'y', 'f', 'g', 'c', 'r', 'l', '/', '=', '\\'],
                ['a', 'o', 'e', 'u', 'i', 'd', 'h', 't', 'n', 's', '-', ' '],
                [';', 'q', 'j', 'k', 'x', 'b', 'm', 'w', 'v', 'z', ' ', ' ']
            ],
            'uppercase': [
                ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '{', '}'],
                ['"', '<', '>', 'P', 'Y', 'F', 'G', 'C', 'R', 'L', '?', '+', '|'],
                ['A', 'O', 'E', 'U', 'I', 'D', 'H', 'T', 'N', 'S', '_', ' '],
                [':', 'Q', 'J', 'K', 'X', 'B', 'M', 'W', 'V', 'Z', ' ', ' ']
            ]
        },
        'hr': {
            'name': 'HCESAR',
            'lowercase': [
                ['\\', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '\'', '='],
                ['c', 'h', 'e', 's', 'a', 'r', 'u', 'i', 'd', 'o', 'p', '´', '~'],
                ['~', 'q', 'j', 'k', 'x', 'b', 'm', 'w', 'v', 'z', 'ç', '^'],
                ['t', 'n', 'r', 'l', 'm', 'g', 'j', 'v', 'k', 'f', ',', '.']
            ],
            'uppercase': [
                ['|', '!', '"', '#', '$', '%', '&', '/', '(', ')', '=', '?', ''],
                ['C', 'H', 'E', 'S', 'A', 'R', 'U', 'I', 'D', 'O', 'P', '`', '^'],
                ['^', 'Q', 'J', 'K', 'X', 'B', 'M', 'W', 'V', 'Z', 'Ç', ''],
                ['T', 'N', 'R', 'L', 'M', 'G', 'J', 'V', 'K', 'F', ';', ':']
            ]
        },
        'jn': {
            'name': 'JCUKEN',
            'lowercase': [
                ['ё', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
                ['й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ', '\\'],
                ['ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э', ' '],
                ['я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю', '.', ' ', ' ']
            ],
            'uppercase': [
                ['Ё', '!', '"', '№', ';', '%', ':', '?', '*', '(', ')', '_', '+'],
                ['Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х', 'Ъ', '/'],
                ['Ф', 'Ы', 'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Э', ' '],
                ['Я', 'Ч', 'С', 'М', 'И', 'Т', 'Ь', 'Б', 'Ю', ',', ' ', ' ']
            ]
        },
        'qy': {
            'name': 'QWERTY',
            'lowercase': [
                ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
                ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
                ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', ' '],
                ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', ' ', ' ']
            ],
            'uppercase': [
                ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'],
                ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|'],
                ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"', ' '],
                ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?', ' ', ' ']
            ]
        },
        'qz': {
            'name': 'QWERTZ',
            'lowercase': [
                ['^', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'ß', '='],
                ['q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p', 'ü', '+', '\\'],
                ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ö', 'ä', '#'],
                ['y', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-', ' ', ' ']
            ],
            'uppercase': [
                ['°', '!', '"', '§', '$', '%', '&', '/', '(', ')', '=', '?', '`'],
                ['Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P', 'Ü', '*', '|'],
                ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ö', 'Ä', '\''],
                ['Y', 'X', 'C', 'V', 'B', 'N', 'M', ';', ':', '_', ' ', ' ']
            ]
        },
        'wn': {
            'name': 'Workman',
            'lowercase': [
                ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
                ['q', 'd', 'r', 'w', 'b', 'j', 'f', 'u', 'p', ';', '[', ']', '\\'],
                ['a', 's', 'h', 't', 'g', 'y', 'n', 'e', 'o', 'i', '\'', ' '],
                ['z', 'x', 'm', 'c', 'v', 'k', 'l', ',', '.', '/', ' ', ' ']
            ],
            'uppercase': [
                ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'],
                ['Q', 'D', 'R', 'W', 'B', 'J', 'F', 'U', 'P', ':', '{', '}', '|'],
                ['A', 'S', 'H', 'T', 'G', 'Y', 'N', 'E', 'O', 'I', '"', ' '],
                ['Z', 'X', 'M', 'C', 'V', 'K', 'L', '<', '>', '?', ' ', ' ']
            ]
        }
    }

    @staticmethod
    def get_layout(key):
        """
        Retrieve the layout (both lowercase and uppercase) by its key.

        Args:
            key (str): The key for the desired layout (e.g., 'qy' for QWERTY).

        Returns:
            tuple: A tuple containing two lists, the lowercase and uppercase layouts.
        """
        layout = KeyboardLayouts.layouts.get(key)
        if layout:
            return layout['lowercase'], layout['uppercase']
        raise ValueError(f"Layout with key '{key}' not found")

    @staticmethod
    def get_layout_name(key):
        """
        Retrieve the name by its key.

        Args:
            key (str): The key for the desired layout (e.g., 'qy' for QWERTY).

        Returns:
            name (str): The name of the layout.
        """        
        layout = KeyboardLayouts.layouts.get(key)
        if layout:
            return layout['name']
        raise ValueError(f"Layout with key '{key}' not found")

    @staticmethod
    def list_layouts():
        """
        List all available keyboard layouts.

        Returns:
            list: A list of tuples containing the key and name of all layouts.
        """
        return [(key, layout['name']) for key, layout in KeyboardLayouts.layouts.items()]

    @staticmethod
    def add_layout(key, name, lowercase, uppercase):
        """
        Add a new keyboard layout.

        Args:
            key (str): The key for the new layout (e.g., 'ck' for Colemak).
            name (str): The human-readable name of the layout.
            lowercase (list): A list of lists representing the lowercase keys.
            uppercase (list): A list of lists representing the uppercase keys.
        """
        if key in KeyboardLayouts.layouts:
            raise ValueError(f"Layout with key '{key}' already exists")
        KeyboardLayouts.layouts[key] = {
            'name': name,
            'lowercase': lowercase,
            'uppercase': uppercase
        }

    @staticmethod
    def get_special_mappings():
        """
        Retrieve the special character mappings.

        Returns:
            tuple: A tuple containing two dictionaries, the encode and decode special mappings.
        """
        return KeyboardLayouts.encode_special_mappings, KeyboardLayouts.decode_special_mappings
