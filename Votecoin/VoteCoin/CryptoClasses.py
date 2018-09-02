# VoteCoin: Cryptocurrency Class Definitions
# (C) Jeff Cikalo, Matt Teichman, Rachel Whaley, and Jordan Zandi

# our modules
from HelperFunctions import *

# standard library modules
import pickle
import random
import math
from random import randint
from hashlib import sha256, new
from binascii import hexlify, unhexlify
import time
import datetime

# pip modules
from fastecdsa import keys, curve, ecdsa
        
class Block(object):
    """blocks for financial transactions in VoteCoin"""
    
    def __init__(self, magic_number=None, transactions=None):
        if magic_number is None:
            self.magic_number = int(0xD9B4BEF9)
        else:
            self.magic_number = magic_number
        self.block_size = int(0)
        self.block_header = Header()
        if transactions is None:
            self.transactions = []
            coinbase_transaction = Transaction("Coinbase", Output(50.0000,1,"string"))
            self.transactions.append(coinbase_transaction)
            self.merkle_tree = self.build_merkle_tree_from_transactions()
        else:
            self.transactions = transactions
            self.build_merkle_tree_from_transactions()
        self.transaction_counter = len(self.transactions)
        self.block_hash = self.block_header.generate_block_hash()
        self.MAX_TXNS = 100
        self.coinbase_transaction = 0
        transaction_count = self.transaction_counter
        self.transaction_fee = 0
        self.total_balance = self.coinbase_transaction + self.transaction_fee

    def __str__(self):
        """string representation for blocks"""
        return("Print Out of Block:" + "\n" + "Magic Number:  %s" % self.magic_number + "\n" + "Block size:  %s" % self.block_size + "\n" + "%s" % self.block_header +"\n" +
        "Transaction Counter:  %s" % self.transaction_counter + "\n" + "\n" + "Block Hash:  %s" % self.block_hash)

    def get_hash(self):
        """retrieve block hash"""
        return self.block_hash

    def create_merkle_tree_from_transactions(self, transactions):
        """
        create a merkle tree for a new block, helper function for
        build_merkle_tree_from_transactions
        """
        transaction_hashes = list(map(lambda x : x.get_hash(), transactions))
        #print("Hashes: ", transaction_hashes)
        dictionary_of_transactions = {}
        dictionary_counter = 0
        level_counter = 0

        while len(transaction_hashes) > 0:
            next_level_transaction_hashes = []
            if len(transaction_hashes) % 2 != 0:
                transaction_hashes.append(transaction_hashes[-1])
            for i in range(0, len(transaction_hashes), 2):
                dictionary_of_transactions[transaction_hashes[i]] = [level_counter, dictionary_counter]
                dictionary_counter = dictionary_counter + 1
                if dictionary_of_transactions.get(transaction_hashes[i+1]) == None:
                    dictionary_of_transactions[transaction_hashes[i+1]] = [level_counter, dictionary_counter]
                dictionary_counter = dictionary_counter + 1
                parent_hash = hash_two_branches(transaction_hashes[i], transaction_hashes[i+1])
                next_level_transaction_hashes.append(parent_hash)
            transaction_hashes = next_level_transaction_hashes
            if len(transaction_hashes) == 1:
                dictionary_of_transactions[transaction_hashes[0]] = [level_counter+1, dictionary_counter]
                break
            level_counter = level_counter + 1
        merkle_root = transaction_hashes[0]
        return (merkle_root, dictionary_of_transactions)

    def build_merkle_tree_from_transactions(self):
        """create a merkle tree for a new block"""
        merkle_root, dictionary_of_transactions = self.create_merkle_tree_from_transactions(self.transactions)
        self.block_header.set_hash_merkle_root(merkle_root)
        self.merkle_tree = dictionary_of_transactions
        self.block_size = len(self.transactions)

    def add_transaction(self, transaction):
        """add a transaction to a block"""
        self.transactions.append(transaction)
        self.transaction_counter = self.transaction_counter + 1
        self.build_merkle_tree_from_transactions()
        self.block_hash = self.block_header.generate_block_hash()

    def validate_merkle_transaction(self, transaction_hash, minimal_transaction_list):
        """validate a node in a merkle tree"""
        for count, hash in enumerate(minimal_transaction_list):
            if transaction_hash == self.block_header.hash_merkle_root:
                return True
            position = self.merkle_tree.get(transaction_hash)
            if position[1] % 2 == 0:
                hash_value = hash_two_branches(transaction_hash, hash)
            else:
                hash_value = hash_two_branches(hash, transaction_hash)
            transaction_hash = hash_value
        return False

    def generate_transactions_needed_for_verification(self, transaction_hash):
        """create list of transactions to validate a node in a merkle tree"""
        minimal_transaction_list = []
        hashes = list(self.merkle_tree.keys())
        positions = list(self.merkle_tree.values())
        while transaction_hash in self.merkle_tree:
            position = self.merkle_tree.get(transaction_hash)
            if position[1] % 2 != 0:
                sibling_position = [position[0], position[1] - 1]
                sibling_index = positions.index(sibling_position)
                sibling = hashes[sibling_position]
                parent = hash_two_branches(sibling, transaction_hash)
            else:
                if transaction_hash == self.block_header.hash_merkle_root:
                    minimal_transaction_list.append(transaction_hash)
                    break
                else:
                    if [position[0], position[1] + 1] in positions:
                        sibling_position = [position[0], position[1] + 1]
                        sibling_index = positions.index(sibling_position)
                        sibling = hashes[sibling_index]
                    else:
                        sibling = transaction_hash
                    parent = hash_two_branches(transaction_hash, sibling)
            minimal_transaction_list.append(sibling)
            transaction_hash = parent
        return(minimal_transaction_list)

    def find_transaction_by_hash(self, transaction_hash):
        """find a transaction in a block by its hash"""
        minimal_transaction_list = self.generate_transactions_needed_for_verification(transaction_hash)
        if self.validate_merkle_transaction(transaction_hash, minimal_transaction_list):
            return self.transactions[self.merkle_tree.get(transaction_hash)[1]]
        else:
            return None


