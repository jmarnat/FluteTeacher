from PyQt5.QtWidgets import QApplication

import sys

from src.SampleRecorder import SampleRecorder
from src.FluteTeacher import FluteTeacher

"""

TODO:
[x] add flat sign
[ ] corresp note number -> correct true note
[ ] upper right draw
[ ] flute draw
[ ] note recognition
[ ] recognized note display
[ ] automatic note validation 
"""


def main():
    app = QApplication(sys.argv)
    flute_teacher = FluteTeacher()
    flute_teacher.next_note()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
