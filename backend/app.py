from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
from blockchain import Blockchain
from encryption_utils import generate_key

app = Flask(__name__)

# Enable CORS for the entire app
CORS(app)

# Initialize the blockchain
blockchain = Blockchain()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the CryptoVault Blockchain!"})

@app.route('/generate-key', methods=['POST'])
def generate_key_route():
    key = generate_key()
    return jsonify({"key": key})

@app.route('/add-data', methods=['POST'])
def add_data():
    data = request.json.get('data')
    key = request.json.get('key')
    new_block = blockchain.add_block(data, key)
    return jsonify({"blockchain": blockchain.get_chain()})

@app.route('/delete-block', methods=['POST'])
def delete_block():
    try:
        block_index = request.json.get('index')
        updated_chain = blockchain.delete_block(block_index)
        return jsonify({"blockchain": updated_chain})
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except IndexError as ie:
        return jsonify({"error": str(ie)}), 400

@app.route('/delete-all', methods=['POST'])
def delete_all():
    updated_chain = blockchain.delete_all_blocks()
    return jsonify({"blockchain": updated_chain})


if __name__ == '__main__':
    app.run(debug=True)
