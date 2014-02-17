import unittest 
from deckconverter.card import Card

class TestCard(unittest.TestCase):

    # setUp method
    def setUp(self):
        self.card = Card('Mountain')

    def test_add_card(self):
        self.assertTrue(self.card.get_mvid() == "207936")
        self.assertTrue(self.card.get_set() == "Premium Deck Series: Slivers (Land)")

    def test_add_card_cache(self):
        self.assertTrue(self.card.get_mvid() == "207936")
        self.assertTrue(self.card.get_set() == "Premium Deck Series: Slivers (Land)")
