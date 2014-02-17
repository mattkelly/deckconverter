import unittest 
from deckconverter.deck import Deck
from deckconverter.card import Card

class TestDeck(unittest.TestCase):

    # setUp method
    def setUp(self):
        self.deck = Deck('test_deck', 'test_description')

    # test deck .get_name()
    def test_get_name(self):
        self.assertTrue(self.deck.get_name() == 'test_deck')

    # test deck .get_description()
    def test_get_description(self):
        self.assertTrue(self.deck.get_description() == 'test_description')

    # test deck .add_to_main() / .get_main()
    def test_add_to_main(self):
        card = Card('Forest')
        self.deck.add_to_main(card)
        main = self.deck.get_main()
        self.assertTrue(len(main) == 1)
        self.assertTrue(main.keys()[0].get_name() == 'Forest')

    # test deck .add_to_sideboard() / .get_sideboard()
    def test_add_to_sideboard(self):
        card = Card('Island')
        self.deck.add_to_sideboard(card)
        sideboard = self.deck.get_sideboard()
        self.assertTrue(len(sideboard) == 1)
        self.assertTrue(sideboard.keys()[0].get_name() == 'Island')

