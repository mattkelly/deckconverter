"""
TODO header
"""

class Card:
    
    def __init__(self, name, set_name = '', mvid = ''):
        self.name = name
        # TODO look up latest set name if needed
        self.set_name = set_name
        # TODO look up mvid if needed
        self.mvid = mvid

    def __eq__(self, other):
        if not isinstance(other, Deck):
            return False

        return (self.name == other.name and 
                self.set_name == other.set_name and
                self.mvid == other.mvid)

