import unittest 
from deckconverter.card import Card

class TestCard(unittest.TestCase):

    # setUp method
    def setUp(self):
        self.card = Card('Mountain')

    def test_get_name(self):
        self.assertTrue(self.card.get_name() == 'Mountain')

    def test_get_set(self):
        self.assertTrue(self.card.get_set() == 'Premium Deck Series: Slivers')

    def test_get_mvid(self):
        self.assertTrue(self.card.get_mvid() == '207936')

    def test_equality(self):
        card = Card('Mountain')
        self.assertTrue(self.card.__eq__(card))
        card = Card('Island')
        self.assertFalse(self.card.__eq__(card))

    def test_repr(self):
        self.assertTrue(self.card.__repr__() == 'Mountain from Premium Deck Series: Slivers (mvid = 207936)')
