from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import *
import sys
from src.FluteTeacher import FluteTeacher


class MainApp(QApplication):
    def __init__(self, argv):
        super(MainApp, self).__init__(argv)

    def quit(self):
        print('bye bye')
        exit(0)


def main():
    app = MainApp(sys.argv)
    FluteTeacher()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
