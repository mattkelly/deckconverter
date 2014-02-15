"""
TODO header
"""

from card import Card

class Deck:

    def __init__(self, name, description = ''):
        self.name = name
        self.description = description
        self.main = []
        self.sideboard = []

    def add_to_main(self, card, quantity):
        self.main.append((card, quantity))

    def add_to_sideboard(self, card, quantity):
        self.sideboard.append((card, quantity))

    def get_sideboard(self):
        return self.sideboard

    def get_main(self):
        return self.main

