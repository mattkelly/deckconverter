"""
Simple tests - to be removed later
"""

from deck import Deck
from card import Card

test1 = Card("test1", "set1", "1")
test2 = Card("test1", "set2", "2")

deck = Deck("test", "description")
deck.add_to_main(test1)
deck.add_to_main(test1, 200)
deck.add_to_main(test2, 2)

deck.print_main()

