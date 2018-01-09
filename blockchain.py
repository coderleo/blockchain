#coding=utf-8
import json
import hashlib
from time import time
from uuid import uuid4
class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
    
    def new_block(self,proof,previous_hash = None):
        block = {
            'index':len(self.chain) + 1,
            'timestamp':time(),
            'transctions': self.current_transactions,
            'proof':proof,
            'previous_hash':previous_hash or self.hash(self.chain[-1])

        }
        self.current_transactions = []
        self.chain.append(block)

    
    def new_transaction(self,sender,recipient,amount):
        '''
         生成新交易信息，信息将加入到下一个待挖的区块中
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        '''
        self.current_transactions.append({'sender':sender,
        'recipient':recipient,'amount':amount
        })
        return self.last_block
    @staticmethod
    def hash(block):
        block_string = json.dump(block,sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    @property
    def last_block(self):
        return self.chain[-1] 
    
    def proof_of_work(self,last_proof):
        """
        简单的工作量证明:
         - 查找一个 p' 使得 hash(pp') 以4个0开头
         - p 是上一个块的证明,  p' 是当前的证明
        :param last_proof: <int>
        :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof,proof) is False:
            proof += 1
        
        return proof
    
    @staticmethod
    def valid_proof(last_proof,proof):
        """
        验证证明: 是否hash(last_proof, proof)以4个0开头?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        guess = ('%s%s' %(last_proof,proof)).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
        
