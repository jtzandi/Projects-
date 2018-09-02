#!/usr/bin/env python3

# VoteCoin: Main Program
# (C) Jeff Cikalo, Matt Teichman, Rachel Whaley, and Jordan Zandi

# our libraries
from CryptoClasses import *
from ElectionClasses import *
from Constants import *
from HelperFunctions import *
from Miner import *
from txn_generator import *
from District import *

# standard libraries
from sys import argv


def initialize_app():
    """create an initial NEWVOTES.vc file for demo purposes"""
    print("Initializing the app...")
    initial_tickets = [voteTicket1, voteTicket2, voteTicket3, voteTicket6]
    while True:
        with open('NEWVOTES.vc', 'wb') as tix_file:
                try:
                    pickle.dump(initial_tickets, tix_file)
                    break
                except:
                    time.sleep(1)
                    continue
    print("Demo votes file NEWVOTES.vc created.")


# main 'query' functions for voting interface
    
def see_votes(nickname):
    """display all votes cast by a voter (nickname)"""
    print("Hello " + nickname + ".")
    voter = voter_dict[nickname]
    tickets = list(filter(lambda x : x.voter.vid == voter.vid,
                          blockchain_depickled.get_tickets()))
    if tickets:
        print("Please see your votes below:")
        for ticket in tickets:
            print(ticket)
    else:
        print("Sorry, you did not cast any votes.")

def verify_votes(nickname):
    """verify the signatures of all votes cast by a voter (nickname)"""
    print("Hello " + nickname + ".")
    voter = voter_dict[nickname]
    tickets = list(filter(lambda x : x.voter.vid == voter.vid,
                          blockchain_depickled.get_tickets()))
    if tickets:
        results = [ ticket.verify_signature() for ticket in tickets ]
        if all(results):
            print("Congratulations!  Your votes are legit.")
        else:
            print("Hmm.  Something is up with the signature on one of your votes.")
            print("You should get in touch with your local government.")
    else:
        print("Sorry, you did not cast any votes.")
        
def see_registrations(nickname):
    """display all elections some voter is registered for"""
    tickets = blockchain_depickled.get_tickets()
    voter = voter_dict[nickname]
    elections = list(map(lambda x : x.election, tickets))
    registered = list(filter(lambda x : is_district_match(voter.district, x.district)
                             , elections))
    if registered:
        print("\nVoter %s is registered for the following elections:\n" % voter_fullname[nickname])
        for r in registered:
            print("Election ID: %s" % r.eid)
            print("Position: %s" % r.position)
            print("District: %s" % r.district)
            print("Eligible voting period from %s to %s.\n" %
                  (r.voting_period[0].strftime("%b %d %Y"),
                   r.voting_period[1].strftime("%b %d %Y") )
            )
    else:
        print("You are not registered for any current elections")
    
def list_elections():
    """display all elections that are recorded on the blockchain"""
    for key, val in election_dict.items():
        print("Position: " + str(val.position) +
              ", Year: " + str(val.voting_period[0].year) +
              ", ID: "  + str(key))

def display_candidates(eid):
    """display all candidates who are running in a given election"""
    int_eid = int(eid)
    election = election_dict[int_eid]
    for key, val in election.candidates.items():
        print("Name: " + str(val.name) +
              ", To vote for this person, choose: " + str(key) )

def change_nickname(old, new):
    """allow a user to change the nickname associated with their account"""
    voter = voter_dict[old]
    del voter_dict[old]
    voter_dict[new] = voter

def display_voters():
    """
    display info on all users who are set up to vote using this
    local installation of the app
    """
    for entry in voter_dict:
        print("Full Name: %s\nVoter ID: %s\nNickname: %s\n" %
              (voter_fullname[entry], voter_dict[entry].vid, entry))


        
# blockchain update functions

def validated_cast_vote(voter, vote, election):
    """cast a vote, once all validation checks are satisfied"""
    new_ticket = VoteTicket(voter, vote, election)
    new_ticket.sign()
    current_tickets = new_ticket.repickle_my_pickle("NEWVOTES.vc")
    print("You just cast the following vote:")
    print(new_ticket)

