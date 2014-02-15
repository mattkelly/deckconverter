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
        if not isinstance(other, Card):
            return False

        return (self.name == other.name and 
                self.set_name == other.set_name and
                self.mvid == other.mvid)

    def __hash__(self):
        return hash((self.name, self.set_name, self.mvid))
