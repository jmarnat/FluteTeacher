from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import threading
import time
from numpy import arange

HANDS_COLORS_1 = {'left': 'blue', 'right': 'red'}
HANDS_COLORS_2 = {'left': 'blue', 'right': 'blue'}
HANDS_COLORS_3 = {'left': 'black', 'right': 'black'}


class Fingering(QWidget):
    DISPLAY_ALWAYS = 1
    DISPLAY_DELAY = 2
    DISPLAY_NEVER = 3

    def __init__(self, display_mode=DISPLAY_ALWAYS, display_delay=3):
        super(Fingering, self).__init__()

        self.keys = []

        self.midi_fingerings = {
            60: {'left': [2, 3, 4, 5],     'right': [1, 3, 5, 7, 8]},  # C  4
            61: {'left': [2, 3, 4, 5],     'right': [1, 3, 5, 7]},     # C# 4
            62: {'left': [2, 3, 4, 5],     'right': [1, 3, 5]},        # D  4
            63: {'left': [2, 3, 4, 5],     'right': [1, 3, 5, 6]},     # D# 4
            64: {'left': [2, 3, 4, 5],     'right': [1, 3, 6]},        # E  4
            65: {'left': [2, 3, 4, 5],     'right': [1, 6]},           # F  4
            66: {'left': [2, 3, 4, 5],     'right': [5, 6]},           # F# 4
            67: {'left': [2, 3, 4, 5],     'right': [6]},              # G  4
            68: {'left': [2, 3, 4, 5, 6],  'right': [6]},              # G# 4
            69: {'left': [2, 3, 4],        'right': [6]},              # A  4
            70: {'left': [2, 3],           'right': [1, 6]},           # A# 4
            71: {'left': [2, 3],           'right': [6]},              # B  4

            72: {'left': [3],              'right': [6]},              # C  5
            73: {'left': [],               'right': [6]},              # C# 5
            74: {'left': [2, 4, 5],        'right': [1, 3, 5]},        # D  5
            75: {'left': [2, 4, 5],        'right': [1, 3, 5, 6]},     # D# 5
            76: {'left': [2, 4, 5],        'right': [1, 3, 6]},        # E  5
            77: {'left': [2, 3, 4, 5],     'right': [1, 6]},           # F  5
            78: {'left': [2, 3, 4, 5],     'right': [5, 6]},           # F# 5
            79: {'left': [2, 3, 4, 5],     'right': [6]},              # G  5
            80: {'left': [2, 3, 4, 5, 6],  'right': [6]},              # G# 5
            81: {'left': [2, 3, 4],        'right': [6]},              # A  5
            82: {'left': [2, 3],           'right': [1, 6]},           # A# 5
            83: {'left': [2, 3],           'right': [6]},              # B  5

            84: {'left': [3],              'right': [6]},              # C  6
            85: {'left': [],               'right': [6]},              # C# 6
        }

        self.hands_colors = HANDS_COLORS_3
        self._display_mode = display_mode
        self._display_delay = display_delay
        self._current_note = None

        # for _fingering_delay
        self._tictoc = 0
        self._next_keys = None
        self._nb_waiting = 0

    def set_display_mode(self, display_mode, display_delay=None):
        self._display_mode = display_mode
        if display_delay is not None:
            self._display_delay = display_delay
            self._tictoc = 0
            self._next_keys = None
            self._nb_waiting = 0
        self._update_fingering()

    def _fingering_delay(self):
        self.keys = None
        self.update()
        self._next_keys = self._compute_fingering()
        self._nb_waiting += 1
        sleep_time = 0.01
        while self._tictoc > 0:
            time.sleep(sleep_time)
            if self._tictoc == 0:
                self._nb_waiting -= 1
                return
            self._tictoc -= sleep_time
        self.keys = self._next_keys
        self.update()
        self._nb_waiting -= 1
        return

    def _compute_fingering(self):
        try:
            return self.midi_fingerings[self._current_note.midi_code]
        except KeyError:
            print('warning, no fingering for note no {}'.format(self._current_note.midi_code))
            return None

    def _update_fingering(self):
        self.set_fingering(self._current_note)

    def set_fingering(self, note):
        self._tictoc = 0
        while self._nb_waiting > 0:
            print('nb_wainting: {}'.format(self._nb_waiting))
            time.sleep(0.01)

        self._current_note = note

        if self._display_mode == Fingering.DISPLAY_ALWAYS:
            self.keys = self._compute_fingering()
            self.update()
        elif self._display_mode == Fingering.DISPLAY_NEVER:
            if self.keys is not None:
                self.keys = None
                self.update()
        elif self._display_mode == Fingering.DISPLAY_DELAY:
            self._tictoc = self._display_delay
            thr = threading.Thread(target=self._fingering_delay)
            thr.start()

    def _get_color(self, n, hand):
        if self.keys is not None:
            if hand in ['left', 'right']:
                return QColor(['white', self.hands_colors[hand]][n in self.keys[hand]])
        return QColor('gray')

    def paintEvent(self, event):
        self.draw_fingering()

    def draw_fingering(self):
        qp = QPainter()
        qp.begin(self)
        w = self.width()
        h = self.height()
        r = w / 40
        qp.setPen(QColor(Qt.black))

        qp.setBrush(self._get_color(1, 'left'))
        qp.drawRect(
            int(0.1 * w - r),
            int(h / 2 + 2 * r),
            int(2 * r),
            int(r)
        )

        qp.setBrush(self._get_color(2, 'left'))
        qp.drawRect(
            int(0.1 * w + r),
            int(h / 2 + 2 * r),
            int(2 * r),
            int(r)
        )

        qp.setBrush(self._get_color(3, 'left'))
        qp.drawEllipse(QPoint(int(0.15 * w), int(h / 2)), r, r)

        qp.setBrush(self._get_color(4, 'left'))
        qp.drawEllipse(QPoint(int(0.25 * w), int(h / 2)), r, r)

        qp.setBrush(self._get_color(5, 'left'))
        qp.drawEllipse(QPoint(int(0.35 * w), int(h / 2)), r, r)

        qp.setBrush(self._get_color(6, 'left'))
        qp.drawRect(
            int(0.35 * w - r),
            int(h / 2 - 3 * r),
            int(2 * r),
            int(r)
        )

        qp.drawLine(
            int(0.45 * w),
            int(0.25 * h - r),
            int(0.45 * w),
            int(0.75 * h + r),
        )

        qp.setBrush(self._get_color(1, 'right'))
        qp.drawEllipse(QPoint(int(0.55 * w), int(h / 2)), r, r)

        qp.setBrush(self._get_color(2, 'right'))
        qp.drawRect(
            int(0.6 * w - r/2),
            int(h / 2 + r),
            int(r),
            int(2*r)
        )

        qp.setBrush(self._get_color(3, 'right'))
        qp.drawEllipse(QPoint(int(0.65 * w), int(h / 2)), r, r)

        qp.setBrush(self._get_color(4, 'right'))
        qp.drawRect(
            int(0.7 * w - r / 2),
            int(h / 2 + r),
            int(r),
            int(2 * r)
        )

        qp.setBrush(self._get_color(5, 'right'))
        qp.drawEllipse(QPoint(int(0.75 * w), int(h / 2)), r, r)

        qp.setBrush(self._get_color(6, 'right'))
        qp.drawRect(
            int(0.85 * w - r),
            int(h / 2 - r),
            int(2 * r),
            int(2 * r)
        )

        qp.setBrush(self._get_color(7, 'right'))
        qp.drawRect(
            int(0.85 * w + r),
            int(h / 2 - r),
            int(2 * r),
            int(r)
        )

        qp.setBrush(self._get_color(8, 'right'))
        qp.drawRect(
            int(0.85 * w + r),
            int(h / 2),
            int(2 * r),
            int(r)
        )

        qp.end()
