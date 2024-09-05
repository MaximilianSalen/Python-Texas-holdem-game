import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from poker_module.cardlib import *


def test_high_card():
    cards = [
        NumberedCard(2, Suit.Clubs),
        NumberedCard(5, Suit.Spades),
        NumberedCard(7, Suit.Hearts),
        NumberedCard(10, Suit.Diamonds),
        NumberedCard(11, Suit.Clubs),
    ]
    poker_hand = PokerHand(cards)
    assert poker_hand.type == HandType.HIGH_CARD


def test_pair_hand():
    cards = [
        NumberedCard(3, Suit.Clubs),
        NumberedCard(3, Suit.Spades),
        NumberedCard(5, Suit.Hearts),
        NumberedCard(7, Suit.Diamonds),
        NumberedCard(10, Suit.Spades),
    ]
    poker_hand = PokerHand(cards)
    assert poker_hand.type == HandType.PAIR


def test_two_pair_hand():
    cards = [
        NumberedCard(3, Suit.Clubs),
        NumberedCard(3, Suit.Spades),
        NumberedCard(7, Suit.Hearts),
        NumberedCard(7, Suit.Diamonds),
        AceCard(Suit.Spades),
    ]
    poker_hand = PokerHand(cards)
    assert poker_hand.type == HandType.TWO_PAIRS


def test_three_of_a_kind():
    cards = [
        NumberedCard(4, Suit.Clubs),
        NumberedCard(4, Suit.Spades),
        NumberedCard(4, Suit.Hearts),
        NumberedCard(7, Suit.Diamonds),
        NumberedCard(10, Suit.Spades),
    ]
    poker_hand = PokerHand(cards)
    assert poker_hand.type == HandType.THREE_OF_A_KIND


def test_straight():
    cards = [
        NumberedCard(6, Suit.Hearts),
        NumberedCard(5, Suit.Spades),
        NumberedCard(4, Suit.Clubs),
        NumberedCard(3, Suit.Diamonds),
        NumberedCard(2, Suit.Hearts),
    ]
    poker_hand = PokerHand(cards)
    assert poker_hand.type == HandType.STRAIGHT


def test_flush():
    cards = [
        NumberedCard(2, Suit.Hearts),
        NumberedCard(5, Suit.Hearts),
        JackCard(Suit.Hearts),
        QueenCard(Suit.Hearts),
        KingCard(Suit.Hearts),
    ]
    poker_hand = PokerHand(cards)
    assert poker_hand.type == HandType.FLUSH


def test_full_house():
    cards = [
        NumberedCard(3, Suit.Clubs),
        NumberedCard(3, Suit.Spades),
        NumberedCard(3, Suit.Hearts),
        NumberedCard(2, Suit.Diamonds),
        NumberedCard(2, Suit.Clubs),
    ]
    poker_hand = PokerHand(cards)
    assert poker_hand.type == HandType.FULL_HOUSE


def test_straight_flush():
    cards = [
        NumberedCard(10, Suit.Hearts),
        NumberedCard(9, Suit.Hearts),
        NumberedCard(8, Suit.Hearts),
        NumberedCard(7, Suit.Hearts),
        NumberedCard(6, Suit.Hearts),
    ]
    poker_hand = PokerHand(cards)
    assert poker_hand.type == HandType.STRAIGHT_FLUSH


# Test Straight Flush Hand
def test_straight_flush():
    cards = [
        NumberedCard(10, Suit.Hearts),
        NumberedCard(9, Suit.Hearts),
        NumberedCard(8, Suit.Hearts),
        NumberedCard(7, Suit.Hearts),
        NumberedCard(6, Suit.Hearts),
    ]
    poker_hand = PokerHand(cards)
    assert poker_hand.type == HandType.STRAIGHT_FLUSH
