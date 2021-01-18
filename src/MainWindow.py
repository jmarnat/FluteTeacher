from PyQt5.QtWidgets import *
from functools import partial
from PyQt5.QtCore import Qt

from src.Staff import Staff
from src.Note import Note
from src.Fingering import Fingering
from src.ScaleManager import ScaleManager
from src.Arpeggiator import Arpeggiator
from src.Alteration import Alterations


class MenuBar(QMenuBar):
    def __init__(self, parent, flute_teacher):
        super(MenuBar, self).__init__(parent)
        self._ft = flute_teacher

        # --------------------------------------------- SCALES AND MODES --------------------------------------------- #
        self._menu_scales = self.addMenu('Scales and Modes')
        self._menu_scales_qactions = {}

        for scale_name, modes in ScaleManager.VALID_MODES.items():
            if modes is not None:
                menu_modes = self._menu_scales.addMenu(scale_name)
                for mode_deg, mode_name in modes.items():
                    # mode_fullname = "{} - {}".format(mode_deg, mode_name)
                    _qaction = QAction(mode_name)
                    _qaction.triggered.connect(partial(self.set_training_scale, scale_name, mode_deg))
                    _qaction.setCheckable(True)
                    if (scale_name, mode_deg) == ('Major', 1):
                        _qaction.setChecked(True)
                    menu_modes.addAction(_qaction)
                    self._menu_scales_qactions[(scale_name, mode_deg)] = _qaction
            else:
                _qaction = QAction(scale_name)
                _qaction.triggered.connect(partial(self.set_training_scale, scale_name, None))
                _qaction.setCheckable(True)
                self._menu_scales.addAction(_qaction)
                self._menu_scales_qactions[(scale_name, None)] = _qaction

        # ----------------------------------------- STARTING OCTAVE AND NOTE ----------------------------------------- #
        self._menu_start_from = self.addMenu('Start from')

        self._menu_start_from_basenote = self._menu_start_from.addMenu('Base note')
        self._menu_start_from_basenote_qactions = {}
        for _alt in [Alterations.NATURAL, Alterations.FLAT, Alterations.SHARP]:
            for _letter in "CDEFGAB":
                _note_str = "{}{}".format(_letter, str(_alt))
                if _note_str in ['Cb', 'Fb', 'B#', 'E#']:
                    continue
                _qaction = QAction(_note_str)
                _qaction.triggered.connect(partial(self.set_training_base_note, _letter, _alt))
                _qaction.setCheckable(True)
                if _note_str == 'C':
                    _qaction.setChecked(True)
                self._menu_start_from_basenote.addAction(_qaction)
                self._menu_start_from_basenote_qactions[(_letter, _alt)] = _qaction
            if str(_alt) in ('', 'b'):
                self._menu_start_from_basenote.addSeparator()

        self._menu_start_from_oct = self._menu_start_from.addMenu('Octave')
        self._menu_start_from_oct_qactions = {}
        for _oct_val, _oct_str in {4: '4 (Middle C)', 5: '5', 6: '6'}.items():
            _qaction = QAction(_oct_str)
            _qaction.triggered.connect(partial(self.set_training_octave, _oct_val))
            _qaction.setCheckable(True)
            if _oct_val == 4:
                _qaction.setChecked(True)
            self._menu_start_from_oct.addAction(_qaction)
            self._menu_start_from_oct_qactions[_oct_val] = _qaction

        # ----------------------------------------------- ARPEGGIATORS ----------------------------------------------- #
        self._menu_arps = self.addMenu('Arpeggiators')
        self._menu_arps_actions = {}
        _arp_dict = Arpeggiator.arp_dict()
        for _noct, _noct_str in Arpeggiator.noct_dict().items():
            for _arp_kind, _arp_kind_str in _arp_dict.items():
                _arp_full_str = "{} - {}".format(_noct_str, _arp_kind_str)
                _qaction = QAction(_arp_full_str, self._menu_arps)
                _qaction.setCheckable(True)
                if _arp_full_str == "1 Octave - Up":
                    _qaction.setChecked(True)
                _qaction.triggered.connect(partial(self.set_arpeggiator, _arp_kind, _noct))
                self._menu_arps_actions[(_arp_kind, _noct)] = _qaction
                self._menu_arps.addAction(_qaction)
            if _noct_str in list(Arpeggiator.noct_dict().values())[:-1]:
                self._menu_arps.addSeparator()

        # ------------------------------------------------ FINGERINGS ------------------------------------------------ #

        self._menu_fingerings = self.addMenu('Fingerings')
        self._menu_fingerings_actions = {}

        _qaction_fgr_always = QAction('Always visible', self._menu_fingerings)
        _qaction_fgr_always.triggered.connect(partial(self.set_fingering_display_mode, Fingering.DISPLAY_ALWAYS, None))
        _qaction_fgr_always.setCheckable(True)
        _qaction_fgr_always.setChecked(True)
        self._menu_fingerings.addAction(_qaction_fgr_always)
        self._menu_fingerings_actions[(Fingering.DISPLAY_ALWAYS, None)] = _qaction_fgr_always

        _qaction_fgr_never = QAction('Always hidden', self._menu_fingerings)
        _qaction_fgr_never.triggered.connect(partial(self.set_fingering_display_mode, Fingering.DISPLAY_NEVER, None))
        _qaction_fgr_never.setCheckable(True)
        self._menu_fingerings.addAction(_qaction_fgr_never)
        self._menu_fingerings_actions[(Fingering.DISPLAY_NEVER, None)] = _qaction_fgr_never

        self._menu_fingerings.addSeparator()
        for d in (1, 2, 3, 4, 5):
            _qaction_fgr_delay = QAction('Display after {}s'.format(d), self._menu_fingerings)
            _qaction_fgr_delay.triggered.connect(partial(self.set_fingering_display_mode, Fingering.DISPLAY_DELAY, d))
            _qaction_fgr_delay.setCheckable(True)
            self._menu_fingerings.addAction(_qaction_fgr_delay)
            self._menu_fingerings_actions[(Fingering.DISPLAY_DELAY, d)] = _qaction_fgr_delay

    def set_training_scale(self, scale_name, mode):
        self._ft.set_scale(scale_name, mode)
        for (_scale_name, _scale_deg), _qaction in self._menu_scales_qactions.items():
            if (_scale_name, _scale_deg) == (scale_name, mode):
                _qaction.setChecked(True)
            else:
                _qaction.setChecked(False)

    def set_training_base_note(self, note_letter, alteration):
        self._ft.set_base_note(note_letter, alteration)
        # _menu_start_from_basenote_qactions[(_alt, _letter)]
        for (_letter, _alt), _qaction in self._menu_start_from_basenote_qactions.items():
            if (_letter, _alt) == (note_letter, alteration):
                _qaction.setChecked(True)
            else:
                _qaction.setChecked(False)

    def set_training_octave(self, octave):
        self._ft.set_start_octave(octave)
        for _oct, _qaction in self._menu_start_from_oct_qactions.items():
            if _oct == octave:
                _qaction.setChecked(True)
            else:
                _qaction.setChecked(False)

    def set_arpeggiator(self, kind, n_octaves):
        self._ft.set_arpeggiator(kind, n_octaves)
        for (_arp_kind, _noct), _qaction in self._menu_arps_actions.items():
            if (_arp_kind, _noct) == (kind, n_octaves):
                _qaction.setChecked(True)
            else:
                _qaction.setChecked(False)

    def set_fingering_display_mode(self, mode, delay):
        self._ft.set_fingering_display_mode(mode, delay)
        for (_mode, _delay), _qaction in self._menu_fingerings_actions.items():
            if (_mode, _delay) == (mode, delay):
                _qaction.setChecked(True)
            else:
                _qaction.setChecked(False)


