from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from cardlib import *
from typing import Dict, Tuple
from pokermodel import *


class TableScene(QGraphicsScene):
    """A scene with a table cloth background"""

    def __init__(self) -> None:
        super().__init__()
        self.tile = QPixmap("cards/table.png")
        self.setBackgroundBrush(QBrush(self.tile))


class CardItem(QGraphicsSvgItem):
    """A simple overloaded QGraphicsSvgItem that also stores the card position"""

    def __init__(self, renderer: QSvgRenderer, position: int) -> None:
        super().__init__()
        self.setSharedRenderer(renderer)
        self.position = position


def read_cards() -> Dict[Tuple[int, Suit], QSvgRenderer]:
    """
    Reads all the 52 cards from files.
    :return: Dictionary of SVG renderers
    """
    all_cards: Dict[Tuple[int, Suit], QSvgRenderer] = {}
    for suit_file, suit in zip("HSCD", Suit):
        for value_file, value in zip(
            ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"],
            range(2, 15),
        ):
            file = value_file + suit_file
            key = (value, suit)
            all_cards[key] = QSvgRenderer(f"cards/{file}.svg")
    return all_cards


class CardView(QGraphicsView):
    """A View widget that represents the table area displaying a player's cards."""

    back_card: QSvgRenderer = QSvgRenderer("cards/Red_Back_2.svg")
    all_cards: Dict[Tuple[int, Suit], QSvgRenderer] = read_cards()

    def __init__(
        self, card_model: CardModel, card_spacing: int = 250, padding: int = 10
    ) -> None:
        """
        Initializes the view to display the content of the given model
        :param card_model: A model that represents a set of cards. Needs to support the CardModel interface.
        :param card_spacing: Spacing between the visualized cards.
        :param padding: Padding of table area around the visualized cards.
        """
        self.scene = TableScene()
        super().__init__(self.scene)

        self.card_spacing = card_spacing
        self.padding = padding

        self.model = card_model
        card_model.new_cards.connect(self.__change_cards)

        self.__change_cards()

    def __change_cards(self) -> None:
        """Private method to update the cards in the view."""
        self.scene.clear()
        for i, card in enumerate(self.model):
            graphics_key = (card.get_value(), card.suit)
            renderer = (
                self.back_card if self.model.flipped() else self.all_cards[graphics_key]
            )
            c = CardItem(renderer, i)

            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.0)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180))
            c.setGraphicsEffect(shadow)

            c.setPos(c.position * self.card_spacing, 0)
            self.scene.addItem(c)

        self.update_view()

    def update_view(self) -> None:
        scale = (self.viewport().height() - 2 * self.padding) / 313
        self.resetTransform()
        self.scale(scale, scale)
        self.setSceneRect(
            -self.padding // scale,
            -self.padding // scale,
            self.viewport().width() // scale,
            self.viewport().height() // scale,
        )

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.update_view()
        super().resizeEvent(event)


class ActionBar(QGroupBox):
    def __init__(self, game: TexasHoldEm) -> None:
        super().__init__()
        self.game = game
        self.pot = QLabel()
        self.active_label = QLabel()
        self.blind_label = QLabel()
        self.bet = QPushButton("Bet")
        self.betting_amount = QSpinBox()
        self.betting_amount.setMinimum(50)
        self.call = QPushButton("Call")
        self.check = QPushButton("Check")
        self.fold = QPushButton("Fold")

        vbox = QVBoxLayout()
        vbox.addWidget(self.active_label)
        vbox.addWidget(self.blind_label)
        vbox.addWidget(self.pot)
        vbox.addWidget(self.betting_amount)
        vbox.addWidget(self.bet)
        vbox.addWidget(self.call)
        vbox.addWidget(self.check)
        vbox.addWidget(self.fold)

        self.setLayout(vbox)

        game.pot.new_value.connect(self.update_pot)
        game.active_player_changed.connect(self.update_active_player)
        game.active_player_changed.connect(self.update_maximum_bet)
        game.active_player_changed.connect(self.update_blind)

        self.update_pot()
        self.update_active_player()
        self.update_maximum_bet()
        self.update_blind()

        self.bet.clicked.connect(lambda: game.bet(self.betting_amount.value()))
        self.call.clicked.connect(game.call)
        self.check.clicked.connect(game.check)
        self.fold.clicked.connect(game.fold)

    def update_pot(self) -> None:
        self.pot.setText(f"Pot\n$ {self.game.pot.value}")

    def update_active_player(self) -> None:
        self.active_label.setText(str(self.game.the_active_player_name))

    def update_maximum_bet(self) -> None:
        self.betting_amount.setMaximum(self.game.the_active_player_money)

    def update_blind(self) -> None:
        self.blind_label.setText(f"Blind: {self.game.blind_player_name}")


class PlayerView(QGroupBox):
    def __init__(self, player: "Player", game: TexasHoldEm) -> None:
        super().__init__(player.name)
        self.player = player
        self.money_label = QLabel()

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        vbox.addWidget(self.money_label)
        vbox.addStretch(1)

        hand_card_view = CardView(player.hand)
        vbox.addWidget(hand_card_view)

        self.game = game
        player.money.new_value.connect(self.update_money)

        self.update_money()
        self.set_bold_title()

    def update_money(self) -> None:
        self.money_label.setText(f"Money\n$ {self.player.money.value}")

    def set_bold_title(self) -> None:
        font = QFont()
        font.setBold(True)
        self.setFont(font)


class GameView(QWidget):
    def __init__(self, game: TexasHoldEm) -> None:
        super().__init__()
        hbox = QHBoxLayout()
        table_card_view = CardView(game.table)
        hbox.addWidget(table_card_view)

        self.setLayout(hbox)
        self.game = game
        game.game_message.connect(self.game_alerts)

    @staticmethod
    def game_alerts(text: str) -> None:
        msg = QMessageBox()
        msg.setText(text)
        msg.exec_()


class GraphicView(QGroupBox):
    def __init__(self, game: TexasHoldEm) -> None:
        super().__init__()
        self.game = game

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        vbox.addWidget(PlayerView(game.players[0], game))
        vbox.addWidget(GameView(game))
        vbox.addWidget(PlayerView(game.players[1], game))


class MyWindow(QMainWindow):
    def __init__(self, game: TexasHoldEm) -> None:
        super().__init__()
        widget = QWidget()
        self.game = game

        layout = QHBoxLayout()
        layout.addWidget(GraphicView(game))
        layout.addWidget(ActionBar(game))
        widget.setLayout(layout)
        self.setCentralWidget(widget)
