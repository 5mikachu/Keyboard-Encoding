import logging

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
def handle_encode():
    text_to_encode: str | None = request.form.get('text_to_encode')
    layout_key: str | None = request.form.get('layout_name')

    if not text_to_encode:
        return jsonify({"error": "No text provided for encoding"}), 400
    if layout_key:
        try:
            encoder_decoder.initialize_layout_dictionaries(layout_key)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    try:
        encoded_text: str = encoder_decoder.encode_text(text_to_encode)
        return jsonify({"encoded_text": encoded_text})
    except Exception as e:
        logging.error(f"Encoding error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/decode', methods=['POST'])
def handle_decode():
    text_to_decode: str | None = request.form.get('text_to_decode')
    layout_key: str | None = request.form.get('layout_name')

    if not text_to_decode:
        return jsonify({"error": "No text provided for decoding"}), 400
    if layout_key:
        try:
            encoder_decoder.initialize_layout_dictionaries(layout_key)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    try:
        decoded_text: str = encoder_decoder.decode_text(text_to_decode)
        return jsonify({"decoded_text": decoded_text})
    except Exception as e:
        logging.error(f"Decoding error: {e}")
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


if __name__ == '__main__':
    app.run(debug=True)
