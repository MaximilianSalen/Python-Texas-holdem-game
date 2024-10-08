import sys
from abc import abstractmethod
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *


###################
# Models
###################


class CardModel(QObject):
    """Base class that described what is expected from the CardView widget"""

    new_cards = pyqtSignal()  #: Signal should be emited when cards change.

    @abstractmethod
    def __iter__(self):
        """Returns an iterator of card objects"""

    @abstractmethod
    def flipped(self):
        """Returns true of cards should be drawn face down"""


# A trivial card class
class MySimpleCard:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def get_value(self):
        return self.value


class Hand:
    def __init__(self):
        # Lets use some hardcoded values for most of this to start with
        self.cards = [MySimpleCard(13, 2), MySimpleCard(7, 0), MySimpleCard(13, 1)]

    def add_card(self, card):
        self.cards.append(card)


class HandModel(Hand, CardModel):
    def __init__(self):
        Hand.__init__(self)
        CardModel.__init__(self)
        # Additional state needed by the UI
        self.flipped_cards = False

    def __iter__(self):
        return iter(self.cards)

    def flip(self):
        # Flips over the cards (to hide them)
        self.flipped_cards = not self.flipped_cards
        self.new_cards.emit()  # something changed, better emit the signal!

    def flipped(self):
        # This model only flips all or no cards, so we don't care about the index.
        return self.flipped_cards

    def add_card(self, card):
        super().add_card(card)
        self.new_cards.emit()  # something changed, better emit the signal!


###################
# Card widget code:
###################


class TableScene(QGraphicsScene):
    """A scene with a table cloth background"""

    def __init__(self):
        super().__init__()
        self.tile = QPixmap("poker_module/cards/table.png")
        self.setBackgroundBrush(QBrush(self.tile))


class CardItem(QGraphicsSvgItem):
    """A simple overloaded QGraphicsSvgItem that also stores the card position"""

    def __init__(self, renderer, position):
        super().__init__()
        self.setSharedRenderer(renderer)
        self.position = position


def read_cards():
    """
    Reads all the 52 cards from files.
    :return: Dictionary of SVG renderers
    """
    all_cards = (
        dict()
    )  # Dictionaries let us have convenient mappings between cards and their images
    for suit_file, suit in zip("HDSC", range(4)):
        for value_file, value in zip(
            ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"],
            range(2, 15),
        ):
            file = value_file + suit_file
            key = (value, suit)  # tuple to be the key for this dictionary
            all_cards[key] = QSvgRenderer("poker_module/cards/" + file + ".svg")
    return all_cards


class CardView(QGraphicsView):
    """A View widget that represents the table area displaying a players cards."""

    # We read all the card graphics as static class variables
    back_card = QSvgRenderer("poker_module/cards/Red_Back_2.svg")
    all_cards = read_cards()

    def __init__(
        self, card_model: CardModel, card_spacing: int = 250, padding: int = 10
    ):
        """
        Initializes the view to display the content of the given model
        :param cards_model: A model that represents a set of cards. Needs to support the CardModel interface.
        :param card_spacing: Spacing between the visualized cards.
        :param padding: Padding of table area around the visualized cards.
        """
        self.scene = TableScene()
        super().__init__(self.scene)

        self.card_spacing = card_spacing
        self.padding = padding

        self.model = card_model
        # Whenever the this window should update, it should call the "change_cards" method.

        card_model.new_cards.connect(self.change_cards)

        # Add the cards the first time around to represent the initial state.
        self.change_cards()

    def change_cards(self):
        # Add the cards from scratch
        self.scene.clear()
        for i, card in enumerate(self.model):
            # The ID of the card in the dictionary of images is a tuple with (value, suit), both integers
            graphics_key = (card.get_value(), card.suit)
            renderer = (
                self.back_card if self.model.flipped() else self.all_cards[graphics_key]
            )
            c = CardItem(renderer, i)

            # Shadow effects
            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.0)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180))  # Semi-transparent black
            c.setGraphicsEffect(shadow)

            # Place the cards on the default positions
            c.setPos(c.position * self.card_spacing, 0)
            # We could also do cool things like marking card by making them transparent
            # c.setOpacity(0.5 if self.model.marked(i) else 1.0)
            self.scene.addItem(c)

        self.update_view()

    def update_view(self):
        scale = (self.viewport().height() - 2 * self.padding) / 313
        self.resetTransform()
        self.scale(scale, scale)
        # Put the scene bounding box
        self.setSceneRect(
            -self.padding // scale,
            -self.padding // scale,
            self.viewport().width() // scale,
            self.viewport().height() // scale,
        )

    def resizeEvent(self, painter):
        # This method is called when the window is resized.
        # If the widget is resize, adjust the card sizes.
        # QGraphicsView automatically re-paints everything when we modify the scene.
        self.update_view()
        super().resizeEvent(painter)


###################
# Main test program
###################

# Lets test it out
app = QApplication(sys.argv)
hand = HandModel()

card_view = CardView(hand)

# Creating a small demo window to work with, and put the card_view inside:
box = QVBoxLayout()
box.addWidget(card_view)
player_view = QGroupBox("Player 1")
player_view.setLayout(box)
player_view.show()

app.exec_()
