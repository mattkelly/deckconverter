"""
TODO header
"""

class Card:
    
    def __init__(self, name, set_name = '', mvid = ''):
        self.name = name
        self.set_name = set_name
        self.mvid = mvid

        if self.set_name == '':
            # TODO look up latest set name if needed
            pass
        if self.mvid == '':
            # TODO look up mvid if needed
            pass

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False

        return (self.name == other.name and 
                self.set_name == other.set_name and
                self.mvid == other.mvid)

    def get_name(self):
        return self.name
    
    def get_set(self):
        return self.set_name

    def get_mvid(self):
        return self.mvid

    def __hash__(self):
        return hash((self.name, self.set_name, self.mvid))

    def __repr__(self):
        return "%s from %s (mvid = %s)" % (self.name, self.set_name, self.mvid)

