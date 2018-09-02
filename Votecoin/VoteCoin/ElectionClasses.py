# VoteCoin: Election/Voting Class Definitions
# (C) Jeff Cikalo, Matt Teichman, Rachel Whaley, and Jordan Zandi

#our modules
from CryptoClasses import *
from HelperFunctions import *
from District import *

# standard library modules
import time
import datetime
import pickle

# pip modules
from fastecdsa import keys, curve, ecdsa

def dict_to_string(dct):
    """
    helper function to get information from a dictionary into 
    a hashable string
    """
    output = []
    for key in dct:
        output.append(key.__str__() + ". " + dct[key].__str__() + "\n")
    return "".join(output)

# dicitonary standing in for a local file storing a voter's private keys
# this would be issued to the user by the election authority
voter_private_keys = {}


class Voter():
    """voter class definition"""

    def __init__(self, district, vid):
        """voter has a uniquely identifying number called a vid"""
        private_key, public_key = keys.gen_keypair(curve.P256)
        self.public_key = public_key
        self.district = district
        self.vid = vid 
        voter_private_keys[vid] = private_key

    def __str__(self):
        """string representation of a voter for pretty printing"""
        return (("Voter ID: %s \n" % (self.vid)) +
                ("Public Key: \n%s\n" % (self.public_key.__str__())) +
                ("District: %s" % (self.district)))
    
    def string_for_hashing(self):
        """put voter information into a string for hashing"""
        return (self.vid +
                self.public_key.__str__() +
                self.district)

    def all_my_tickets(self, blockchain):
        """returns list of all vote tickets this voter cast"""
        tickets = blockchain.get_tickets()
        my_tickets = list(filter(lambda x : x.voter == self, tickets))
        return my_tickets


class Election():
    """election class definition"""

    def __init__(self, position, candidates, voting_period, district, eid):
        """
        election is for a position, has a dictionary of candidates with
        numeric menu choices as keys, is only live for a given time period, 
        is for a certain jurisdiction, and has a numeric ID called 'eid'
        """
        self.position = position
        self.candidates = candidates
        # voting period is an ordered pair of datetimes
        self.voting_period = voting_period
        self.district = district
        self.eid = eid

    def __str__(self):
        """string representation of an election"""
        return (("Election ID: %s \n" % self.eid) +
                ("Position: %s \n" % self.position) +
                ("District: %s \n" % self.district) +
                "Candidates: \n" +
                dict_to_string(self.candidates) +
                "Polls in this election are open from " + self.voting_period[0].__str__() +
                " to " + self.voting_period[1].__str__() )

    def string_for_hashing(self):
        """put information about an election into a string for hashing"""
        return (self.position +
                list_to_string(list(self.candidates.values())) +
                tuple_to_string(self.voting_period) +
                self.district)

    def get_election_tickets(self, blockchain):
        """get all voter ballots for a particular election off a blockchain"""
        tickets = blockchain.get_tickets()
        my_tickets = list(filter(lambda x : x.election == self, tickets))
        return my_tickets

    def __eq__(self, other):
        """equality definition for elections"""
        return self.eid == other.eid

    
class Candidate():
    """electoral candidate class definition"""

    def __init__(self, name, cid):
        self.name = name
        self.cid = cid

    def __str__(self):
        """string representation of a candidate"""
        return (("Candidate Name: %s \n" % self.name) +
                ("Candidate ID: %s" % str(self.cid))
                )

    def string_for_hashing(self):
        """pack information about a candidate into a string for hashing"""
        return self.name

    def get_candidate_stats(self, election, voter_dict, blockchain):
        """print stats on a given candidate"""
        total_votes = 0
        candidate_votes = 0
        total_registered = 0 
                    
        # count total registrations
        for voter in voter_dict:
            if is_district_match(voter_dict[voter].district, election.district):
                total_registered+=1

        # count total and candidate-specific votes
        for record in blockchain.get_tickets():
            if record.election == election:
                total_votes+=1
                if record.vote == self.cid:
                    candidate_votes+=1
        percent_cast = int(candidate_votes)/int(total_votes)
        if total_registered == 0:
            percent_reg = 0
            percent_turnout = 0
        else:
            percent_reg = float(candidate_votes)/float(total_registered)
            percent_turnout = total_votes/total_registered
        print(("%s \n" % self),
                ("Position: %s \n" % election.position),
                ("District: %s \n" % election.district),
                ("# of Votes: %s \n" % total_votes),
                ("Percentage of Votes Cast: %i%% \n" % percent_cast),
                ("Percentage of Total Possible Votes: %i%% \n" % percent_reg),
                ("Overall Turnout: %i%% \n" % (percent_turnout)))

    def __eq__(self, other):
        """identity conditions on candidates"""
        return self.cid == other.cid




class VoteTicket():
    """voter ballot class definition"""
    
    def __init__(self,
                 voter,
                 vote,
                 election):
        """
        voter ballots contain a voter, their choice of candidate,
        an election, and the time the vote was cast
        """
        self.voter = voter
        self.vote = vote
        self.election = election 
        self.time = datetime.datetime.now()
        # signature intializes to empty value, because
        #  a ballot can only be signed once all the information is in
        self.signature = None

    def sign(self):
        """elliptic curves sign a ballot"""
        (r, s) = ecdsa.sign(self.string_for_hashing(), voter_private_keys[self.voter.vid])
        self.signature = (r,s)

    def verify_signature(self):
        """verify an elliptic curves signature on a ballot"""
        if self.signature:
            return ecdsa.verify(self.signature,
                                self.string_for_hashing(),
                                self.voter.public_key
            )
        else:
            return False
    
    def __str__(self):
        """string representation of a ballot"""
        return (("Voter ID: %s \n" % self.voter.vid) +
                ("Position: %s \n" % self.election.position) +
                ("District: %s \n" % self.election.district) +
                ("%s \n" % self.election.candidates[self.vote].__str__()) +
                ("Date: %s \n" % self.time.strftime("%b %d %Y%l:%M %p")) 
        )

    def string_for_hashing(self):
        """pack ballot information into a string for SHA-hashing"""
        return (str(self.voter.vid) +
                self.election.position +
                self.election.district +
                self.election.candidates[self.vote].string_for_hashing()
        )

    def is_correct_district(self):
        """validation predicate for voters voting in the correct district"""
        if is_district_match(self.voter.district, self.election.district):
            return True
        else:
            return False

    def verify_voting_first_time(vote, blockchain):
        """validation predicate for voting at most once in a single election"""
        for record in blockchain.get_tickets():
            if (record.voter == vote.voter) and (record.election == vote.election):
                return False
        return True

    def pickle_me_timbers(self, file_name):
        """save a vote ballot to a file"""
        my_file = open(file_name, 'wb')
        pickle.dump(self, my_file)
        my_file.close()
        print('Vote Ticket "%s" has been pickled! ' % file_name)

    def repickle_my_pickle(self, file_name):
        """
        load a saved list of voter ballots, append a new one to it,
        and write the result back out to the same file
        """
        my_file = open(file_name, 'rb')
        output = pickle.load(my_file)
        my_file.close()
        output.append(self)
        my_file2 = open(file_name, 'wb')
        pickle.dump(output, my_file2)
        my_file2.close()
        
    def de_pickle_me(file_name):
        """save a vote ballot to a file"""
        my_file = open(file_name, 'rb')
        output = pickle.load(my_file)
        my_file.close()
        return output
