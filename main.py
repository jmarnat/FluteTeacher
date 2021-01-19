from PyQt5.QtWidgets import QApplication
import sys
from src.FluteTeacher import FluteTeacher
from src.Settings import *


class MainApp(QApplication):
    def __init__(self, argv):
        super(MainApp, self).__init__(argv)
        self.setStyleSheet(Settings.MAIN_APP_STYLE_SHEET)

    def quit(self):
        print('bye bye')
        exit(0)


def main():
    app = MainApp(sys.argv)
    FluteTeacher()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
