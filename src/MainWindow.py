from PyQt5.QtWidgets import *
from functools import partial

from src.Staff import Staff
from src.Note import Note
from src.Fingering import Fingering
from src.ScaleManager import ScaleManager


class MenuBar(QMenuBar):
    def __init__(self, parent, flute_teacher):
        super(MenuBar, self).__init__(parent)
        self._ft = flute_teacher

        # self._exit_action = QAction(' &Quit FluteTeacher', self)
        # self._exit_action.setShortcut('Ctrl+Q')
        # self._exit_action.triggered.connect(qApp.quit)
        # self._menu_file = self.addMenu('&File')
        # self._menu_file.addAction(self._exit_action)

        self._menu_training = self.addMenu('Training')
        self._menu_scales = self._menu_training.addMenu('Scales')

        for scale_name in ScaleManager.VALID_SCALES.keys():
            local_menu_scale = self._menu_scales.addMenu(scale_name)

            for scale_alt_str in ScaleManager.VALID_SCALES[scale_name].keys():
                alt_dict = {'': 'Naturals', '#': 'Sharps', 'b': 'Flats'}
                local_menu_alt = local_menu_scale.addMenu(alt_dict[scale_alt_str])

                for scale_note in ScaleManager.VALID_SCALES[scale_name][scale_alt_str]:
                    full_scale_str = '{}{} {}'.format(scale_note, scale_alt_str, scale_name)
                    _qaction = QAction(full_scale_str, local_menu_alt)
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
