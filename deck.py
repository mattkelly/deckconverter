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

    def get_main(self):
        return self.main

    def get_sideboard(self):
        return self.sideboard

    def print_main(self):
        # TODO actually implement this (or __repr__ and __str__)
        print self.main

