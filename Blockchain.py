# I have use a python program to create a blockchain.
# For timestamp
import datetime
# Calculating the hash in order to add digital fingerprints to the blocks
import hashlib
# To store data in the blockchain
import json
# Flask is for creating the web app and jsonify is for displaying the blockchain.
from flask import Flask, jsonify 

class Blockchain:
    # This function is created to create the very first block and set its hash to the "0"
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
    # This function is created to add further blocks into the chain
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1, 'timestamp': str(datetime.datetime.now()), 'proof': proof,
                'previous_hash': previous_hash}
        self.chain.append(block)
        return block
    # This function is created to display the previous block
    def print_previous_block(self):
        return self.chain[-1]
    # This is the function for proof of work and used to successfully mine the block
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
        while not check_proof:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation.start[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    def hash(self, block):
        encode_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encode_block).hexdigest()
    def chain_valid(self, chain):
        previous_proof = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_proof'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:5] != '00000':
                return False
            previous_block = block
            block_index += 1
        return True
# Creating the web App using Flask
app = Flask(__name__)
# Create the object of yhe class blockchain
Blockchain = Blockchain()
# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = Blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = Blockchain.proof_of_work(previous_proof)
    previous_hash = Blockchain.hash(previous_block)
    block = Blockchain.create_block(proof, previous_hash)
    response = {'message': 'A block is MINED', 'index': block['index'], 'proof': block['proof'], 'previous_hash': block['previous_hash']}
    return jsonify(response), 200
# Display blockchain in json format
@app.route('/get_chain', methods = ['GET'])
def display_chain():
    response = {'chain': Blockchain.chain, 'length': len(Blockchain.chain)}
    return jsonify(response), 200
# Check validity of blockchain
@app.route('/valid', methods = ['GET'])
def valid():
    valid = Blockchain.chain_valid(Blockchain.chain)
    if valid:
        response = {'message': 'The blockchain is valid.'}
    else:
        response = {'message': 'The blockchain is not valid.'}
    return jsonify(response), 200
# Run the flask server locally
app.run(host = 'localhost', port = 5000)

