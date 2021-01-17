from PyQt5.QtWidgets import QApplication
import sys
from src.FluteTeacher import FluteTeacher


def main():
    app = QApplication(sys.argv)
    FluteTeacher()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