class MainWindow(QMainWindow):
    def __init__(self, flute_teacher, width=800, height=600):
        super(MainWindow, self).__init__()
        self._ft = flute_teacher
        # self._autonext = False
        # self._listening = False

        # ------------------------- MAIN WINDOW (self) ----------------------- #

        screen_size = qApp.desktop().availableGeometry().size()
        top_x = (screen_size.width() // 2) - (width // 2)
        top_y = (screen_size.height() // 2) - (height // 2)
        self.setGeometry(top_x, top_y, width, height)
        # self._window.setGeometry(10, 10, width, height)
        self.setWindowTitle("FluteTeacher")

        # ------------------------------ MENU BAR ---------------------------- #
        self._menubar = MenuBar(self, flute_teacher)

        # --------------------------- CENTER WIDGET -------------------------- #
        self._ww = QWidget()
        self._ww_layout = QGridLayout()
        self._ww.setLayout(self._ww_layout)
        self._ww.setMinimumWidth(500)

        # FIRST ROW
        self._top_row = QGroupBox()
        self._top_row_layout = QHBoxLayout()
        self._top_row.setLayout(self._top_row_layout)

        self._left_staff = Staff(kind='normal')
        self._top_row_layout.addWidget(self._left_staff)

        self._right_staff = Staff(kind='normal')
        self._top_row_layout.addWidget(self._right_staff)

        # SECOND ROW
        self.fingering = Fingering()

        # BOTTOM ROW
        self._bottom_row = QGroupBox()
        self._bottom_row_layout = QHBoxLayout(self._bottom_row)
        self._bottom_row.setLayout(self._bottom_row_layout)

        self._next_button = QPushButton('Next note')
        self._next_button.clicked.connect(self._ft.next_note)
        self._next_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._bottom_row_layout.addWidget(self._next_button)

        self._button_autonext = QPushButton('Enable AutoNext' if not self._ft.is_autonext() else 'Disable AutoNext')
        self._button_autonext.clicked.connect(self.toggle_autonext)
        self._button_autonext.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._bottom_row_layout.addWidget(self._button_autonext)

        self._button_listening = QPushButton('Start listening' if not self._ft.is_listening() else 'Stop listening')
        self._button_listening.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._button_listening.clicked.connect(self.toggle_listening)

        self._bottom_row_layout.addWidget(self._button_listening)

        # main grid
        self._top_row.setMinimumHeight(200)
        self.fingering.setMinimumHeight(200)
        self._bottom_row.setFixedHeight(80)

        self._ww_layout.addWidget(self._top_row)
        self._ww_layout.addWidget(self.fingering)
        self._ww_layout.addWidget(self._bottom_row)

        self.setCentralWidget(self._ww)

        self.show()

    # def quit(self):
    #     print('bye bye')
    #     exit(0)

    def toggle_autonext(self):
        # self._autonext = not self._autonext
        if self._ft.is_autonext():
            self._button_autonext.setText('Enable AutoNext')
            self._ft.set_autonext(False)
        else:
            self._button_autonext.setText('Disable AutoNext')
            self._ft.set_autonext(True)

    def toggle_listening(self):
        if self._ft.is_listening():
            self._ft.stop_listening()
            self._button_listening.setText('Start listening')
            self._right_staff.erase_note()
        else:
            self._ft.start_listening()
            self._button_listening.setText('Stop listening')

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
