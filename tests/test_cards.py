import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from poker_module.cardlib import *
import pytest


def test_numbered_card():
    card = NumberedCard(5, Suit.Spades)
    assert card.get_value() == 5
    assert str(card) == "5 of Spades"

def test_jack_card():
    card = JackCard(Suit.Hearts)
    assert card.get_value() == 11
    assert str(card) == "Jack of Hearts"

def test_queen_card():
    card = QueenCard(Suit.Clubs)
    assert card.get_value() == 12
    assert str(card) == "Queen of Clubs"

def test_king_card():
    card = KingCard(Suit.Diamonds)
    assert card.get_value() == 13
    assert str(card) == "King of Diamonds"

def test_ace_card():
    card = AceCard(Suit.Spades)
    assert card.get_value() == 14
    assert str(card) == "Ace of Spades"