class Blockchain(object):
    """
    blockchain, to store both financial transactions and the votes 
    within those transactions
    """
    
    def __init__(self):
        self.blocks = []
        self.build_genesis_block()

    def build_genesis_block(self):
        """create genesis block"""
        block = Block()
        self.blocks.append(block)

    def __str__(self):
        """string representation of a blockchain"""
        return("Print Out of Blockchain:" + "\n"  +"Size:  %s" % len(self.blocks))

    def add_block(self, block):
        """add a new block to a blockchain"""
        block.block_header.set_hash_prev_block(self.blocks[-1].get_hash())
        self.blocks.append(block)

    def find_block_by_height(self, block_height):
        """retrieve a block from a blockchain by block height"""
        if block_height <= len(self.blocks):
            return self.blocks[block_height]
        else:
            return None

    def find_block_by_hash(self, block_hash):
        """retrieve a block from a blockchain by its hash"""
        for i in range(1, len(self.blocks)):
            if self.blocks[i].get_hash() == block_hash:
                return self.blocks[i]
        return None

    def find_transaction_by_hash(self, transaction_hash):
        """find a transaction in a blockchain by its hash"""
        for block in self.blocks:
            transaction = block.find_transaction_by_hash(transaction_hash)
            if transaction != None:
                return transaction
        return None

    def get_tickets(self):
        """retrieve all vote ballots from a blockchain"""
        output = []
        for block in self.blocks:
            for trans in block.transactions:
                if trans.vote_tickets:
                    output += trans.vote_tickets
                else:
                    pass
        return output

    def pickle_me_timbers(self, file_name):
        """
        save the latest version of a blockchain to a local file;
        this is intended to simulate broadcasting the blockchain
        over a peer to peer network
        """
        my_file = open(file_name, 'wb')
        pickle.dump(self, my_file)
        my_file.close()

    def de_pickle_me(file_name): #unpickles self
        """
        load the latest version of a blockchain from a local file;
        this is intended to simulate listening for the latest 
        blockchain over a peer to peer network
        """
        my_file = open(file_name, 'rb')
        output = pickle.load(my_file)
        my_file.close()
        return output