def is_double_vote(voter, election, blockchain):
    """vaidation predicate: identifies double votes"""
    prev_tickets = blockchain.get_tickets()
    this_election = list(filter(lambda x : x.election.eid == election.eid, prev_tickets))
    this_voter = list(map(lambda x : x.voter.vid, this_election))
    return (voter.vid in this_voter)

def election_is_happening(election):
    """validation predicate: identifies whether an election is currently happening"""
    start = election.voting_period[0]
    end = election.voting_period[1]
    return (datetime.date.today() >= start and datetime.date.today() <= end)
    
def cast_vote(nickname, vote, eid):
    """cast a vote in an election, provided it passes three validation checks"""
    int_vote = int(vote)
    int_eid = int(eid)
    election = election_dict[int_eid]
    voter = voter_dict[nickname]

    # three validation checks
    if not is_district_match(voter.district, election.district):
        print("Oops!  Voter %s is not eligible to vote in district %s!" %
              (voter.vid, election.district)
        )
        print("Voter %s is only eligible to vote in district %s." %
              (voter.vid, voter.district)
        )
    elif not election_is_happening(election):
        print("Oops!  That election isn't currently accepting votes.")
        print("That election only accepts votes between:")
        print("    " + election.voting_period[0].strftime("%b %d %Y"))
        print("        and")
        print("    " + election.voting_period[1].strftime("%b %d %Y"))
    elif is_double_vote(voter, election, blockchain_depickled):
        print("Oops!  You already voted in that election.")
    elif all([  is_district_match(voter.district, election.district)
              , election_is_happening(election)
              , not is_double_vote(voter, election, blockchain_depickled)
    ]):
        validated_cast_vote(voter, int_vote, election)
    else:
        raise Exception("False Assert: this shouldn't happen.")


def get_turnout(eid): 
    """display how many votes were cast in an election"""
    total_registered = 0
    total_votes = 0
    int_eid = int(eid)
    election = election_dict[int_eid]
    # total number of votes
    for record in blockchain_depickled.get_tickets():
        if record.election == election:
            total_votes+=1
    # total number of people eligible to vote
    for voter in voter_dict:
        if is_district_match(voter_dict[voter].district, election.district):
            total_registered+=1
    # ratio of the two
    if total_registered == 0:
        print("No one is registered.")
        return
    print(total_votes/total_registered)

def find_voter_nickname(vid):
    '''find voter nickname based on their id number'''
    for nickname in voter_dict:
        if str(voter_dict[nickname].vid) == vid:
            print(nickname)
            return nickname
    print("No voter found for that vid.")
    return "No voter found for that vid."

def find_votable_elections(voter_name):
    can_vote_in = []
    for e in election_dict:
        if is_district_match(voter_dict[voter_name].district, election_dict[e].district):
            if (election_dict[e].voting_period[0] <= datetime.date.today()) and (election_dict[e].voting_period[1] >= datetime.date.today()):
                print(election_dict[e])
                can_vote_in.append(election_dict[e])
    if len(can_vote_in) == 0:
        print("No votable elections currently open.")
        return 
    return can_vote_in

def candidate_votes(eid): # how to pass in the blockchain?
    """display how many votes a candidate received in an election"""
    int_eid = int(eid)
    election = election_dict[int_eid]
    for candidate in election.candidates.values():
        candidate.get_candidate_stats(election, voter_dict, blockchain_depickled)

def who_won(eid):
    '''tells you who won'''
    int_eid = int(eid)
    election = election_dict[int_eid]
    winner_votes = 0
    winner = ''
    for candidate in election.candidates:
        candidate_votes = 0
        for vote in blockchain_depickled.get_tickets():
            if (vote.vote == candidate) and (vote.election == election):
                candidate_votes += 1
        if candidate_votes > winner_votes:
            winner_votes = candidate_votes
            winner = election.candidates[candidate].name
    if winner_votes == 0:
        print("There is no winner.")
        return
    print ("Winner is " + winner + "!!!!!!")

