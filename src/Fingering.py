from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import threading
import time

HANDS_COLORS_1 = {'left': 'blue', 'right': 'red'}
HANDS_COLORS_2 = {'left': 'blue', 'right': 'blue'}
HANDS_COLORS_3 = {'left': 'black', 'right': 'black'}

FINGERINGS = {
    60: [((0, 1, 1, 1, 1, 0), (1, 0, 1, 0, 1, 0, 1, 2))],  # C  4
    61: [((0, 1, 1, 1, 1, 0), (1, 0, 1, 0, 1, 0, 1, 0))],  # C# 4
    62: [((0, 1, 1, 1, 1, 0), (1, 0, 1, 0, 1, 0, 0, 0))],  # D  4
    63: [((0, 1, 1, 1, 1, 0), (1, 0, 1, 0, 1, 1, 0, 0))],  # D# 4
    64: [((0, 1, 1, 1, 1, 0), (1, 0, 1, 0, 0, 1, 0, 0))],  # E  4
    65: [((0, 1, 1, 1, 1, 0), (1, 0, 0, 0, 0, 1, 0, 0))],  # F  4
    66: [((0, 1, 1, 1, 1, 0), (0, 0, 0, 0, 1, 1, 0, 0)),
         ((0, 1, 1, 1, 1, 0), (0, 0, 1, 0, 0, 1, 0, 0))],  # F# 4
    67: [((0, 1, 1, 1, 1, 0), (0, 0, 0, 0, 0, 1, 0, 0))],  # G  4
    68: [((0, 1, 1, 1, 1, 1), (0, 0, 0, 0, 0, 1, 0, 0))],  # G# 4
    69: [((0, 1, 1, 1, 0, 0), (0, 0, 0, 0, 0, 2, 0, 0))],  # A  4
    70: [((0, 1, 1, 0, 0, 0), (1, 0, 0, 0, 0, 1, 0, 0)),
         ((1, 0, 1, 0, 0, 0), (0, 0, 0, 0, 0, 1, 0, 0))],  # A# 4
    71: [((0, 1, 1, 0, 0, 0), (0, 0, 0, 0, 0, 1, 0, 0))],  # B  4

    72: [((0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 0, 1, 0, 0))],  # C  5
    73: [((0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 1, 0, 0))],  # C# 5
    74: [((0, 1, 0, 1, 1, 0), (1, 0, 1, 0, 1, 0, 0, 0))],  # D  5
    75: [((0, 1, 0, 1, 1, 0), (1, 0, 1, 0, 1, 1, 0, 0))],  # D# 5
    76: [((0, 1, 1, 1, 1, 0), (1, 0, 1, 0, 0, 1, 0, 0))],  # E  5
    77: [((0, 1, 1, 1, 1, 0), (1, 0, 0, 0, 0, 1, 0, 0))],  # F  5
    78: [((0, 1, 1, 1, 1, 0), (0, 0, 0, 0, 1, 1, 0, 0)),
         ((0, 1, 1, 1, 1, 0), (0, 0, 1, 0, 0, 1, 0, 0))],  # F# 5
    79: [((0, 1, 1, 1, 1, 0), (0, 0, 0, 0, 0, 1, 0, 0))],  # G  5
    80: [((0, 1, 1, 1, 1, 1), (0, 0, 0, 0, 0, 1, 0, 0))],  # G# 5
    81: [((0, 1, 1, 1, 0, 0), (0, 0, 0, 0, 0, 1, 0, 0))],  # A  5
    82: [((0, 1, 1, 0, 0, 0), (1, 0, 0, 0, 0, 1, 0, 0)),
         ((1, 0, 1, 0, 0, 0), (0, 0, 0, 0, 0, 1, 0, 0))],  # A# 5
    83: [((0, 1, 1, 0, 0, 0), (0, 0, 0, 0, 0, 1, 0, 0))],  # B  5

    84: [((0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 0, 1, 0, 0))],  # C  6
    85: [((0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 1, 0, 0))],  # C# 6
}


