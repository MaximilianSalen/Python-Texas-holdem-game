from enum import Enum
from abc import ABC, abstractmethod
from random import shuffle
from collections import Counter
from typing import List, Tuple, Optional


class Suit(Enum):
    """
    Class of Enum type implemented in order to sort using the __lt__ operator
    """

    Hearts = 3
    Spades = 2
    Clubs = 1
    Diamonds = 0

    def __str__(self) -> str:
        return self.name


class PlayingCard(ABC):
    """
    Is an abstract base class, which will work as a blueprint for creating the cards.
    """

    def __init__(self, suit: Suit) -> None:
        """
        Constructs suit
        :param suit:
        """
        self.suit = suit

    @abstractmethod
    def get_value(self) -> int:
        """
        Abstract method for retrieving values of cards, serves as a contract: in order to be considered a card
        this method must be implemented in the card.
        """
        pass

    def __eq__(self, other: "PlayingCard") -> bool:
        return self.get_value() == other.get_value()

    def __lt__(self, other: "PlayingCard") -> bool:
        return self.get_value() < other.get_value()


class NumberedCard(PlayingCard):
    """
    Subclass of PlayingCard which it inherits from. Subclass is the numbered cards in a deck.
    """

    def __init__(self, value: int, suit: Suit) -> None:
        self.value = value
        super().__init__(suit)

    def get_value(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return f"{str(self.value)} of {str(self.suit.name)}"


class JackCard(PlayingCard):
    def get_value(self) -> int:
        return 11

    def __repr__(self) -> str:
        return f"Jack of {self.suit.name}"


class QueenCard(PlayingCard):
    def get_value(self) -> int:
        return 12

    def __repr__(self) -> str:
        return f"Queen of {self.suit.name}"


class KingCard(PlayingCard):
    def get_value(self) -> int:
        return 13

    def __repr__(self) -> str:
        return f"King of {self.suit.name}"


class AceCard(PlayingCard):
    def get_value(self) -> int:
        return 14

    def __repr__(self) -> str:
        return f"Ace of {self.suit.name}"


class StandardDeck:
    """
    Class that creates the deck of cards containing 52 unique cards, incorporates methods for shuffling the deck and
    drawing cards.
    """

    def __init__(self) -> None:
        self.cards: List[PlayingCard] = []

        for suit in Suit:
            self.cards.append(AceCard(suit))
            self.cards.append(KingCard(suit))
            self.cards.append(QueenCard(suit))
            self.cards.append(JackCard(suit))
            for value in range(2, 11):
                self.cards.append(NumberedCard(value, suit))

    def shuffle(self) -> None:
        shuffle(self.cards)

    def draw(self) -> PlayingCard:
        return self.cards.pop(0)

    def __repr__(self) -> str:
        return str(self.cards)


class Hand:
    """
    Class that represents a player's hand with methods that add, drop and sorting cards. It also includes a method that
    returns the best poker hand based on the cards on the table and the cards on the hand.
    """

    def __init__(self) -> None:
        self.cards: List[PlayingCard] = []

    def add_card(self, card: PlayingCard) -> None:
        self.cards.append(card)

    def drop_cards(self, indices: List[int]) -> None:
        for index in sorted(indices, reverse=True):
            del self.cards[index]

    def sort(self) -> None:
        self.cards.sort()

    def best_poker_hand(self, cards: List[PlayingCard] = []) -> "PokerHand":
        return PokerHand(self.cards + cards)

    def __repr__(self) -> str:
        return str(self.cards)


class HandType(Enum):
    """
    Enum class that assigns a value to each hand type.
    """

    STRAIGHT_FLUSH = 9
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    THREE_OF_A_KIND = 4
    TWO_PAIRS = 3
    PAIR = 2
    HIGH_CARD = 1

    def __lt__(self, other: "HandType") -> bool:
        return self.value < other.value

    def __eq__(self, other: "HandType") -> bool:
        return self.value == other.value


class PokerHand:
    """
    Class that checks the hand type of the poker hand.
    """

    def __init__(self, cards: List[PlayingCard]) -> None:
        self.cards = sorted(cards, reverse=True)
        checkers = [
            self.check_straight_flush,
            self.check_four_of_a_kind,
            self.check_full_house,
            self.check_flush,
            self.check_straight,
            self.check_diff_pairs,
        ]

        for checker in checkers:
            result = checker(self.cards)
            if result:
                self.type, self.values = result
                break

    def __lt__(self, other: "PokerHand") -> bool:
        return (self.type, self.values) < (other.type, other.values)

    def __eq__(self, other: "PokerHand") -> bool:
        return (self.type, self.values) == (other.type, other.values)

    @staticmethod
    def check_straight_flush(
        cards: List[PlayingCard],
    ) -> Optional[Tuple[HandType, List[PlayingCard]]]:
        vals = [(c.get_value(), c.suit) for c in cards] + [
            (1, c.suit) for c in cards if c.get_value() == 14
        ]
        for c in reversed(cards):
            if all((c.get_value() - k, c.suit) in vals for k in range(1, 5)):
                return HandType.STRAIGHT_FLUSH, cards[:7]
        return None

    @staticmethod
    def check_four_of_a_kind(
        cards: List[PlayingCard],
    ) -> Optional[Tuple[HandType, List[PlayingCard]]]:
        value_count = Counter(c.get_value() for c in cards)
        if any(count >= 4 for count in value_count.values()):
            return HandType.FOUR_OF_A_KIND, cards[:7]
        return None

    @staticmethod
    def check_full_house(
        cards: List[PlayingCard],
    ) -> Optional[Tuple[HandType, Tuple[int, int]]]:
        value_count = Counter(c.get_value() for c in cards)
        threes = [v for v, count in value_count.items() if count >= 3]
        twos = [v for v, count in value_count.items() if count >= 2]
        if threes and twos:
            return HandType.FULL_HOUSE, (threes[0], twos[0])
        return None

    @staticmethod
    def check_flush(
        cards: List[PlayingCard],
    ) -> Optional[Tuple[HandType, List[PlayingCard]]]:
        suit_count = Counter(c.suit for c in cards)
        if any(count >= 5 for count in suit_count.values()):
            return HandType.FLUSH, cards[:7]
        return None

    @staticmethod
    def check_straight(
        cards: List[PlayingCard],
    ) -> Optional[Tuple[HandType, List[PlayingCard]]]:
        vals = [c.get_value() for c in cards] + [
            1 for c in cards if c.get_value() == 14
        ]
        for c in reversed(cards):
            if all(c.get_value() - k in vals for k in range(1, 5)):
                return HandType.STRAIGHT, cards[:7]
        return None

    @staticmethod
    def check_diff_pairs(
        cards: List[PlayingCard],
    ) -> Tuple[HandType, List[PlayingCard]]:
        value_count = Counter(c.get_value() for c in cards)
        twos = sorted(
            (v for v, count in value_count.items() if count >= 2), reverse=True
        )
        threes = sorted(
            (v for v, count in value_count.items() if count >= 3), reverse=True
        )
        if threes:
            return HandType.THREE_OF_A_KIND, cards[:7]
        elif len(twos) >= 2:
            return HandType.TWO_PAIRS, cards[:7]
        elif len(twos) == 1:
            return HandType.PAIR, cards[:7]
        return HandType.HIGH_CARD, cards[:7]

    def __repr__(self) -> str:
        return f"{self.type}, {self.values}"
