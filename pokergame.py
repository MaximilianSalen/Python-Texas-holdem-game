from pokerview import *
import sys


def main():
    qt_app = QApplication(sys.argv)
    player_1 = input("Enter Player 1's name:\n")
    player_2 = input("Enter Player 2's name:\n")
    starting_money = int(input("Enter starting money:\n"))
    game = TexasHoldEm([Player(player_1, starting_money), Player(player_2, starting_money)])
    win = MyWindow(game)
    win.show()

    qt_app.exec_()


if __name__ == '__main__':
    main()
