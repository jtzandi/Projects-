# VoteCoin: Transaction Generator Mode
# (C) Jeff Cikalo, Matt Teichman, Rachel Whaley, and Jordan Zandi

# The purpose of this mode is to simulate the flow of transactions and
# votes over a peer to peer network, to which the miner is listening,
# much the same as in Bitcoin.

# our modules
from CryptoClasses import *

# standard library modules
import time
from binascii import hexlify, unhexlify

def txn_generator(pool):
    """generate a new transaction and add it to the memory pool"""
    txn_input = (str(randint(1,1000)) + str(randint(1,1000)) +
                 str(randint(1,1000)) + str(randint(1,1000))
                 )
    txn_output = (str(randint(1,1000)) + str(randint(1,1000)) +
                  str(randint(1,1000)) +str(randint(1,1000)) +
                  str(randint(1,1000))
                  )
    txn = Transaction(txn_input, txn_output)
    pool.add_transaction_to_txn_memory_pool_list(txn)

    
def txn_generate():
    """
    main function for transaction generation mode;
    simulates new transactions coming in over a peer to peer
    network
    """

    pool = TxnMemoryPool()
    previous_tickets = []

    while True:
        time.sleep(2)
        with open('NEWVOTES.vc', 'rb') as data_file:
            try:
                data = pickle.load(data_file)
            except:
                time.sleep(1)
                continue
        new_tickets = [ x for x in data if not any( [ same_tickets(x,y) for y in previous_tickets ] ) ]
        deduped_tickets = list(set(new_tickets))
        time.sleep(1)
        txn_generator(pool)

        for ticket in deduped_tickets:
            pool.insert_ticket(ticket) 

        new = [ x for x in new_tickets if not any( [ same_tickets(x,y) for y in previous_tickets ] ) ]

        if new:
            print("New Vote Tickets:")
            for ticket in new:
                print(ticket)
            print("Total number of transactions generated: ", len(pool.txn_memory_pool_list))
        else:
             pass       
        
        pool.pickle_me_timbers("MEMPOOL.vc")
        previous_tickets.extend(x for x in new_tickets if not any( [ same_tickets(x,y) for y in previous_tickets ] ) )
