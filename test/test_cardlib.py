import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from poker_module.cardlib import *
import pytest


# This test assumes you call your suit class "Suit" and the suits "Hearts and "Spades"
def test_cards():
    h4 = NumberedCard(4, Suit.Hearts)
    jack = JackCard(Suit.Hearts)
    queen = QueenCard(Suit.Hearts)
    king = KingCard(Suit.Diamonds)
    ace = AceCard(Suit.Clubs)
    ace_hearts = AceCard(Suit.Hearts)

    # Checks correct form of the cards
    assert isinstance(h4.suit, Enum)
    assert isinstance(jack.suit, Enum)
    assert isinstance(queen.suit, Enum)
    assert isinstance(king.suit, Enum)
    assert isinstance(ace.suit, Enum)

    # Checks so that the different cards equals to what their intended value should be
    assert h4.get_value() == 4
    assert jack.get_value() == 11
    assert queen.get_value() == 12
    assert king.get_value() == 13
    assert ace.get_value() == 14

    # Compares the different card types.
    assert h4 == h4  # Numbered card equal to itself
    assert queen == queen  # Royal card equal to itself
    assert ace == ace_hearts  # Check so that only value is considered
    assert h4 < jack < queen < king < ace  # Value ordering

    with pytest.raises(TypeError):
        pc = PlayingCard(Suit.Clubs)


# This test assumes you call your shuffle method "shuffle" and the method to draw a card "draw"
def test_deck():
    d = StandardDeck()
    c1 = d.draw()
    c2 = d.draw()
    assert not c1 == c2

    d2 = StandardDeck()
    d2.shuffle()
    c3 = d2.draw()
    c4 = d2.draw()
    assert not ((c3, c4) == (c1, c2))

    d3 = StandardDeck()
    d3.shuffle()
    c5 = d3.draw()
    c6 = d3.draw()
    assert len(d3.cards) == 50

    # Check so the deck "understand" that a card has been drawn
    deck = []
    deck = [deck.append(d3.draw()) for item in range(len(d3.cards))]
    assert len(deck) == 50

    # Check so that those exact cards are not in the deck anymore
    assert c5 not in d3.cards and c6 not in d3.cards

    # Draw all remaining cards from the deck
    remaining_cards = [d3.draw() for _ in range(len(d3.cards))]
    assert len(remaining_cards) == 50  # Ensure full deck was drawn


# This test builds on the assumptions above and assumes you store the cards in the hand in the list "cards",
# and that your sorting method is called "sort" and sorts in increasing order
def test_hand():
    h = Hand()
    assert len(h.cards) == 0
    d = StandardDeck()
    d.shuffle()
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    assert len(h.cards) == 5

    h.sort()
    for i in range(4):
        assert h.cards[i] < h.cards[i + 1] or h.cards[i] == h.cards[i + 1]

    cards = h.cards.copy()
    h.drop_cards([3, 0, 1])
    assert len(h.cards) == 2
    assert h.cards[0] == cards[2]
    assert h.cards[1] == cards[4]

    # Adds to determined card to the hand to check if it drops the intended card and that size of hand is correct
    h2 = Hand()

    h2.add_card(NumberedCard(9, Suit.Clubs))
    h2.add_card(JackCard(Suit.Hearts))
    assert len(h2.cards) == 2
    h2.drop_cards([0])
    assert len(h2.cards) == 1
    assert h2.cards[0] == JackCard(Suit.Hearts)


