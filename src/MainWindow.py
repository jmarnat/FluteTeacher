from PyQt5.QtWidgets import *
from functools import partial
from PyQt5.QtCore import Qt

from src.Staff import Staff
from src.Note import Note
from src.Fingering import Fingering
from src.ScaleManager import ScaleManager
from src.Arpeggiator import Arpeggiator


class MenuBar(QMenuBar):
    def __init__(self, parent, flute_teacher):
        super(MenuBar, self).__init__(parent)
        self._ft = flute_teacher

        self._menu_scales = self.addMenu('Scales')
        for scale_name in ScaleManager.VALID_SCALES.keys():
            local_menu_scale = self._menu_scales.addMenu("{} scales".format(scale_name))
            _alts = list(ScaleManager.VALID_SCALES[scale_name].keys())
            for _alt_str in _alts:
                for scale_note in ScaleManager.VALID_SCALES[scale_name][_alt_str]:
                    full_scale_str = '{}{} {}'.format(scale_note, _alt_str, scale_name)
                    _qaction = QAction(full_scale_str, local_menu_scale)
                    _qaction.triggered.connect(partial(self.set_training_scale,
                                                       scale_name,
                                                       scale_note,
                                                       _alt_str
                                                       ))
                    local_menu_scale.addAction(_qaction)
                if _alt_str in _alts[:-1]:
                    local_menu_scale.addSeparator()

        self._menu_scales.addSeparator()
        self._menu_octave = self._menu_scales.addMenu('Start from octave..')
        for octave, octave_name in {4: '4 (Middle C)', 5: '5', 6: '6'}.items():
            _qaction = QAction(octave_name, self._menu_octave)
            _qaction.triggered.connect(partial(self.set_training_octave, octave))
            self._menu_octave.addAction(_qaction)

        self._menu_arps = self.addMenu('Apreggiators')
        _arp_dict = Arpeggiator.arp_dict()
        for _arp_kind, _arp_kind_str in _arp_dict.items():
            for _noct, _noct_str in Arpeggiator.noct_dict().items():
                _arp_full_str = "{} - {}".format(_arp_kind_str, _noct_str)
                _qaction = QAction(_arp_full_str, self._menu_arps)
                _qaction.triggered.connect(partial(self.set_arpeggiator, _arp_kind, _noct))
                self._menu_arps.addAction(_qaction)
            if _arp_kind_str in list(_arp_dict.values())[:-1]:
                self._menu_arps.addSeparator()

    def set_training_scale(self, scale_name, base_note_letter, base_note_alt_str):
        base_note_str = "{}{}{}".format(base_note_letter, base_note_alt_str, 4)
        _new_scale_mgr = ScaleManager(scale_name, Note.from_str(base_note_str), mode=1)
        self._ft.set_scale_manager(_new_scale_mgr)

    def set_training_octave(self, octave):
        self._ft.set_start_octave(octave)

    # noinspection PyMethodMayBeStatic
    def set_arpeggiator(self, kind, n_octaves):
        self._ft.set_arpeggiator(kind, n_octaves)


class MainWindow(QMainWindow):
    def __init__(self, flute_teacher, width=800, height=600):
        super(MainWindow, self).__init__()
        self._ft = flute_teacher
        self._autonext = False
        self._listening = False

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

        self._button_autonext = QPushButton('Enable AutoNext' if not self._autonext else 'Disable AutoNext')
        self._button_autonext.clicked.connect(self.toggle_autonext)
        self._button_autonext.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._bottom_row_layout.addWidget(self._button_autonext)

        self._button_listening = QPushButton('Start listening' if not self._listening else 'Stop listening')
        self._button_listening.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._button_listening.clicked.connect(self.toggle_listening)

        self._bottom_row_layout.addWidget(self._button_listening)

        # main grid
        self._top_row.setMinimumHeight(200)
        self.fingering.setMinimumHeight(200)
        self._bottom_row.setFixedHeight(60)

        self._ww_layout.addWidget(self._top_row)
        self._ww_layout.addWidget(self.fingering)
        self._ww_layout.addWidget(self._bottom_row)

        self.setCentralWidget(self._ww)

        self.show()

    # def quit(self):
    #     print('bye bye')
    #     exit(0)

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
