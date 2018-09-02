# VoteCoin: Initialized Constants for Demo
# (C) Jeff Cikalo, Matt Teichman, Rachel Whaley, and Jordan Zandi

from CryptoClasses import *
from District import *

# sample voters
voter1 = Voter("Illinois", 1)
voter2 = Voter("Illinois", 2)
voter3 = Voter("Michigan", 3)
voter4 = Voter("Illinois", 4)
voter5 = Voter("Toon Town", 5)
voter6 = Voter("Texas", 6)

# locally stored record of which voter has which nickname
voter_dict = {
      "matt" : voter1
    , "rachel" : voter2
    , "jeff" : voter3
    , "jordan" : voter4
    , "george" : voter5
    , "rascal" : voter6
    }

# locally stored record of which voter has which full name
#   (in practice, the real app would probably also include
#    other identifying information here, like date of birth)
voter_fullname = {
      "matt" : "Matt Teichman"
    , "rachel" : "Rachel Whaley"
    , "jeff" : "Jeff Cikalo"
    , "jordan" : "Jordan Zandi"
    , "george" : "George Raad"
    , "rascal" : "Rascally McDevious"
    }

# example candidates for demo, for six elections
candidates1 = {1: Candidate("Elizabeth Warren", 1),
               2: Candidate("Jill Stein", 2),
               3: Candidate("Gary Johnson", 3),
               4: Candidate("Paul Ryan", 4)}

candidates2 = {1: Candidate("Donald Duck", 4),
               2: Candidate("Mickey Mouse", 5),
               3: Candidate("Minnie Mouse", 6),
               4: Candidate("Goofy", 7)}

candidates3 = {1: Candidate("Bill Clinton", 8),
               2: Candidate("George H. W. Bush", 9),
               3: Candidate("Ross Perot", 10),
               4: Candidate("Steve Forbes", 11)}

candidates4 = {1: Candidate("Kim Foxx", 12),
               2: Candidate("Anita Alvarez", 13),
               3: Candidate("Donna More", 14)}

candidates5 = {1: Candidate("Margaret Hamilton", 15),
               2: Candidate("Grace Hopper", 16),
               3: Candidate("Ada Lovelace", 17)}

candidates6 = {1: Candidate("Donald Trump", 15),
               2: Candidate("A Lizard", 16),
               3: Candidate("A Piece of Pie", 17)}

# example valid voting periods for demo, for six elections
interval1 = (datetime.date(2018, 7, 20),
             datetime.date(2018, 9, 20))

interval2 = (datetime.date(2018, 7, 20),
             datetime.date(2018, 11, 9))

interval3 = (datetime.date(1992, 10, 20),
             datetime.date(1992, 11, 9))

interval4 = (datetime.date(2016, 10, 20),
             datetime.date(2016, 11, 9))

interval5 = (datetime.date(2018, 8, 20),
             datetime.date(2018, 10, 20))

interval6 = (datetime.date(2020, 8, 20),
             datetime.date(2020, 10, 20))

# six example elections, for demo purposes
election1 = Election("President", candidates1, interval1, "United States", 1)
election2 = Election("Head Disney Character", candidates2, interval2, "Disneyworld", 2)
election3 = Election("President", candidates3, interval3, "United States", 3)
election4 = Election("Prosecutor", candidates4, interval4, "United States", 4)
election5 = Election("Badassest Computer Scientist", candidates5, interval5, "Posterity", 5)
election6 = Election("President", candidates6, interval6, "United States", 6)

# helper function to build elections dictionary
def elecs_to_dict(elecs):
    output = {}
    for e in elecs:
        output[e.eid] = e
    return output

# locally stored information about all elections
#   (these will have been issued to the user by the voting authority)
elections = [election1, election2, election3, election4, election5, election6]
election_dict = elecs_to_dict(elections)

# example vote ballots for the demo
voteTicket1 = VoteTicket(voter1, 2, election1)
voteTicket2 = VoteTicket(voter2, 3, election2)
voteTicket3 = VoteTicket(voter3, 1, election3)
voteTicket4 = VoteTicket(voter4, 2, election4)
voteTicket6 = VoteTicket(voter6, 2, election4)

# sign all but one of the example voting ballots,
#   to demonstrate verification function
voteTicket1.sign()
voteTicket2.sign()
voteTicket3.sign()
voteTicket4.sign()
