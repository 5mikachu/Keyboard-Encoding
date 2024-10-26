import logging
import re

from flask import Flask, render_template, request, jsonify

from encode_decode import EncodeDecode
from layout_functions import LayoutFunctions

app = Flask(__name__)

# Initialize LayoutFunctions and EncodeDecode
layouts = LayoutFunctions()
encoder_decoder = EncodeDecode(layouts)


@app.route('/')
def home():
    available_layouts = layouts.list_layouts()  # Get layout options from LayoutFunctions
    return render_template('index.html', layouts=available_layouts)


@app.route('/encode', methods=['POST'])
@app.route('/decode', methods=['POST'])
def handle_encode_decode():
    action: str = request.path.split('/')[-1]
    text: str = request.form.get('text_to_' + action)
    layout_key: str = request.form.get('layout_name')

    if not text:
        return jsonify({"error": f"No text provided for {action}"}), 400
    if layout_key:
        try:
            encoder_decoder.initialize_layout_dictionaries(layout_key)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    try:
        if action == 'encode':
            result: str = encoder_decoder.encode_text(text)
        else:
            result: str = encoder_decoder.decode_text(text)
        return jsonify({f"{action}d_text": result})
    except Exception as e:
        logging.error(f"{action.capitalize()}ing error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/switch_layout', methods=['POST'])
def handle_choose_layout():
    layout_key: str | None = request.form.get('layout_name')
    try:
        layout_name: str = layouts.get_layout_name(layout_key)
        encoder_decoder.initialize_layout_dictionaries(layout_key)
        return jsonify({"message": f"Switched to layout '{layout_name}'"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/view_layout/<layout_key>')
def view_layout(layout_key):
    try:
        # Retrieve layouts
        layout_lowercase, layout_uppercase = layouts.get_layout(layout_key)
        layout_name: str = layouts.get_layout_name(layout_key)

        # Helper function to decode \uXXXX codes
        def decode_unicode(data):
            return [[re.sub(r'\\u([0-9A-Fa-f]{4})', lambda match: chr(int(match.group(1), 16)), key) for key in row] for row in data]

        # Decode both layouts
        decoded_lowercase: list[list[str]] = decode_unicode(layout_lowercase)
        decoded_uppercase: list[list[str]] = decode_unicode(layout_uppercase)

        return render_template(
            'layout_view.html',
            layout_name=layout_name,
            layout_lowercase=decoded_lowercase,
            layout_uppercase=decoded_uppercase
        )
    except ValueError as e:
        return f"Error: {e}", 404


@app.route('/add_layout', methods=['GET', 'POST'])
def add_layout():
    if request.method == 'POST':
        data = request.get_json()
        layout_key: str = data.get('layout_key')
        layout_name: str = data.get('layout_name')
        layout_lowercase: list[list[str]] = data.get('layout_lowercase')
        layout_uppercase: list[list[str]] = data.get('layout_uppercase')

        # Validate inputs
        if not (layout_key and layout_name and layout_lowercase and layout_uppercase):
            return jsonify({"error": "All fields are required"}), 400

        try:
            # Use LayoutFunctions' add_layout to save the layout
            layouts.add_layout(layout_key, layout_name, layout_lowercase, layout_uppercase)
            return jsonify({"message": f"Layout '{layout_name}' added successfully"})
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    # Render the add layout form for GET requests
    return render_template('add_layout.html')


if __name__ == '__main__':
    app.run(debug=True)
