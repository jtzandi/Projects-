# VoteCoin: Assorted Helper Functions
# (C) Jeff Cikalo, Matt Teichman, Rachel Whaley, and Jordan Zandi

# our modules
from ElectionClasses import *

# standard library modules
from hashlib import sha256, new
from binascii import hexlify, unhexlify
import time

def registered_voters(dct):
    """determine who is registered to vote from locally-stored dictionary"""
    return list(dct.keys())


# merkle functions

def reverser(str):
    """little-endian/big-endian magic"""
    ba = bytearray(str)
    ba.reverse()
    retval = hexlify(ba)
    return retval

def hash_first_two_branches(txids):
    """conclude the creation of a merkle tree"""
    return(hash_two_branches(txids[0].get_hash(), txids[1].get_hash()))

def hash_two_branches(branch1, branch2):
    """create merkle parent hash from two merkle child hashes"""
    branch1 = branch1
    branch2 = branch2
    bbranch1 = unhexlify(branch1)
    branch1hash = reverser(bbranch1)
    bbranch2 = unhexlify(branch2)
    branch2hash = reverser(bbranch2)
    concatenate1and2 = branch1hash + branch2hash
    header = unhexlify(concatenate1and2)
    headerhash = sha256(sha256(header).digest()).hexdigest()
    reversedheaderhash = reverser(unhexlify(sha256(sha256(header).digest()).hexdigest()))
    return(reversedheaderhash.decode())


# stringification functions

def tuple_to_string(tpl):
    """put information from a tuple into a string"""
    return tpl[0].__str__() + tpl[1].__str__()
                
def list_to_string(lst):
    """put information from a list into a string"""
    output = ""
    for item in lst:
        output += item.__str__()
    return output

def list_to_hashing_string(lst):
    """put information from a hashstring-able list into a string"""
    output = ""
    for item in lst:
        output += item.string_for_hashing()
    return output


# hashing functions 

def doubleSHA_hashing(string):
    """double SHA-256 a string"""
    value = string
    x = unhexlify(sha256(value.encode('utf-8')).hexdigest())
    y = sha256(x).hexdigest()
    return y

def same_tickets(tick1, tick2):
    """predicate: equivalence relation on tickets"""
    return (tick1.voter.vid == tick2.voter.vid and
            tick1.election.eid == tick2.election.eid 
            )

def same_transes(trans1, trans2):
    """predicate: equivalence relation on transactions"""
    return trans1.hash == trans2.hash
