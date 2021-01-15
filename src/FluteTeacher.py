import threading
from time import sleep
from PyQt5.QtWidgets import *
from .Staff import Staff
from .Note import Note
from .Fingering import Fingering
from .HearAI import HearAI

VALIDATE_NOTE = True
BLINKING_TIME = 1
BLINKING_LOOPS = 3


class FluteTeacher:
    def __init__(self, width=800, height=600):
        self._current_note = None
        self._heard_note = None
        self._is_hearing = False
        self._autonext = False

        # ================================================= #
        #                   USER INTERFACE                  #
        # ================================================= #

        # main window
        self._window = QWidget()
        screen_size = qApp.desktop().availableGeometry().size()
        top_x = (screen_size.width() // 2) - (width // 2)
        top_y = (screen_size.height() // 2) - (height // 2)
        self._window.setGeometry(top_x, top_y, width, height)
        # self._window.setGeometry(10, 10, width, height)
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
        self._next_button.clicked.connect(self.next_note)
        # self._next_button.onc
        self._bottom_row_layout.addWidget(self._next_button)

        self._button_autonext = QPushButton('Enable AutoNext' if not self._autonext else 'Disable AutoNext')
        self._button_autonext.clicked.connect(self.toggle_autonext)
        self._bottom_row_layout.addWidget(self._button_autonext)

        self._button_listening = QPushButton('Start listening' if not self._is_hearing else 'Stop listening')
        self._button_listening.clicked.connect(self.toggle_listening)
        self._bottom_row_layout.addWidget(self._button_listening)

        # main grid
        self._grid = QGridLayout()
        self._grid.addWidget(self._top_row)
        self._grid.addWidget(self.fingering)
        self._grid.addWidget(self._bottom_row)

        self._window.setLayout(self._grid)
        self._window.show()

        # ================================================= #
        #                NOTE RECOGNITION                   #
        # ================================================= #
        self._hear_ai = HearAI()

    def toggle_autonext(self):
        self._autonext = not self._autonext

        if self._autonext:
            self._button_autonext.setText('Disable AutoNext')
        else:
            self._button_autonext.setText('Enable AutoNext')

    def hearing_loop(self):
        while self._is_hearing:
            dec = self.hear_sample()

            if self._autonext and (dec == 0):
                self.next_note()

            self._window.update()

    def toggle_listening(self):
        self._is_hearing = not self._is_hearing

        if self._is_hearing:
            self._button_listening.setText('Stop listening')
            thr = threading.Thread(target=self.hearing_loop)
            thr.start()
        else:
            self._button_listening.setText('Start listening')
            self._right_staff.erase_note()

    def next_note(self):
        if (self._current_note is not None) and VALIDATE_NOTE:
            (_note, _alt) = self._current_note.to_graph()
            btime = (BLINKING_TIME / (2 * BLINKING_LOOPS))
            for blink_loop in range(BLINKING_LOOPS):
                self._left_staff.display_note(_note, _alt, ndec=0)
                self._right_staff.display_note(_note, _alt, ndec=0)
                sleep(btime)
                self._left_staff.erase_note()
                self._right_staff.erase_note()
                sleep(btime)

        self._current_note = Note.random(difficulty=1, last_note=self._current_note)
        (_note, _alt) = self._current_note.to_graph()
        self._left_staff.display_note(_note, _alt)
        self.fingering.set_fingering(self._current_note.a4index())

    def hear_sample(self):
        self._hear_ai.record(millis=200)
        heard_note = self._hear_ai.get_last_note()

        if heard_note is not None:
            self._heard_note = heard_note
            (b_index, alt) = heard_note.to_graph()
            dec = heard_note.a4index() - self._current_note.a4index()
            self._right_staff.display_note(b_index=b_index, alt=alt, ndec=dec)
            return dec

        self._right_staff.erase_note()
        return None