class Header(object):
    """block header class"""
    
    def __init__(self,
                 version=None,
                 hash_prev_block=None,
                 hash_merkle_root=None,
                 timestamp=None,
                 bits=None,
                 nonce=None):
        """initialize Header with default values, then populate them"""
        if version is None:
            self.version = int(1)
        else:
            self.version = version
        if hash_prev_block is None:
            self.hash_prev_block = 0
        else:
            self.hash_prev_block = hash_prev_block
        if hash_merkle_root is None:
            self.hash_merkle_root = 0
        else:
            self.hash_merkle_root = hash_merkle_root
        if timestamp is None:
            self.timestamp = time.time()
        else:
            self.timestamp = timestamp
        if bits is None:
            self.bits = int(0x207fffff)
        else:
            self.bits = bits
        if nonce is None:
            self.nonce = 0
        else:
            self.nonce = nonce

    def __str__(self):
        """string representation of a block header"""
        return("Block Header - Version:  %s" % self.version + "\n" + "Hash of Previous Block:  %s" % self.hash_prev_block + "\n" +
        "Merkle root:  %s" % self.hash_merkle_root + "\n" + "Time stamp:  %s" % self.timestamp + "\n" + "Bits:  %s" % self.bits + "\n" + "Nonce:  %s" % self.nonce)

    def generate_block_hash(self):
        """determine the hash of a block"""
        timestamp_in_hex = str(self.timestamp).encode('utf-8').hex()
        timestamp_rev = reverser(unhexlify(timestamp_in_hex))

        #merkle root
        merkle_in_hex = str(self.hash_merkle_root).encode('utf-8').hex()
        merkle_rev = reverser(unhexlify(merkle_in_hex))

        #bits
        bits_in_hex = str(self.bits).encode('utf-8').hex()
        bits_rev = reverser(unhexlify(bits_in_hex))

        #nonce
        nonce_in_hex = str(self.nonce).encode('utf-8').hex()
        nonce_rev = reverser(unhexlify(nonce_in_hex))

        #previous block hash
        prevhash_in_hex = str(self.hash_prev_block).encode('utf-8').hex()
        prevhash_rev = reverser(unhexlify(prevhash_in_hex))

        catstring = timestamp_rev + merkle_rev + bits_rev + nonce_rev + prevhash_rev
        reversed_block_hash = reverser(unhexlify(sha256(sha256(unhexlify(catstring)).digest()).hexdigest()))

        return(reversed_block_hash.decode())

    def set_hash_prev_block(self, hash_prev_block):
        """populate previous block hash attribute"""
        self.hash_prev_block = hash_prev_block

    def set_hash_merkle_root(self, hash_merkle_root):
        """set merkle root hash attribute"""
        self.hash_merkle_root = hash_merkle_root


class MerkleTreeNode(object):
    """merkle tree node class definition"""
    
    def __init__(self):
        """each node in a merkle tree has a horizontal position and a hash"""
        self.position = 0
        self.hash = 0

    def set_position(self, position):
        """set position attribute"""
        self.position = position

    def get_position(self):
        """retrieve position attribute"""
        return self.position

    def get_hash(self):
        """retrieve hash"""
        return self.hash


class Transaction(MerkleTreeNode):
    """transaction class definition"""
    
    def __init__(self,
                 list_of_inputs=None,
                 list_of_outputs=None,
                 transaction_hash=None,
                 version_number=None,
                 in_counter=None,
                 out_counter=None):

        # list of vote tickets initializes to empty,
        # and when a user casts a vote, the new vote
        # gets appended to it
        self.vote_tickets = []
        
        MerkleTreeNode.__init__(self)

        # populate attributes
        if list_of_inputs is None:
            self.list_of_inputs = []
        else:
            self.list_of_inputs = [list_of_inputs]
        if list_of_outputs is None:
            self.list_of_outputs = []
        else:
            self.list_of_outputs = [list_of_outputs]
        if version_number is None:
            self.version_number = 1
        else:
            self.version_number = version_number
        if in_counter is None:
            self.in_counter = len(self.list_of_inputs)
        else:
            self.in_counter = in_counter
        if out_counter is None:
            self.out_counter = len(self.list_of_outputs)
        else:
            self.out_counter = out_counter
        if transaction_hash is None:
            self.hash = self.generate_transaction_hash()
        else:
            self.hash = transaction_hash

    def __str__(self):
        """string representation for a transaction"""
        return("Transaction:  " +"\n" +
               "Version number:  %s" % self.version_number +"\n" +
               "Transaction count in:  %s" % self.in_counter +"\n" +
               "List of inputs:  %s" % self.list_of_inputs +"\n" +
               "Transaction count out:  %s" % self.out_counter +"\n" +
               "List of outputs:  %s" % self.list_of_outputs + "\n" +
               "transaction hash:  %s" % self.hash)
    
    def string_for_hashing(self):
        """
        prep information about transaction and any votes it 
        contains for being SHA-hashed
        """
        return (str(self.version_number) +
                str(self.in_counter) +
                list_to_string(self.list_of_inputs) +
                str(self.out_counter) +
                list_to_string(self.list_of_outputs) +
                str(list_to_hashing_string(self.vote_tickets))
        )

    def generate_transaction_hash(self, txn_list=None):
        """generate hash of a transaction"""
        string = self.string_for_hashing()
        return doubleSHA_hashing(string)

    def random():
        """create a random new transaction"""
        return Transaction("input"+str(random.random()),
                           "output"+str(random.random()))

        


