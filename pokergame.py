from pokerview import *
import sys


def main():
    qt_app = QApplication(sys.argv)
    player_1 = input("Enter Player 1's name:\n")
    player_2 = input("Enter Player 2's name:\n")
    game = TexasHoldEm([Player(player_1), Player(player_2)])
    win = MyWindow(game)
    win.show()

    qt_app.exec_()


if __name__ == '__main__':
    main()
