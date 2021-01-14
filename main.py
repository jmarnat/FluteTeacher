from PyQt5.QtWidgets import QApplication
import sys
from src.FluteTeacher import FluteTeacher


def main():
    app = QApplication(sys.argv)
    flute_teacher = FluteTeacher()
    flute_teacher.next_note()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
