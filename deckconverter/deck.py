"""
TODO header
"""

from card import Card

class Deck:

    def __init__(self, name, description = ''):
        self.name = name
        self.description = description
        self.main = {}
        self.sideboard = {}

    def add_to_main(self, card, quantity = 1):
        if card in self.main:
            self.main[card] += quantity 
        else:
            self.main[card] = quantity

    def add_to_sideboard(self, card, quantity = 1):
        if card in self.sideboard:
            self.sideboard[card] += quantity 
        else:
            self.sideboard[card] = quantity
    
    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_main(self):
        return self.main

    def get_sideboard(self):
        return self.sideboard

    def __repr__(self):
        out = 'Main Deck:\n\n'

        if len(self.main) == 0:
            out += '   (empty)\n'
        else:
            for card in sorted(self.main.iterkeys()):
                out += "   [%3d] %s\n" % (self.main[card], card)

        out += '\nSideboard:\n\n'

        if len(self.sideboard) == 0:
            out += '   (empty)\n'
        else:
            for card in sorted(self.sideboard.iterkeys()):
                out += "   [%3d] %s\n" % (self.sideboard[card], card)

        return out
