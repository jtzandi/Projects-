VoteCoin
(C) Jeff Cikalo, Matt Teichman, Rachel Whaley, and Jordan Zandi

SHORT DESCRIPTION:

VoteCoin is a cryptocurrency and voting app.  The purpose of the app is to use the model of emergent consensus to provide a tamper-resistant voting record of multiple elections in multiple jurisdictions, with the potential to scale to multiple countries.  Votes are signed and can be verified within the app using elliptic curves encryption.  For more detailed information on how our proof of concept relates to the functioning of the actual app when it is in production, please see the section of this readme called BACKGROUND ON THE PROJECT.  


GUIDE TO RUNNING:

VoteCoin is written in Python 3 and requires Python 3.6 or later.  It uses the fastecdsa library for public key encryption, which Mark Shacklette demonstrated in class.  To install Python 3 on OS X, type:

    $ brew install python3

The best way to install the fastecsda library is to use pip.  There are a couple ways to install fastecdsa through pip, but the command that worked for us is:

    $ python3 -m pip install fastecdsa

You can also try:

    $ pip3 install fastecda

If you encounter difficulties, this reference is helpful for troubleshooting:

    https://github.com/AntonKueltz/fastecdsa/issues/4

The files for the project are stored in Matt Teichman's SVN repository in the directory called /project.  To run the demo, please fire up three terminals, and run the following commands:

    In Terminal 1:
    $ chmod +x votecoin.py
    $ ./votecoin.py --initialize votes
    $ ./votecoin.py --txn generate

    In Terminal 2:
    $ ./votecoin.py --miner mine

    In Terminal 3:
    $ ./votecoin.py

(Side note: if you don't have your shell environment variable set up with a path to python3, then instead of running './votecoin.py', you have to run 'python3 votecoin.py'.)

VoteCoin in demo mode in fact runs locally rather than over the network, but is intended to illustrate what the app will look like when it is operating over the network.  The first command in Terminal 1 creates an initial set of votes, so that it's as if we're jumping into a scenario where three people have voted, and one person (nicknamed Rascally McDevious) has tampered with the blockchain and managed to get a vote with a faulty signature into the transaction memory pool.  (So that we can see what happens when a vote is not properly signed.)  

The second command in Terminal 1 starts up our transaction generator, which runs on an infinite loop, generating a random new transaction every second and packaging any new votes up into the latest transaction it generated.  This is intended to simulate new transactions and votes coming in over the network.

The command in Terminal 2 starts up our miner, which will mine new blocks on infinite loop with a bits difficulty setting of 0x1e200000.  Every time it mines a new block, it grabs the latest transactions and votes from the transaction memory pool and packages them into the new block.  It then writes the resulting blockchain to a file shared between the three main processes, which is intended to simulate the broadcast of a miner's new blockchain over a peer to peer network.  Note: the transaction generator should be started before the miner.  If you run the miner first, it will wait until the transaction generator generates some new transactions and writes them to the memory pool data file before doing anything.

To get either the miner or the transaction generator to gracefully exit, hit CTRL-C.  We recommend re-running './interface.py --initialize votes' every time you quit the miner and transaction generator, so that the data files are refreshed to their initial settings.  

In Terminal 3, you will be running the main app as it presents itself to a voter.  If you run ./votecoin.py with no options, a help/error message pops up displaying all possible command line arguments.  We recommend making sure that miner mode and transaction generator mode are both running in separate terminals before running the main app in voter mode.

Here are some example commands that you can run in voter mode, to see how it works:

    $ ./votecoin.py
    $ ./votecoin.py --voter display_voters
    $ ./votecoin.py --voter find_voter_nickname 1
    $ ./votecoin.py --voter find_votable_elections matt
    $ ./votecoin.py --voter cast_vote rachel 1 1
    $ ./votecoin.py --voter cast_vote george 3 2
    $ ./votecoin.py --voter who_won 1
    $ ./votecoin.py --voter my_vote_history 1
    $ ./votecoin.py --voter verify_votes matt

For reference, when looking at the code, the following python script is the main program:

    votecoin.py

Code for our other modules can be found in:

    Constants.py
    CryptoClasses.py
    District.py
    ElectionClasses.py
    HelperFunctions.py
    Miner.py
    txn_generator.py
    votecoin.py



BACKGROUND ON THE PROJECT:

This Python app is a proof of concept for what would be a voting app and cryptocurrency distributed over a peer to peer network in the same way as Bitcoin is.  The demo we are submitting is intended to simulate the experience of using the app both as a voter and as a miner of its cryptocurrency, called VoteCoin.

The main purpose of the app is to provide a mechanism for automatically recording election votes on a publicly viewable blockchain whose integrity is guaranteed via emergent consensus, in the same manner as Bitcoin.

One basic function the app serves is that it eliminates human error from the vote counting process, which by some estimates is as high as 2%.  2% of all the votes cast in the US Presidential Election is about two and a half million.  So right off the bat, one significant advantage to automating the vote tallying process via an app is that it eliminates this numerically considerable margin for error.  

Of course, with an automated vote counting process also comes the concern that cybercriminals or other malicious actors could hack into the system and commit some sort of electoral fraud.  This is where the use of blockchain technology, backed by cryptocurrency mining as an incentive, comes in.  With a publicly viewable blockchain, anyone can audit the voting record.  The more people there are, spread around the world, verifying the integrity of this voting record, the more difficult it is to fraudulently interfere with the voting process.  

Our app stores voting ballots on the blockchain, but does not store any identifying information about voters on the blockchain.  If I wanted to find out whether you voted for Hillary Clinton or Bernie Sanders using this app, I would be out of luck--the best I could to would be to find out whether a voter with ID number 26317812 voted for Hillary Clinton or Bernie Sanders.  Voters' public keys are also stored on the blockchain, so that anyone inspecting it can verify their authenticity.

It is worth mentioning that this app assumes certain aspects of the electoral process to be centralized.  It will be up to a government's central voting authority to issue user accounts, which contain personal identifying information for a voter, the voter's private key, and a link between this information and the voter's publicly viewable numeric ID on the blockchain.  A voter will not be permitted to participate in the system until they have been issued a user account by the voting authority.  In order to simulate this part of the functionality, we have included dictionaries in our code that correlate identifying information and private keys with publicly viewable voter IDs.  The idea is that in the fully fleshed-out version of the app, those dictionaries will be stored locally on the user's machine and kept secure.

So authorization and authentication are not handled within the app; those duties are outsourced onto the government authority in charge of the relevant election, and thus managed in a centralized manner.  It is the voting record that is maintained and verified in a decentralized manner, following the Bitcoin model.  Thus, as long as the voting authorities can be entrusted with the task of issuing non-fraudulent user accounts to the citizens of their jurisdiction, our app will take trust out of the equation when it comes to the most important part of an election: the process of gathering the votes and determining the result. 

Our software performs the following three validations before it allows a user to cast a vote:

    - has the user already voted in this election?
    - is the user registered to vote in this district?
    - is the election currently happening?

The first of these validations requires the app to inspect the blockchain for double votes.  No vote that fails any of them is allowed to be added to the blockchain.  And if somehow a malicious actor is able to sneak a fraudulent vote onto the blockchain via another route, the app allows any user to check the signature of any vote that has been recorded.
