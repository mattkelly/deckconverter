"""
TODO header
"""

import request

class Card:
    
    def __init__(self, name, set_name = None, mvid = None):
        self.name = name
        self.set_name = set_name
        self.mvid = mvid
        self.__set_card_details()

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False

        return (self.name == other.name and 
                self.set_name == other.set_name and
                self.mvid == other.mvid)

    def __set_card_details(self):
        if self.set_name == None or self.mvid == None:
            details = request.get_card_details(self.name, self.set_name, self.mvid)
            self.mvid = details['mvid']
            self.set_name = details['set_name']

    def __set_mvid(self):
        self.mvid = request.get_mvid(self.name, self.set_name)

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
