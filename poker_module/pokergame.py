from pokerview import *
import sys


def main():
    qt_app = QApplication(sys.argv)
    init_window = InitializationWindow()
    init_window.show()

    qt_app.exec_()


if __name__ == "__main__":
    main()
