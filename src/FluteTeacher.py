import threading
from time import sleep
from PyQt5.QtWidgets import *

from src.Staff import Staff
from src.Note import Note
from src.Fingering import Fingering
from src.HearAI import HearAI
from src.ScaleManager import ScaleManager
from src.Arpeggiator import ArpeggiatorV2
from src.Alteration import Alterations

VALIDATE_NOTE = True
BLINKING_TIME = 0.6
BLINKING_LOOPS = 3


class FluteTeacher:
    NOTE_MODE_RANDOM_1 = 1
    NOTE_MODE_RANDOM_2 = 2
    NOTE_MODE_SCALE = 0

    def __init__(self, width=800, height=600):
        self._current_note = None
        self._heard_note = None
        self._is_hearing = False
        self._autonext = False
        self._scale_manager = ScaleManager(scale_name='Major',
                                           mode=1,
                                           base_note=Note('C', 4, Alterations.NATURAL),
                                           arp=ArpeggiatorV2.THIRDS_UP)
        self._note_mode = FluteTeacher.NOTE_MODE_SCALE

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
        self._bottom_row_layout.addWidget(self._next_button)

        self._button_autonext = QPushButton('Enable AutoNext' if not self._autonext else 'Disable AutoNext')
        self._button_autonext.clicked.connect(self.toggle_autonext)
        self._bottom_row_layout.addWidget(self._button_autonext)

        self._button_listening = QPushButton('Start listening' if not self._is_hearing else 'Stop listening')
        self._button_listening.clicked.connect(self.toggle_listening)
        self._bottom_row_layout.addWidget(self._button_listening)

        self._button_debug_update = QPushButton('[debug redraw]')
        self._button_debug_update.clicked.connect(self.debug_update)
        self._bottom_row_layout.addWidget(self._button_debug_update)

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

    def debug_update(self):
        self._window.update()

    def toggle_autonext(self):
        self._autonext = not self._autonext

        if self._autonext:
            self._button_autonext.setText('Disable AutoNext')
        else:
            self._button_autonext.setText('Enable AutoNext')

    def hearing_loop(self):
        while self._is_hearing:
            dec = self.hear_sample()

            if self._autonext and (dec is not None) and (dec == 0):
                self.next_note(validate=True)

            # self._window.update()
            # print('window update ok')

    def toggle_listening(self):
        self._is_hearing = not self._is_hearing

        if self._is_hearing:
            self._button_listening.setText('Stop listening')
            thr = threading.Thread(target=self.hearing_loop)
            thr.start()
        else:
            self._button_listening.setText('Start listening')
            self._right_staff.erase_note()

    def blink_notes(self):
        btime = (BLINKING_TIME / (2 * BLINKING_LOOPS))
        for blink_loop in range(BLINKING_LOOPS):
            self._left_staff.display_note(self._current_note, ndec=0)
            self._right_staff.display_note(self._current_note, ndec=0)
            sleep(btime)
            self._left_staff.erase_note()
            self._right_staff.erase_note()
            sleep(btime)
        return

    def next_note(self, validate=False):
        if VALIDATE_NOTE and validate and (self._current_note is not None):
            thr = threading.Thread(target=self.blink_notes())
            print('blinking thread')
            thr.start()
            thr.join()
            print('done.')

        if self._note_mode == FluteTeacher.NOTE_MODE_RANDOM_1:
            self._current_note = Note.random_note(difficulty=1, last_note=self._current_note)
        elif self._note_mode == FluteTeacher.NOTE_MODE_RANDOM_2:
            self._current_note = Note.random_note(difficulty=2, last_note=self._current_note)
        elif self._note_mode == FluteTeacher.NOTE_MODE_SCALE:
            self._current_note = self._scale_manager.next_arp_note()
        else:
            exit(0)

        if self._current_note is None:
            print('ERROR: NEW NOTE IS NONE')
            exit(0)
        else:
            print('note_str:', self._current_note.to_str())

        self._left_staff.display_note(self._current_note)
        self.fingering.set_fingering(self._current_note)

    def hear_sample(self):
        self._hear_ai.record(millis=200)
        heard_note = self._hear_ai.get_last_note(alt=self._current_note.alt)

        if heard_note is not None:
            self._heard_note = heard_note
            dec = heard_note.midi_code - self._current_note.midi_code
            self._right_staff.display_note(heard_note, ndec=dec)
            return dec

        self._right_staff.erase_note()
        return None

    def set_scale(self, str_name):
        self._scale_manager = ScaleManager(str_name)
