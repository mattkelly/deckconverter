"""
TODO header
"""

import request

class Card:
    
    def __init__(self, name, set_name = '', mvid = ''):
        self.name = name
        self.set_name = set_name
        self.mvid = mvid
        if self.set_name == '':
            self.__set_set_name()
        if self.mvid == '':
            self.__set_mvid()

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False

        return (self.name == other.name and 
                self.set_name == other.set_name and
                self.mvid == other.mvid)

    def __set_set_name(self):
        self.set_name = request.get_set_name(self.name)

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