#MINER---------------------------------------------------------------------------------------------------

class Miner(object):
    """miner class definition"""
    
    def __init__(self):
        self.candidate_transaction = 0
        self.transaction_fees = 0
        self.total_balance = str(self.candidate_transaction + self.transaction_fees)
        self.transactions_from_memory_pool = []
        self.counter_transactions_from_memory_pool = len(self.transactions_from_memory_pool)

    def __str__(self):
        """string representation of a miner"""
        return(" Block amount of VoteCoin coinbase + transaction fees:  " +
               str(self.total_balance) + "\n" +
               "Transactions:  %s" % self.transactions_from_memory_pool + "\n" +
               "Count of Transactions:  %s" % self.counter_transactions_from_memory_pool)

    def create_candidate_block(self):
        """create a candidate block"""
        block = Block()
        print("Printing Block in Miner:  ", block)

    def transaction_fees(self):
        """calculate transaction fees a miner is to receive"""
        self.transaction_fees = 0.05 * self.counter_transactions_from_memory_pool

    def proof_of_work(self, text, bits):
        """calculate a valid nonce for the latest block"""
        self.text = text
        exponent = bits >> 24
        coefficient = bits & 0xffffff
        first_number_raised_in_target = int(0x8)
        second_number_raised_in_target = int(0x3)
        raised_portion_in_target = (first_number_raised_in_target * (exponent - second_number_raised_in_target))
        two_to_the_raised_portion_in_target = math.pow(2,raised_portion_in_target)

        target = int(coefficient * two_to_the_raised_portion_in_target)
        target_in_hex = hex(target)
        nonce = 0
        while target > nonce:
            # add the nonce to the end of the text
            input_data = text + str(nonce)
            # calculate the SHA-256 hash of the input (text+nonce)
            hash_data = sha256(input_data.encode('utf-8')).hexdigest()
            ihash = int(hash_data,16)
            match = ihash < target # ???
            # show the input and hash result
            if match:
                print("\nNew block nonce:", str(nonce))
                return (nonce)
            else:
                nonce += 1

class TxnMemoryPool(object):
    """transaction memory pool class definition"""
    
    def __init__(self):
        self.txn_memory_pool_list = []
        self.txn_lst = self.txn_memory_pool_list

    def add_transaction_to_txn_memory_pool_list(self, transaction):
        """append a new transaction to the transaction memory pool"""
        self.txn_memory_pool_list.append(transaction)

    def add_random(self):
        """append a random transaction to the memory pool"""
        new = Transaction.random()
        self.add_transaction_to_txn_memory_pool_list(new)

    def get_transaction_from_memory_pool(self):
        """retrieve memory pool list"""
        return self.txn_memory_pool_list

    def insert_ticket(self, vote_ticket):
        """insert ticket into the front of the transaction memory pool"""
        tip = self.txn_memory_pool_list[-1]
        tip.vote_tickets.append(vote_ticket)
            
    def __str__(self):
        """memory pool string representation"""
        return("Transaction Memory Pool: "  + str(self.txn_memory_pool_list))

    def pickle_me_timbers(self, file_name):
        """save the current state of the memory pool to a binary file"""
        my_file = open(file_name, 'wb')
        pickle.dump(self, my_file)
        my_file.close()

    def de_pickle_me(file_name):
        """load a transaction memory pool from a saved file"""
        my_file = open(file_name, 'rb')
        output = pickle.load(my_file)
        my_file.close()
        return output


class Output(object):
    """
    output class definition
    (pretty similar to outputs from the labs)
    """
    
    def __init__(self, value=None, index=None, script=None):

        # populate attributes
        if value is None:
            self.value = 50.0000
        else:
            self.value = value
        if index is None:
            self.index = 1
        else:
            self.index = index
        if script is None:
            self.script = 1
        else:
            self.script = script

    def get_value_index_script(self):
        """helper function for __str__ method"""
        return("Value: %d" % self.value + "\n" +
               "Index: %d" % self.index + "\n" +
               "Script: %s" % self.script)

    def get_value_from_output(self):
        """retrieve value"""
        return(self.value)

    def __str__(self):
        """string representation for outputs"""
        return("Value: %d" % self.value + "\n" +
               "Index: %d" % self.index + "\n" +
               "Script: %s" % self.script)
