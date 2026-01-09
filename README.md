# Building a Simplified Blockchain 
*(English Version)* 
### Implementation of a simple Blockchain in Python with proof-of-work, consensus algorithm, and Flask API in order to study how Blockchains work.

##

### Tools and Technologies
To run and test this application, the following tools are required:
* **Language:** Python 3.6+
* **Web Framework:** Flask (to create API endpoints).
* **HTTP Client:** Postman (to interact with the blockchain).
* **Libraries:** `requests` and `hashlib`

### Features
This project simulates the core mechanics of a blockchain:
* **Block Structure:** 
```json
block = {
    'index': ..., #block height
    'timestamp': ..., #creation time of the block
    'transactions': [
        {
            'sender': ..., #address of the sender
            'recipient': ..., #address of the recipient
            'amount': ... #value of the transaction
        }
    ],
    'merkle_root': ..., #hash representing the Merkle Tree root of the transactions
    'proof': ..., #the proof given by the Proof of Work algorithm
    'previous_hash': ... #the SHA-256 hash of the previous block
}
```
* **Proof of Work (PoW):** a mining algorithm to secure the network.
* **Merkle Tree:** verification of transaction integrity within blocks.
* **Data Persistence:** automatically saves the chain to `blockchain_data.json`.
* **Consensus Algorithm:** solve conflicts by prioritazing the longest valid chain.

Note: the server will run at `http://localhost:5000`

### Interacting via Postman:
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/mine` | Mines a new block. |
| **POST** | `/transactions/new` | Adds a new transaction. |
| **GET** | `/chain` | Returns the full blockchain. |
| **POST** | `/nodes/register` | Registers new neighbor nodes. |
| **GET** | `/nodes/resolve` | Runs the consensus algorithm. |

### Tutorials used:
* [Learn Blockchains by Building One](https://hackernoon.com/learn-blockchains-by-building-one-117428612f46)
* [Build Your Own Blockchain: A Python Tutorial](https://ecomunsing.com/build-your-own-blockchain)


##

# Construindo uma Blockchain Simplificada:
*(Versão em Português)* 
### Implementação de uma Blockchain simples em Python com prova de trabalho, algoritmo de consenso e API Flask com o objetivo de estudar o funcionamento das Blockchains.

##

### Ferramentas e Tecnologias:
Para rodar e testar esta aplicação, são necessárias as seguintes ferramentas:
* **Linguagem:** Python 3.6+
* **Framework Web:** Flask (para criar os endpoints da API).
* **Cliente HTTP:** Postman (para interagir com a blockchain).
* **Bibliotecas:** `requests` e `hashlib`

### Funcionalidades Implementadas:
Esse projeto simula a mecânica central de uma blockchain:
* **Estrutura dos Blocos:** 
```json
block = {
    'index': ..., #altura do bloco
    'timestamp': ..., #momento de criação do bloco
    'transactions': [
        {
            'sender': ..., #endereço do remetente
            'recipient': ..., #endereço do destinatário
            'amount': ... #valor da transação
        }
    ],
    'merkle_root': ..., #hash que representa a raiz da Merkle Tree das transações
    'proof': ..., #a prova de trabalho gerada pelo algoritmo de Proof of Work
    'previous_hash': ... #o hash SHA-256 do bloco anterior
}
```
* **Prova de Trabalho (PoW):** algoritmo de mineração para garantir a segurança da rede.
* **Merkle Tree:** verificação da integridade das transações dentro dos blocos.
* **Data Persistence:** salva automaticamente a cadeia no arquivo `blockchain_data.json`.
* **Algoritmo de Consenso:** resolve conflitos ao priorizar a maior cadeia válida.

Obs.: o servidor irá rodar em `http://localhost:5000`

### Interagindo via Postman:
| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| **GET** | `/mine` | Minera um novo bloco. |
| **POST** | `/transactions/new` | Adiciona uma nova transação. |
| **GET** | `/chain` | Retorna a blockchain completa. |
| **POST** | `/nodes/register` | Registra novos nós vizinhos. |
| **GET** | `/nodes/resolve` | Executa o algoritmo de consenso. |
