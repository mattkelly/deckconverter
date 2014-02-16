"""
Simple tests - to be removed later
"""

from deckconverter.deck import Deck
from deckconverter.card import Card

test1 = Card("Forest", "Gatecrashers", "1")
test2 = Card("Island", "Born of the Gods", "2")

deck = Deck("test", "description")
deck.add_to_main(test1)
deck.add_to_main(test1, 200)
deck.add_to_main(test2, 2)

print deck
