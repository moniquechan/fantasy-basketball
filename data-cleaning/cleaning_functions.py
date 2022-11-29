def initialize_name(firstname, lastname):
    if '.' in firstname:
        return firstname + ' ' + lastname
    return firstname.str.slice(0,1) + '. ' + lastname
