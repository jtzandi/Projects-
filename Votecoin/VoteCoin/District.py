# VoteCoin: District Information 
# (C) Jeff Cikalo, Matt Teichman, Rachel Whaley, and Jordan Zandi

def is_district_match(voter_district, election_district):
    """predicate for when a voter is registered to vote in an election"""
    if voter_district == election_district:
        return True
    if election_district in district_defns:
        if voter_district in district_defns[election_district]:
            return True
    else:
        return False   

# definition of districts: keys are superdistricts,
#   values are subdistricts
district_defns = {  "United States": ["Alabama", "Alaska", "Arizona", "Arkansas", "California",
                                      "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
                                      "Hawaii", "Idaho","Illinois","Indiana","Iowa",
                                      "Kansas","Kentucky", "Louisiana", "Maine","Maryland",
                                      "Massachusetts","Michigan","Minnesota","Mississippi",
                                      "Missouri","Montana", "Nebraska","Nevada","New Hampshire",
                                      "New Jersey" ,"New Mexico","New York","North Carolina",
                                      "North Dakota", "Ohio","Oklahoma","Oregon","Pennsylvania",
                                      "Rhode Island","South Carolina","South Dakota","Tennessee" ,
                                      "Texas" ,"Utah","Vermont","Virginia","Washington",
                                      "West Virginia" ,"Wisconsin", "Wyoming"]
                  , "Disneyworld" : ["Toon Town", "Epcot"] }