class Fingering(QWidget):
    DISPLAY_ALWAYS = 1
    DISPLAY_DELAY = 2
    DISPLAY_NEVER = 3

    def __init__(self, display_mode=DISPLAY_ALWAYS, display_delay=3):
        super(Fingering, self).__init__(flags=Qt.Widget)

        self.fingerings = []

        self.hands_colors = HANDS_COLORS_3
        self._display_mode = display_mode
        self._display_delay = display_delay
        self._current_note = None

        # for _fingering_delay
        self._tictoc = 0
        self._next_fingerings = []
        self._nb_waiting = 0

        self.setMinimumWidth(200)
        self.setMinimumHeight(200)

    def set_display_mode(self, display_mode, display_delay=None):
        self._display_mode = display_mode
        if display_delay is not None:
            self._display_delay = display_delay
            self._tictoc = 0
            self._next_fingerings = []
            self._nb_waiting = 0
        self._update_fingering()

    def _fingering_delay(self):
        self._next_fingerings = self._compute_fingering()
        self.fingerings = [(tuple([-1] * 6), tuple([-1] * 8))] * len(self._next_fingerings)
        self.update()
        self._nb_waiting += 1
        sleep_time = 0.01
        while self._tictoc > 0:
            time.sleep(sleep_time)
            if self._tictoc == 0:
                self._nb_waiting -= 1
                return
            self._tictoc -= sleep_time
        self.fingerings = self._next_fingerings
        self.update()
        self._nb_waiting -= 1
        return

    def _compute_fingering(self):
        try:
            found_fingers = FINGERINGS[self._current_note.midi_code]
            if type(found_fingers) == tuple:
                return [found_fingers]
            elif type(found_fingers) == list:
                return found_fingers
            else:
                print('ERROR: UNKNOWN TYPE(FOUND_FINGERS) = {}'.format(type(found_fingers)))
        except KeyError:
            print('warning, no fingering for note no {}'.format(self._current_note.midi_code))
            return [(None, None, None, None, None, None), (None, None, None, None, None, None, None, None)]

    def _update_fingering(self):
        self.set_fingering(self._current_note)

    def set_fingering(self, note):
        self._tictoc = 0
        while self._nb_waiting > 0:
            time.sleep(0.01)

        self._current_note = note
        if self._display_mode == Fingering.DISPLAY_ALWAYS:
            self.fingerings = self._compute_fingering()
            self.update()
        elif self._display_mode == Fingering.DISPLAY_NEVER:
            if self.fingerings is not None:
                self.fingerings = None
                self.update()
        elif self._display_mode == Fingering.DISPLAY_DELAY:
            self._tictoc = self._display_delay
            thr = threading.Thread(target=self._fingering_delay)
            thr.start()

    def _get_color(self, hand, key_index, n_fingering):
        side = {'left': 0, 'right': 1}[hand]

        if not any(self.fingerings[0]):
            return Qt.Dense5Pattern

        val = self.fingerings[n_fingering][side][key_index - 1]

        if val == -1:
            return Qt.Dense7Pattern
        if val == 0:
            return QColor('white')
        if val == 1:
            return QColor('black')
        if val == 2:
            return QColor('gray')

        # should never happen
        return QColor('red')

    def paintEvent(self, event):
        self.draw_fingerings()

    def draw_fingerings(self):
        if self._display_mode == Fingering.DISPLAY_NEVER:
            return

        qp = QPainter()
        qp.begin(self)

        if self.fingerings is not None:
            nb_fingerings = len(self.fingerings)
            if nb_fingerings > 0:
                for n_fingering in range(nb_fingerings):
                    self._draw_flute(qp, n_fingering, nb_fingerings)
                    self._draw_fingering(qp, n_fingering, nb_fingerings)
                    if n_fingering < (nb_fingerings - 1):
                        self._draw_separator(qp, n_fingering, nb_fingerings)
            else:
                print('drawing empty flute')
                self._draw_flute(qp, 0, 1)
        else:
            print('fingerings is None')

        qp.end()

    def _draw_separator(self, qp, n_fingering=0, total=1):
        w = self.width()
        y = int((n_fingering+1) * self.height() / total)
        dash_pen = QPen(QColor('gray'))
        dash_pen.setStyle(Qt.DashLine)
        qp.setPen(dash_pen)
        qp.drawLine(10, y, w-10, y)

    def _draw_flute(self, qp, n_fingering=0, total=1):
        w = self.width()
        h = self.height() // total
        flute_h = self.height() / 2
        cy = int((n_fingering * h) + (h / 2))
        r = min(flute_h/10, w/30)
        _flute_top = cy - 4 * r
        _flute_width = 8 * r
        _flute_bottom = _flute_top + _flute_width

        # TESTING FLUTE GRADIENT..
        _flute_top = cy - 4 * r
        _flute_width = 8 * r
        _flute_bottom = _flute_top + _flute_width

        path = QPainterPath()
        gradient = QLinearGradient(0, _flute_top, 0, _flute_bottom)
        gradient.setColorAt(0, QColor('#e0e0e0'))
        gradient.setColorAt(1, QColor('#c0c0c0'))
        path.addRoundedRect(20, _flute_top, w-40, _flute_width, 10, 10)
        qp.fillPath(path, gradient)

        path = QPainterPath()
        gradient = QLinearGradient(0.45*w, _flute_top, 0.45*w+5, _flute_top)
        gradient.setColorAt(1, QColor('#e0e0e0'))
        gradient.setColorAt(0, QColor('#c0c0c0'))
        path.addRect(0.45*w, _flute_top, 5, _flute_width)
        qp.fillPath(path, gradient)

        path = QPainterPath()
        gradient = QLinearGradient(0.45 * w, _flute_top, 0.45 * w - 5, _flute_top)
        gradient.setColorAt(1, QColor('#e0e0e0'))
        gradient.setColorAt(0, QColor('#c0c0c0'))
        path.addRect(0.45 * w, _flute_top, -5, _flute_width)
        qp.fillPath(path, gradient)

    def _draw_fingering(self, qp, n_fingering=0, total=1):
        qp.setPen(QColor('gray'))
        qp.setBrush(QColor('#e0e0e0'))

        w = self.width()
        h = self.height() // total
        flute_h = self.height() / 2
        cy = int((n_fingering * h) + (h / 2))
        r = min(flute_h/10, w/30)

        qp.setPen(QColor(Qt.black))

        qp.setBrush(self._get_color('left', 1, n_fingering))
        qp.drawRect(
            int(0.1 * w - r),
            int(cy + 2 * r),
            int(2 * r),
            int(r)
        )

        qp.setBrush(self._get_color('left', 2, n_fingering))
        qp.drawRect(
            int(0.1 * w + r),
            int(cy + 2 * r),
            int(2 * r),
            int(r)
        )

        qp.setBrush(self._get_color('left', 3, n_fingering))
        qp.drawEllipse(QPoint(int(0.15 * w), cy), r, r)

        qp.setBrush(self._get_color('left', 4, n_fingering))
        qp.drawEllipse(QPoint(int(0.25 * w), cy), r, r)

        qp.setBrush(self._get_color('left', 5, n_fingering))
        qp.drawEllipse(QPoint(int(0.35 * w), cy), r, r)

        qp.setBrush(self._get_color('left', 6, n_fingering))
        qp.drawRect(
            int(0.35 * w - r),
            int(cy - 3 * r),
            int(2 * r),
            int(r)
        )

        qp.setBrush(self._get_color('right', 1, n_fingering))
        qp.drawEllipse(QPoint(int(0.55 * w), cy), r, r)

        qp.setBrush(self._get_color('right', 2, n_fingering))
        qp.drawRect(
            int(0.6 * w - r / 2),
            int(cy + r),
            int(r),
            int(2 * r)
        )

        qp.setBrush(self._get_color('right', 3, n_fingering))
        qp.drawEllipse(QPoint(int(0.65 * w), cy), r, r)

        qp.setBrush(self._get_color('right', 4, n_fingering))
        qp.drawRect(
            int(0.7 * w - r / 2),
            int(cy + r),
            int(r),
            int(2 * r)
        )

        qp.setBrush(self._get_color('right', 5, n_fingering))
        qp.drawEllipse(QPoint(int(0.75 * w), cy), r, r)

        qp.setBrush(self._get_color('right', 6, n_fingering))
        qp.drawRect(
            int(0.85 * w - r),
            int(cy - r),
            int(2 * r),
            int(2 * r)
        )

        qp.setBrush(self._get_color('right', 7, n_fingering))
        qp.drawRect(
            int(0.85 * w + r),
            int(cy - r),
            int(2 * r),
            int(r)
        )

        qp.setBrush(self._get_color('right', 8, n_fingering))
        qp.drawRect(
            int(0.85 * w + r),
            int(cy),
            int(2 * r),
            int(r)
        )
