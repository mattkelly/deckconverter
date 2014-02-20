"""
TODO header
"""

from card import Card

class Deck:

    def __init__(self, name = '', description = ''):
        self.name = name
        self.description = description
        # deck is a dict { Card: (main_qty, sideboard_qty) }
        self.deck = {}
        #self.main = {}
        #self.sideboard = {}

    def add_to_main(self, card, quantity = 1):
        if card in self.deck:
            self.deck[card][0] += quantity 
        else:
            self.deck[card] = (quantity, 0)

    def add_to_sideboard(self, card, quantity = 1):
        if card in self.sideboard:
            self.sideboard[card][1] += quantity 
        else:
            self.sideboard[card] = (0, quantity)
    
    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_sorted_cards(self, sort_by = 'name', reverse = False):
        # TODO error checking on sort_by
        if sort_by == 'name': 
            return sorted(self.deck.keys(), key = lambda x: x.get_name(), reverse = reverse)
        if sort_by == 'main_qty':
            pass # TODO
        if sort_by == 'sideboard_qty':
            pass # TODO

    def iteritems(self):
        return self.deck.iteritems()

    def get_quantity(self):
        return len(deck)

    def __getitem__(self, card):  
        return self.deck[card]

    def __repr__(self):

        if len(self.deck) == 0:
            return 'This deck is empty!\n'

        out = 'Main Deck:\n\n'

        empty = False
        for card in sorted(self.deck.iterkeys()):
            main_qty = self.deck[card][0]
            if main_qty > 0:
                out += "   [%3d] %s\n" % (self.deck[card][0], card)
                empty = False

        if empty:
            out += '   (empty)\n'

        out += '\nSideboard:\n\n'

        empty = True
        for card in sorted(self.deck.iterkeys()):
            sideboard_qty = self.deck[card][1]
            if sideboard_qty > 0:
                out += "   [%3d] %s\n" % (self.deck[card][1], card)
                empty = False

        if empty:
            out += '   (empty)\n'

        return out
