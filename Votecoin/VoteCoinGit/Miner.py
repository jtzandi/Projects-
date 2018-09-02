# VoteCoin: Miner Mode
# (C) Jeff Cikalo, Matt Teichman, Rachel Whaley, and Jordan Zandi

# The purpose of this mode is to simulate the mining that would happen
# on a peer to peer network, with miners adding incoming votes to the
# blockchain.

# our modules
from CryptoClasses import *

# in case you'd like to vary the difficulty setting, for testing purposes
difficulty = 0x1e200000

def mine_new_block(blockchain, lst):
    """mine a new block and add it to the blockchain, for demo"""
    time.sleep(2)
    block = Block()
    counter = 0
    for t in lst:
        block.add_transaction(t)
    miner = Miner()
    updated_nonce = miner.proof_of_work(block.get_hash(), difficulty)
    block.block_header.nonce = updated_nonce
    blockchain.add_block(block)
    print("Current blockchain length: ", len(blockchain.blocks))
    print("Current # of votes in the blockchain:", len(blockchain.get_tickets()))

def start_mining():
    """mine new blocks forever, incorporating new votes as they come in"""
    print("Starting Miner.")
    previous_transes = []
    blockchain = Blockchain()
    while True:
        time.sleep(1)
        while True:
            try:
                pool = TxnMemoryPool.de_pickle_me("MEMPOOL.vc")
                break
            except:
                time.sleep(1)
                continue
        incoming_transes = pool.txn_memory_pool_list
        new_transes = [ x for x in incoming_transes if not any( [ same_transes(x,y) for y in previous_transes ] ) ]
        deduped_transes = dict.fromkeys(new_transes).keys()
        miner = Miner()
        mine_new_block(blockchain, new_transes)
        blockchain.pickle_me_timbers("BLOCKCHAIN.vc")
        previous_transes += new_transes

