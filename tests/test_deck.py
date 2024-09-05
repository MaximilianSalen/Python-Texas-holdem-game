import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from poker_module.cardlib import *

def test_deck_has_52_cards():
    deck = StandardDeck()
    assert len(deck.cards) == 52

def test_draw_card():
    deck = StandardDeck()
    card = deck.draw()
    assert isinstance(card, PlayingCard)

def test_shuffle_changes_order():
    deck = StandardDeck()
    original_order = deck.cards.copy()
    deck.shuffle()
    assert original_order != deck.cards  # Order should change

def test_draw_from_empty_deck():
    deck = StandardDeck()
    for _ in range(52):
        deck.draw()
    with pytest.raises(IndexError):  # Assuming the draw method raises an IndexError
        deck.draw()