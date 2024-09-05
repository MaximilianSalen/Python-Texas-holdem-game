import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from poker_module.cardlib import *

def test_straight_flush():
    cards = [
        NumberedCard(10, Suit.Hearts),
        NumberedCard(9, Suit.Hearts),
        NumberedCard(8, Suit.Hearts),
        NumberedCard(7, Suit.Hearts),
        NumberedCard(6, Suit.Hearts)
    ]
    poker_hand = PokerHand(cards)
    assert poker_hand.type == HandType.STRAIGHT_FLUSH

def test_full_house():
    cards = [
        NumberedCard(3, Suit.Clubs),
        NumberedCard(3, Suit.Spades),
        NumberedCard(3, Suit.Hearts),
        NumberedCard(2, Suit.Diamonds),
        NumberedCard(2, Suit.Clubs)
    ]
    poker_hand = PokerHand(cards)
    assert poker_hand.type == HandType.FULL_HOUSE

def test_high_card():
    cards = [
        NumberedCard(2, Suit.Clubs),
        NumberedCard(5, Suit.Spades),
        NumberedCard(7, Suit.Hearts),
        NumberedCard(10, Suit.Diamonds),
        NumberedCard(11, Suit.Clubs)
    ]
    poker_hand = PokerHand(cards)
    assert poker_hand.type == HandType.HIGH_CARD