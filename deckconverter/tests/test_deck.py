import unittest 
from deckconverter.deck import Deck
from deckconverter.card import Card

class TestDeck(unittest.TestCase):

    # setUp method
    def setUp(self):
        self.deck = Deck('test deck', 'test description')

    # test deck .get_name()
    def test_get_name(self):
        self.assertTrue(self.deck.get_name() == 'test deck')

    # test deck .get_description()
    def test_get_description(self):
        self.assertTrue(self.deck.get_description() == 'test description')

    # test deck .add_to_main() / .get_main()
    def test_add_to_main(self):
        card = Card('Forest')
        self.deck.add_to_main(card)
        self.assertTrue(self.deck[card][0] == 1)

    # test deck .add_to_sideboard() / .get_sideboard()
    def test_add_to_sideboard(self):
        card = Card('Island')
        self.deck.add_to_sideboard(card)
        self.assertTrue(self.deck[card][1] == 1)