# This test builds on the assumptions above. Add your type and data for the commented out tests
# and uncomment them!
def test_pokerhands():
    h1 = Hand()
    h1.add_card(QueenCard(Suit.Diamonds))
    h1.add_card(KingCard(Suit.Hearts))

    h2 = Hand()
    h2.add_card(QueenCard(Suit.Hearts))
    h2.add_card(AceCard(Suit.Hearts))

    cl = [
        NumberedCard(10, Suit.Diamonds),
        NumberedCard(9, Suit.Diamonds),
        NumberedCard(8, Suit.Clubs),
        NumberedCard(6, Suit.Spades),
    ]

    ph1 = h1.best_poker_hand(cl)
    assert isinstance(ph1, PokerHand)
    ph2 = h2.best_poker_hand(cl)

    assert ph1 < ph2

    cl.pop(0)
    cl.append(QueenCard(Suit.Spades))
    ph3 = h1.best_poker_hand(cl)
    ph4 = h2.best_poker_hand(cl)
    assert ph3 < ph4
    assert ph1 < ph2

    cl = [
        QueenCard(Suit.Clubs),
        QueenCard(Suit.Spades),
        KingCard(Suit.Clubs),
        KingCard(Suit.Spades),
    ]
    ph5 = h1.best_poker_hand(cl)
    # assert # Check ph5 handtype class and data here>

    # Check that flush > straight
    h1 = Hand()
    h1.add_card(JackCard(Suit.Clubs))
    h1.add_card(QueenCard(Suit.Clubs))

    h2 = Hand()
    h2.add_card(NumberedCard(2, Suit.Hearts))
    h2.add_card(NumberedCard(3, Suit.Hearts))

    cards_on_table = [
        NumberedCard(4, Suit.Clubs),
        NumberedCard(5, Suit.Clubs),
        NumberedCard(6, Suit.Clubs),
        AceCard(Suit.Spades),
        AceCard(Suit.Diamonds),
    ]

    poker_hand1 = h1.best_poker_hand(cards_on_table)  # Flush hand
    poker_hand2 = h2.best_poker_hand(cards_on_table)  # Straight hand

    assert poker_hand1 > poker_hand2

    # Check that two fullhouses with same values equal each other
    h3 = Hand()
    h3.add_card(NumberedCard(2, Suit.Spades))
    h3.add_card(NumberedCard(3, Suit.Clubs))

    h4 = Hand()
    h4.add_card(NumberedCard(2, Suit.Hearts))
    h4.add_card(NumberedCard(3, Suit.Diamonds))

    cards_on_table = [
        NumberedCard(2, Suit.Diamonds),
        NumberedCard(2, Suit.Clubs),
        NumberedCard(3, Suit.Spades),
        KingCard(Suit.Spades),
        QueenCard(Suit.Clubs),
    ]

    poker_hand3 = h3.best_poker_hand(cards_on_table)  # Fullhouse hand one
    poker_hand4 = h4.best_poker_hand(cards_on_table)  # Fullhouse hand two

    assert poker_hand3 == poker_hand4

    # Check that a fullhouse with higher three is more valued than other fullhouse

    h3 = Hand()
    h3.add_card(NumberedCard(2, Suit.Spades))
    h3.add_card(NumberedCard(4, Suit.Clubs))

    h4 = Hand()
    h4.add_card(NumberedCard(2, Suit.Hearts))
    h4.add_card(NumberedCard(3, Suit.Diamonds))

    cards_on_table = [
        NumberedCard(3, Suit.Hearts),
        NumberedCard(2, Suit.Clubs),
        NumberedCard(3, Suit.Spades),
        NumberedCard(4, Suit.Spades),
        NumberedCard(4, Suit.Hearts),
    ]

    poker_hand3 = h3.best_poker_hand(cards_on_table)  # Fullhouse hand with higher three
    poker_hand4 = h4.best_poker_hand(cards_on_table)  # Fullhouse hand with lesser three

    assert poker_hand3 > poker_hand4

    # Checking two hands with different high card
    h3.drop_cards([1])
    h4.drop_cards([1])

    h3.add_card(QueenCard(Suit.Hearts))
    h4.add_card(KingCard(Suit.Hearts))

    poker_hand5 = h3.best_poker_hand(cards_on_table)  # Pair hand with lesser high card
    poker_hand6 = h4.best_poker_hand(cards_on_table)  # Pair hand with highest high card
    assert poker_hand6 > poker_hand5

    # Check of ordering of all already created hands
    # fullhouse > flush > straight > pair
    assert poker_hand3 > poker_hand1 > poker_hand2 > poker_hand5

    # Test for three of a kind and straight
    h5 = Hand()
    h5.add_card(NumberedCard(4, Suit.Hearts))
    h5.add_card(NumberedCard(9, Suit.Hearts))

    cards_on_table.pop(0)
    cards_on_table.append(NumberedCard(10, Suit.Clubs))

    poker_hand7 = h5.best_poker_hand(cards_on_table)

    assert poker_hand2 > poker_hand7

    # Comparison of hands with two pair where one hand has the highest pair
    h1 = Hand()
    h1.add_card(QueenCard(Suit.Diamonds))
    h1.add_card(KingCard(Suit.Hearts))

    h2 = Hand()
    h2.add_card(QueenCard(Suit.Hearts))
    h2.add_card(AceCard(Suit.Hearts))

    cl = [
        AceCard(Suit.Diamonds),
        KingCard(Suit.Diamonds),
        QueenCard(Suit.Clubs),
        NumberedCard(6, Suit.Spades),
        NumberedCard(3, Suit.Clubs),
    ]

    ph1 = h1.best_poker_hand(cl)
    ph2 = h2.best_poker_hand(cl)
    assert ph2 > ph1

    # The hands have the same highest pair but different pair for second
    cl.sort()
    h2.drop_cards([1])
    h2.drop_cards([0])
    h2.add_card(KingCard(Suit.Clubs))
    h2.add_card(NumberedCard(6, Suit.Clubs))
    ph1 = h1.best_poker_hand(cl)
    ph2 = h2.best_poker_hand(cl)
    assert ph1 > ph2

    # Same pairs with different high card
    h1.drop_cards([0])
    h1.add_card(NumberedCard(10, Suit.Clubs))
    h2.drop_cards([1])
    h2.add_card(NumberedCard(8, Suit.Hearts))
    ph1 = h1.best_poker_hand(cl)
    ph2 = h2.best_poker_hand(cl)
    assert ph1 > ph2

    # Three of a kind with different high card
    h3 = Hand()
    h3.add_card(NumberedCard(2, Suit.Spades))
    h3.add_card(NumberedCard(2, Suit.Clubs))

    h4 = Hand()
    h4.add_card(NumberedCard(3, Suit.Hearts))
    h4.add_card(NumberedCard(3, Suit.Diamonds))

    cards_on_table = [
        NumberedCard(2, Suit.Diamonds),
        NumberedCard(10, Suit.Clubs),
        NumberedCard(3, Suit.Spades),
        KingCard(Suit.Clubs),
        QueenCard(Suit.Clubs),
    ]

    poker_hand3 = h3.best_poker_hand(cards_on_table)
    poker_hand4 = h4.best_poker_hand(cards_on_table)
    assert poker_hand4 > poker_hand3

    # Flush with different high card
    h3 = Hand()
    h3.add_card(NumberedCard(5, Suit.Hearts))
    h3.add_card(NumberedCard(2, Suit.Hearts))

    h4 = Hand()
    h4.add_card(NumberedCard(3, Suit.Hearts))
    h4.add_card(NumberedCard(9, Suit.Hearts))

    cards_on_table = [
        NumberedCard(4, Suit.Hearts),
        NumberedCard(10, Suit.Hearts),
        NumberedCard(7, Suit.Hearts),
        KingCard(Suit.Clubs),
        QueenCard(Suit.Clubs),
    ]

    poker_hand3 = h3.best_poker_hand(cards_on_table)
    poker_hand4 = h4.best_poker_hand(cards_on_table)
    assert poker_hand4 > poker_hand3
