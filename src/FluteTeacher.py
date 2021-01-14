from PyQt5.QtWidgets import *
from .Staff import Staff
from .Note import Note
from .Fingering import Fingering


class FluteTeacher:
    def __init__(self, width=800, height=600):
        self.wanted_note = -12

        # main window
        self._window = QWidget()
        screen_size = qApp.desktop().availableGeometry().size()
        top_x = (screen_size.width() // 2) - (width // 2)
        top_y = (screen_size.height() // 2) - (height // 2)
        self._window.setGeometry(top_x, top_y, width, height)
        self._window.setWindowTitle("FluteTeacher")

        # first row
        self._top_row = QGroupBox()
        self._top_row_layout = QHBoxLayout()
        self._top_row.setLayout(self._top_row_layout)

        self._left_staff = Staff(kind='normal')
        self._top_row_layout.addWidget(self._left_staff)

        self._right_staff = Staff(kind='normal')
        self._top_row_layout.addWidget(self._right_staff)

        # second row
        self.fingering = Fingering()

        # bottom row
        self._bottom_row = QGroupBox()
        self._bottom_row_layout = QHBoxLayout()
        self._bottom_row.setLayout(self._bottom_row_layout)
        self._next_button = QPushButton('next')
        # self._next_button.setFixedHeight(100)
        self._next_button.clicked.connect(self.next_note)
        self._bottom_row_layout.addWidget(self._next_button)

        # main grid
        self._grid = QGridLayout()
        self._grid.addWidget(self._top_row)
        self._grid.addWidget(self.fingering)
        self._grid.addWidget(self._bottom_row)

        self._window.setLayout(self._grid)
        self._window.show()

        self.last_note = None

    def next_note(self):
        self.last_note = Note.random(difficulty=1, lastNote=self.last_note)
        note, alt = self.last_note.to_graph()
        self._left_staff.display_note(note, alt)
        self.fingering.set_fingering(self.last_note.a4index)

