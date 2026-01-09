import json, hashlib, requests, os
from time import time
from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, jsonify, request

#variáveis globais:
chain = []
current_transactions = []
nodes = set()
file_path='blockchain_data.json'

#criação do hash SHA-256 de um bloco:
def hash(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

#cálculo da raiz da merkle tree das transações:
def calculate_merkle_root(transactions):
    if not transactions:
        return hashlib.sha256(b'').hexdigest()
    transaction_hashes = []
    for tx in transactions:
        tx_hash = hashlib.sha256(json.dumps(tx, sort_keys=True).encode()).hexdigest()
        transaction_hashes.append(tx_hash)
    while len(transaction_hashes) > 1:
        if len(transaction_hashes)%2 != 0:
            transaction_hashes.append(transaction_hashes[-1])
        new_level = []
        for i in range(0, len(transaction_hashes), 2):
            combined = transaction_hashes[i] + transaction_hashes[i+1]
            new_level.append(hashlib.sha256(combined.encode()).hexdigest())
        transaction_hashes = new_level
    return transaction_hashes[0]

#criação de um bloco:
def new_block(proof, previous_hash=None):
    global chain, current_transactions
    merkle_root = calculate_merkle_root(current_transactions)
    block = {
        'index':len(chain)+1,
        'timestamp':time(),
        'transactions':current_transactions,
        'merkle_root': merkle_root,
        'proof':proof,
        'previous_hash':previous_hash or hash(chain[-1])
    }
    current_transactions=[]
    chain.append(block)
    return block

#retorno do último bloco:
def last_block():
    global chain
    return chain[-1]

#criação de uma nova transação (adicionada na lista global até ser minerada e salva na blockchain em um bloco):
def new_transaction(sender, recipient, amount):
    global current_transactions
    current_transactions.append({'sender':sender, 'recipient':recipient,'amount':amount})
    return last_block()['index']+1

#validação da prova de trabalho:
def valid_proof(last_proof, proof):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"
    
#algoritmo da prova de trabalho:
#encontrar um número p' tal que hash(pp') contém 4 0s, onde p é o p' anterior
def proof_of_work(last_proof):
    proof=0
    while valid_proof(last_proof, proof) is False:
        proof = proof+1
    return proof
    
#verificação da validade da chain:
def valid_chain(chain_to_check):
    global chain
    last_block=chain_to_check[0]
    current_index=1
    while current_index < len(chain_to_check):
        block = chain_to_check[current_index]
        if block['previous_hash']!=hash(last_block):
            return False
        if block['merkle_root'] != calculate_merkle_root(block['transactions']):
            return False
        if not valid_proof(last_block['proof'], block['proof']):
            return False
        last_block = block
        current_index = current_index + 1
    return True

#resolução de conflitos: garante o consenso fazendo com que a chain mais longa válida é a correta
def resolve_conflicts():
    global chain, nodes
    neighbours = nodes
    new_chain = None
    max_length = len(chain)
    for node in neighbours:
        response = requests.get(f'http://{node}/chain')
        if response.status_code == 200:
            length = response.json()['length']
            ext_chain = response.json()['chain']
            if length > max_length and valid_chain(ext_chain):
                max_length = length
                new_chain = ext_chain
    if new_chain:
        chain = new_chain
        save_blockchain()
        return True
    return False
    
#registro dos nós:
def register_nodes(address):
    global nodes
    url = urlparse(address)
    nodes.add(url.netloc)

#persistência dos dados:
def save_blockchain():
    global chain
    with open(file_path, 'w') as f:
        json.dump(chain, f, indent=4)
def load_blockchain():
    global chain
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            chain = json.load(f)
        return True
    return False

#criação do bloco gênesis:
if not load_blockchain():
    new_block(proof=100, previous_hash='1')
    save_blockchain()

#usando Python Flask Framework para "conversar" com a blockchain usando HTTP requests
"""Obs.: Códigos comuns em APIs:
200 -> sucesso
201 -> criado
400 -> bad request
401 -> unauthorized
404 -> not found
500 -> internal server error"""
app = Flask(__name__)
node_identifier = str(uuid4()).replace('-','') #cria um nome aleatório para o nó

@app.route('/mine', methods=['GET']) #cria o endpoint /mine que é um GET
def mine():
#processo de mineração: cálculo do proof of work, recompensa do minerador, criação do novo bloco e adição na chain
    last_block_v = last_block()
    last_proof = last_block_v['proof']
    proof = proof_of_work(last_proof)

    new_transaction(sender="0", recipient=node_identifier, amount=1)

    previous_hash = hash(last_block_v)
    block = new_block(proof, previous_hash)

    save_blockchain()

    response = {'message':"New block forged", 'index':block['index'], 'transactions':block['transactions'],'merkle_root': block['merkle_root'],'proof':block['proof'],'previous_hash':block['previous_hash']}
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST']) #cria o endpoint /transactions/new que é um POST
def transaction_new():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    index = new_transaction(values['sender'], values['recipient'],values['amount'])
    response = {'message': f'Transaction added to Bloco {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET']) #cria o endpoint /chain, que retorna a blockchain toda
def full_chain():
    global chain
    response = {'chain':chain, 'length':len(chain)}
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST']) #cria o endpoint /nodes/register, que permite registrar novos nós
def nodes_register():
    global nodes
    values = request.get_json()
    nodes_list = values.get('nodes')
    if nodes_list is None:
        return "Error: list of nodes is invalid", 400
    for node in nodes_list:
        register_nodes(node)
    response = {'message':'New nodes added','total_nodes':list(nodes)}
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET']) #cria o endpoint /nodes/resolve, que resolve conflitos entre nós diferentes
def consensus():
    global chain
    replaced = resolve_conflicts()
    if replaced:
        response={'message':'Chain was replaced', 'new_chain':chain}
    else:
        response={'message':'Chain is already authoritative', 'chain':chain}
    return jsonify(response),200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
