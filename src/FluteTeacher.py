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

from functools import partial

VALIDATE_NOTE = True
BLINKING_TIME = 0.6
BLINKING_LOOPS = 3


class MenuBar(QMenuBar):
    def __init__(self, parent, flute_teacher):
        super(MenuBar, self).__init__(parent)
        self._ft = flute_teacher
        # self._init_actions()
        # self._init_menus()

        # def _init_actions(self):
        self._exit_action = QAction(' &Quit FluteTeacher', self)
        self._exit_action.setShortcut('Ctrl+Q')
        self._exit_action.triggered.connect(qApp.quit)

        # def _init_menus(self):
        self._menu_file = self.addMenu('&File')
        self._menu_file.addAction(self._exit_action)

        # actions_scale = [
        #     QAction('C Major', self),
        #     QAction('D Major', self)
        # ]
        self._menu_training = self.addMenu('Training')
        self._menu_scales = self._menu_training.addMenu('Scales')
        # self._menu_scales_list = []

        self._scale_actions = dict()

        for scale_name in ScaleManager.VALID_SCALES.keys():
            local_menu_scale = self._menu_scales.addMenu(scale_name)
            # self._menu_scales_list.append()

            for scale_alt_str in ScaleManager.VALID_SCALES[scale_name].keys():
                alt_dict = {'': 'Naturals', '#': 'Sharps', 'b': 'Flats'}
                local_menu_alt = local_menu_scale.addMenu(alt_dict[scale_alt_str])

                for scale_note in ScaleManager.VALID_SCALES[scale_name][scale_alt_str]:
                    full_scale_str = '{}{} {}'.format(scale_note, scale_alt_str, scale_name)
                    _qaction = QAction(full_scale_str, local_menu_alt)
                    # print('adding action "{}"'.format(full_scale_str))
                    _qaction.triggered.connect(partial(self.set_training_scale,
                                                       scale_name,
                                                       scale_note,
                                                       scale_alt_str
                                                       ))
                    local_menu_alt.addAction(_qaction)

    def set_training_scale(self, scale_name, base_note_letter, base_note_alt_str):
        base_note_str = "{}{}{}".format(base_note_letter, base_note_alt_str, 4)
        self._ft.set_scale(scale_name, Note.from_str(base_note_str), mode=1)