def my_vote_history(vid):
    '''tells you all past elections you voted in and your votes'''
    history = {}
    for vote in blockchain_depickled.get_tickets():
        if str(vote.voter.vid) == vid:
            history[vid] = vote.vote
    if history:
        print("My vote history: \n")
        for key, val in history.items(): 
            print('Election: ' + str(election_dict[int(key)].position) + "\n" +
                  'District: ' + str(election_dict[int(key)].district) + "\n" +
                  ('Voting Period: from %s to %s\n' % (election_dict[int(key)].voting_period[0].strftime("%b %d %Y"),
                                                     election_dict[int(key)].voting_period[1].strftime("%b %d %Y"))) +
                  'Candidate Voted For: ' + election_dict[int(key)].candidates[val].name)
    else:
        print("Voter %s hasn't voted yet." % vid)


# dictionary showing which CLI option in voter mode does what
voter_options = {
      'see_votes' : see_votes
    , 'verify_votes' : verify_votes
    , 'display_voters' : display_voters
    , 'see_registrations' : see_registrations
    , 'get_turnout' : get_turnout
    , 'candidate_votes' : candidate_votes
    , 'cast_vote' : cast_vote
    , 'list_elections' : list_elections
    , 'display_candidates' : display_candidates
    , 'find_voter_nickname' : find_voter_nickname
    , 'find_votable_elections' : find_votable_elections
    , 'change_nickname' : change_nickname
    , 'my_vote_history' : my_vote_history
    , 'who_won' : who_won
}

# dictionary showing which CLI option in other modes does what
other_options = {
        'mine' : start_mining
      , 'generate' : txn_generate
      , 'votes' : initialize_app
    }

# message showing the user all command line options
usage_message = ("USAGE: please type one of following command line arguments:\n\n" +
                 "    (voter mode)\n" +
                 "    --voter  see_votes [VOTER NICKNAME]\n"
                 "             verify_votes [VOTER NICKNAME]\n" +
                 "             display_voters\n" +
                 "             see_registrations [VOTER NICKNAME]\n" +
                 "             get_turnout [ELECTION ID]\n" +
                 "             candidate_votes [ELECTION ID]\n" +
                 "             cast_vote [VOTER NICKNAME] [CHOICE] [ELECTION ID]\n" +
                 "             list_elections\n" +
                 "             display_candidates [ELECTION ID]\n" +
                 "             find_voter_nickname [VOTER ID]\n" +
                 "             find_votable_elections [VOTER NICKNAME]\n" +
                 "             change_nickname [OLD NICKNAME] [NEW NICKNAME]\n" +
                 "             my_vote_history [VOTER ID]\n" +
                 "             who_won [ELECTION ID]" +
                 "\n\n" +
                 "    (miner mode)\n" +
                 "    --miner mine\n\n" +
                 "    (simulation of transactions coming in over the network)\n" +
                 "    --txn generate\n\n" +
                 "    (initialize the app)\n" +
                 "    --initialize votes\n\n" +
                 "To quit miner or transaction generation mode, type CTRL-C."
                 )

def main():
    """main program"""
    try:
        if argv[1] == "--voter":
            voter_options[argv[2]](*argv[3:])
        else:
            raise IndexError
    except IndexError:
        try:
            if argv[1] in ["--miner", "--txn", "--initialize"]:
                other_options[argv[2]]()
            else:
                raise IndexError
        except IndexError:
            print(usage_message)
        except KeyboardInterrupt:
            print("\nGoodbye! Happy Voting!")
        except KeyError:
            print("Please choose an item within the range of options.")
    except KeyboardInterrupt:
        print("\nGoodbye! Happy Voting!")
    except KeyError:
        print("Please choose an item within the range of options.")


if __name__ == "__main__":
    try:
        # load latest blockchain if it exists
        blockchain_depickled = Blockchain.de_pickle_me("BLOCKCHAIN.vc")
    except:
        # create new blockchain if it doesn't
        blockchain_depickled = Blockchain()
    main()