class MainWindow(QMainWindow):
    def __init__(self, flute_teacher, width=800, height=600):
        super(MainWindow, self).__init__()
        self._ft = flute_teacher
        self._autonext = False
        self._listening = False

        # ==================================================================== #
        #                             USER INTERFACE                           #
        # ==================================================================== #

        # main window

        screen_size = qApp.desktop().availableGeometry().size()
        top_x = (screen_size.width() // 2) - (width // 2)
        top_y = (screen_size.height() // 2) - (height // 2)
        self.setGeometry(top_x, top_y, width, height)
        # self._window.setGeometry(10, 10, width, height)
        self.setWindowTitle("FluteTeacher")

        # ------------------------------ MENU BAR ------------------------------
        # # self.statusBar()
        # self._menu_bar = QMenuBar(self)
        # self._menu_bar.setGeometry(0, 0, width, 40)
        # self._file_menu = QMenu(self._menu_bar)
        # self._file_menu.setObjectName('menuFile')
        # # self._action_quit = QAction('&Quit', self)
        # # self._action_quit.setStatusTip('Bye..')
        # # self._action_quit.triggered.connect(self.quit)
        # # self._file_menu.addAction(self._action_quit)
        # self.setMenuBar(self._menu_bar)

        # test 2:
        # note: we need the space before "&Exit"
        # menubar = self.menuBar()
        self._menubar = MenuBar(self, flute_teacher)



        # --------------------------- CENTER WIDGET ----------------------------
        self._ww = QWidget()

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
        self._next_button.clicked.connect(self._ft.next_note)
        self._bottom_row_layout.addWidget(self._next_button)

        self._button_autonext = QPushButton('Enable AutoNext' if not self._autonext else 'Disable AutoNext')
        self._button_autonext.clicked.connect(self.toggle_autonext)
        self._bottom_row_layout.addWidget(self._button_autonext)

        self._button_listening = QPushButton('Start listening' if not self._listening else 'Stop listening')
        self._button_listening.clicked.connect(self.toggle_listening)
        self._bottom_row_layout.addWidget(self._button_listening)

        # main grid
        self._grid = QGridLayout()
        self._grid.addWidget(self._top_row)
        self._grid.addWidget(self.fingering)
        self._grid.addWidget(self._bottom_row)

        self._ww.setLayout(self._grid)

        self.setCentralWidget(self._ww)

        self.show()

    # noinspection PyMethodMayBeStatic
    def quit(self):
        print('bye bye')
        exit(0)

    def toggle_autonext(self):
        self._autonext = not self._autonext
        if self._autonext:
            self._button_autonext.setText('Disable AutoNext')
        else:
            self._button_autonext.setText('Enable AutoNext')
        self._ft.set_autonext(self._autonext)

    def toggle_listening(self):
        self._listening = not self._listening
        if self._listening:
            self._ft.start_listening()
            self._button_listening.setText('Stop listening')
        else:
            self._ft.stop_listening()
            self._button_listening.setText('Start listening')
            self._right_staff.erase_note()

    def display_note(self, staff, note, ndec=None):
        if staff == 'left':
            self._left_staff.display_note(note, ndec)
        elif staff == 'right':
            self._right_staff.display_note(note, ndec)
        else:
            print('ERROR: unknown staff "{}"'.format(staff))

    def set_fingering(self, note):
        self.fingering.set_fingering(note)

    def erase_note(self, staff):
        if staff == 'left':
            self._left_staff.erase_note()
        elif staff == 'right':
            self._right_staff.erase_note()
        else:
            print('ERROR: unknown staff "{}"'.format(staff))


class FluteTeacher:
    NOTE_MODE_RANDOM_1 = 1
    NOTE_MODE_RANDOM_2 = 2
    NOTE_MODE_SCALE = 0

    def __init__(self):
        self._current_note = None
        self._heard_note = None
        self._listening = False
        self._autonext = False
        self._scale_manager = ScaleManager(scale_name='Major',
                                           mode=1,
                                           base_note=Note('C', 4, Alterations.NATURAL),
                                           arp=ArpeggiatorV2.UP)

        self._note_mode = FluteTeacher.NOTE_MODE_SCALE

        self._main_window = MainWindow(flute_teacher=self)

        # ================================================= #
        #                NOTE RECOGNITION                   #
        # ================================================= #
        self._hear_ai = HearAI()

    def is_autonext(self):
        return self._autonext

    def is_listening(self):
        return self._listening

    def set_autonext(self, val):
        self._autonext = val

    def hearing_loop(self):
        while self._listening:
            dec = self.hear_sample()
            if self._autonext and (dec is not None) and (dec == 0):
                self.next_note(validate=True)

    def start_listening(self):
        print('FT: start listening')
        self._listening = True
        thr = threading.Thread(target=self.hearing_loop)
        thr.start()

    def stop_listening(self):
        print('FT: stop listening')
        self._listening = False

    # def toggle_listening(self):
    #     self._listening = not self._listening
    #     if self._listening:
    #         print('listening start')
    #         thr = threading.Thread(target=self.hearing_loop)
    #         thr.start()
    #     else:
    #         print('stop listening')

    def blink_notes(self):
        btime = (BLINKING_TIME / (2 * BLINKING_LOOPS))
        for blink_loop in range(BLINKING_LOOPS):
            # self._left_staff.display_note(self._current_note, ndec=0)
            # self._right_staff.display_note(self._current_note, ndec=0)
            self._main_window.display_note(staff='left', note=self._current_note, ndec=0)
            self._main_window.display_note(staff='right', note=self._current_note, ndec=0)
            sleep(btime)
            # self._left_staff.erase_note()
            # self._right_staff.erase_note()
            self._main_window.erase_note(staff='left')
            self._main_window.erase_note(staff='right')
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

        # self._left_staff.display_note(self._current_note)
        self._main_window.display_note(staff='left', note=self._current_note)
        # self.fingering.set_fingering(self._current_note)
        self._main_window.set_fingering(self._current_note)

    def hear_sample(self):
        self._hear_ai.record(millis=200)
        heard_note = self._hear_ai.get_last_note(alteration=self._current_note.alteration)

        if heard_note is not None:
            self._heard_note = heard_note
            dec = heard_note.midi_code - self._current_note.midi_code
            # self._right_staff.display_note(heard_note, ndec=dec)
            print('display note: {}'.format(heard_note))
            self._main_window.display_note(staff='right', note=heard_note, ndec=dec)
            return dec

        # self._right_staff.erase_note()
        self._main_window.erase_note(staff='right')
        return None

    def set_scale(self, scale_name, base_note, mode):
        self._scale_manager.set_scale(scale_name, base_note, mode)
        self._scale_manager.init_arp()
        self.next_note()
