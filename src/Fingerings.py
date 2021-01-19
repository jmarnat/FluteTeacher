import threading
import time
from random import randint

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.Settings import Settings


# ------------------------------- STYLE SHEET -------------------------------- #
class StyleSheet:
    KEY_BORDER_COLOR = '#000000'
    KEY_BORDER_WEIGHT = 2

    # KEY_COLOR_CLOSED = '#6e93d6'
    # KEY_COLOR_OPEN = '#ffffff'
    # KEY_COLOR_DELAY = '#c0c0c0'

    COLOR_RELEASED_KEYS = '#ffffff'
    COLOR_OPTIONNAL_KEYS = '#888888'

    COLORS_PRESSED_KEYS = {
        'Black': '#000000',
        'Blue':  '#64b5f6',     # dark: 6e93d6, light: 64b5f6
    }

    COLORS_DELAY_KEYS = {
        'Gray': '#c0c0c0',
        'Rainbow': 'RAINBOW'
    }


# -------------------------------- FINGERINGS -------------------------------- #
FINGERINGS = {
    60: [((0, 1, 1, 1, 1, 0), (1, 0, 1, 0, 1, 0, 1, 2))],  # C  4
    61: [((0, 1, 1, 1, 1, 0), (1, 0, 1, 0, 1, 0, 0, 1))],  # C# 4

    62: [((0, 1, 1, 1, 1, 0), (1, 0, 1, 0, 1, 0, 0, 0))],  # D  4
    63: [((0, 1, 1, 1, 1, 0), (1, 0, 1, 0, 1, 1, 0, 0))],  # D# 4
    64: [((0, 1, 1, 1, 1, 0), (1, 0, 1, 0, 0, 1, 0, 0))],  # E  4
    65: [((0, 1, 1, 1, 1, 0), (1, 0, 0, 0, 0, 1, 0, 0))],  # F  4
    66: [((0, 1, 1, 1, 1, 0), (0, 0, 0, 0, 1, 1, 0, 0)),
         ((0, 1, 1, 1, 1, 0), (0, 0, 1, 0, 0, 1, 0, 0))],  # F# 4
    67: [((0, 1, 1, 1, 1, 0), (0, 0, 0, 0, 0, 1, 0, 0))],  # G  4
    68: [((0, 1, 1, 1, 1, 1), (0, 0, 0, 0, 0, 1, 0, 0))],  # G# 4
    69: [((0, 1, 1, 1, 0, 0), (0, 0, 0, 0, 0, 1, 0, 0))],  # A  4
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
    86: [((0, 1, 0, 1, 1, 0), (0, 0, 0, 0, 0, 1, 0, 0))],  # D  6
    87: [((0, 1, 1, 1, 1, 1), (1, 0, 1, 0, 1, 1, 0, 0))],  # D# 6
    88: [((0, 1, 1, 1, 0, 0), (1, 0, 1, 0, 0, 1, 0, 0))],  # E  6
    89: [((0, 1, 1, 0, 1, 0), (1, 0, 0, 0, 0, 1, 0, 0))],  # F  6
    90: [((0, 1, 1, 0, 1, 0), (0, 0, 0, 0, 1, 1, 0, 0))],  # F# 6
    91: [((0, 0, 1, 1, 1, 0), (0, 0, 0, 0, 0, 1, 0, 0))],  # G  6
    92: [((0, 0, 0, 1, 1, 1), (0, 0, 0, 0, 0, 1, 0, 0))],  # G# 6
    93: [((0, 1, 0, 1, 0, 0), (1, 0, 0, 0, 0, 1, 0, 0))],  # A  6
    94: [((0, 1, 0, 0, 0, 0), (1, 1, 0, 0, 0, 0, 0, 0))],  # A# 6
    95: [((0, 1, 1, 0, 1, 0), (0, 0, 0, 1, 0, 0, 0, 0))],  # B  6

    96: [((0, 0, 1, 1, 1, 1), (1, 0, 0, 0, 0, 0, 0, 0))],  # C  7

}


class FingeringError(Exception):
    """
    Just for warning in MainWindow
    """
    pass


class Fingerings(QWidget):
    """
    Both model, view and controller for fingerings
    """
    DISPLAY_ALWAYS = 1
    DISPLAY_DELAY = 2
    DISPLAY_NEVER = 3

    def __init__(self,
                 display_mode=DISPLAY_ALWAYS,
                 display_delay=None):
        super(Fingerings, self).__init__(flags=Qt.Widget)

        self.fingerings = []

        self._display_mode = display_mode
        self._display_delay = display_delay
        self._current_note = None

        # default colors = first in dictionnaries
        self._color_key = StyleSheet.COLORS_PRESSED_KEYS[list(StyleSheet.COLORS_PRESSED_KEYS.keys())[0]]
        self._color_delay = StyleSheet.COLORS_DELAY_KEYS[list(StyleSheet.COLORS_DELAY_KEYS.keys())[0]]

        # for _fingering_delay
        self._tictoc = 0
        self._next_fingerings = []
        self._nb_waiting = 0

        self.setMinimumWidth(200)
        self.setMinimumHeight(200)

    @staticmethod
    def check_notes(notes_list):
        """
        checks if all the notes are playable, i.e. have registered fingerings
        :param notes_list: list of Class:Note
        :return: True if playable, False otherwise.
        """
        for note in notes_list:
            if note.midi_code not in FINGERINGS.keys():
                return False
        return True

    def set_display_mode(self, display_mode, display_delay=None):
        self._display_mode = display_mode
        if display_delay is not None:
            self._display_delay = display_delay
            self._tictoc = 0
            self._next_fingerings = []
            self._nb_waiting = 0
        self._update_fingering()

    def _fingering_delay(self):
        self._next_fingerings = self._get_fingerings()
        self.fingerings = [(-1, -1)] * len(self._next_fingerings)
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

    def _get_fingerings(self):
        try:
            found_fingers = FINGERINGS[self._current_note.midi_code]
            if type(found_fingers) == tuple:
                return [found_fingers]
            elif type(found_fingers) == list:
                return found_fingers
            else:
                print('ERROR: UNKNOWN TYPE(FOUND_FINGERS) = {}'.format(type(found_fingers)))
        except KeyError:
            # SHOULD NEVER HAPPEN CAUSE CHECKED BEFORE
            print('warning, no fingering for note no {}'.format(self._current_note))
            return [(None, None)]

    def _update_fingering(self):
        self.set_fingering(self._current_note)

    def set_fingering(self, note):
        self._tictoc = 0
        while self._nb_waiting > 0:
            time.sleep(0.01)

        self._current_note = note
        if self._display_mode == Fingerings.DISPLAY_ALWAYS:
            self.fingerings = self._get_fingerings()
            self.update()
        elif self._display_mode == Fingerings.DISPLAY_NEVER:
            if self.fingerings is not None:
                self.fingerings = None
                self.update()
        elif self._display_mode == Fingerings.DISPLAY_DELAY:
            if note.midi_code in FINGERINGS.keys():
                self._tictoc = self._display_delay
                thr = threading.Thread(target=self._fingering_delay)
                thr.start()
            else:
                self.fingerings = [(None, None)]
                self.update()

    def set_key_color(self, color):
        self._color_key = color
        self.update()

    def set_delay_color(self, color):
        self._color_delay = color
        self.update()

    def _get_key_color(self, side, key_index, n_fingering):
        """
        :param side: 0=left, 1=right
        :param key_index: 0=1->6, 1=0->7
        :param n_fingering: if multiple fingerings, its' number (0->2?)
        :return: the associated QColor
        """

        # key delayed -> set wo weird values
        if self.fingerings[0] == (-1, -1):
            if self._color_delay == 'RAINBOW':
                _rr = randint(150, 256)
                _gg = randint(150, 256)
                _bb = randint(150, 256)
                return QColor(_rr, _gg, _bb)
            else:
                return QColor(self._color_delay)

        # getting key value
        val = self.fingerings[n_fingering][side][key_index - 1]

        # key not pressed / pressed / optionnal
        if val == 0:
            return QColor(StyleSheet.COLOR_RELEASED_KEYS)
        if val == 1:
            return QColor(self._color_key)
        if val == 2:
            return QColor(StyleSheet.COLOR_OPTIONNAL_KEYS)

        # should never happen
        return QColor('red')

    def paintEvent(self, event):
        self.draw_fingerings()

    def draw_fingerings(self):
        if self._display_mode == Fingerings.DISPLAY_NEVER:
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
        dash_pen = QPen(QColor('#ababab'))
        dash_pen.setStyle(Qt.DashLine)
        dash_pen.setWidth(1)
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
        path.addRoundedRect(
            20, _flute_top,
            w-40, _flute_width,
            10, 10
        )
        qp.fillPath(path, gradient)

        dash_pen = QPen(QColor('gray'))
        dash_pen.setStyle(Qt.DashLine, )
        dash_pen.setWidth(2)
        qp.setPen(dash_pen)
        qp.drawLine(
            0.45 * w,
            cy - 3 * r,
            0.45 * w,
            cy + 3 * r
        )

    def _draw_fingering(self, qp, n_fingering=0, total=1):

        w = self.width()
        h = self.height() // total
        flute_h = self.height() / 2
        cy = int((n_fingering * h) + (h / 2))
        r = min(flute_h/10, w/30)

        border_pen = QPen(QColor(StyleSheet.KEY_BORDER_COLOR), StyleSheet.KEY_BORDER_WEIGHT)
        qp.setPen(border_pen)

        # ---------------------------- LEFT HAND ----------------------------- #
        qp.setBrush(self._get_key_color(0, 1, n_fingering))
        qp.drawRect(
            int(0.15 * w - 3 * r),
            int(cy + 2 * r),
            int(2 * r),
            int(r)
        )

        qp.setBrush(self._get_key_color(0, 2, n_fingering))
        qp.drawRect(
            int(0.15 * w - r),
            int(cy + 2 * r),
            int(2 * r),
            int(r)
        )

        qp.setBrush(self._get_key_color(0, 3, n_fingering))
        qp.drawEllipse(
            QPoint(int(0.15 * w), cy),
            r, r
        )

        qp.setBrush(self._get_key_color(0, 4, n_fingering))
        qp.drawEllipse(
            QPoint(int(0.25 * w), cy),
            r, r
        )

        qp.setBrush(self._get_key_color(0, 5, n_fingering))
        qp.drawEllipse(
            QPoint(int(0.35 * w), cy),
            r, r
        )

        qp.setBrush(self._get_key_color(0, 6, n_fingering))
        qp.drawRect(
            int(0.35 * w - r),
            int(cy - 3 * r),
            int(2 * r),
            int(r)
        )

        # ---------------------------- RIGHT HAND ---------------------------- #
        qp.setBrush(self._get_key_color(1, 1, n_fingering))
        qp.drawEllipse(
            QPoint(int(0.55 * w), cy),
            r, r
        )

        qp.setBrush(self._get_key_color(1, 2, n_fingering))
        qp.drawRect(
            int(0.6 * w - r / 2),
            int(cy + r),
            int(r),
            int(2 * r)
        )

        qp.setBrush(self._get_key_color(1, 3, n_fingering))
        qp.drawEllipse(
            QPoint(int(0.65 * w), cy),
            r, r
        )

        qp.setBrush(self._get_key_color(1, 4, n_fingering))
        qp.drawRect(
            int(0.7 * w - r / 2),
            int(cy + r),
            int(r),
            int(2 * r)
        )

        qp.setBrush(self._get_key_color(1, 5, n_fingering))
        qp.drawEllipse(
            QPoint(int(0.75 * w), cy),
            r, r
        )

        qp.setBrush(self._get_key_color(1, 6, n_fingering))
        qp.drawRect(
            int(0.85 * w - r),
            int(cy - r),
            int(2 * r),
            int(2 * r)
        )

        qp.setBrush(self._get_key_color(1, 7, n_fingering))
        qp.drawRect(
            int(0.85 * w + r),
            int(cy - r),
            int(2 * r),
            int(r)
        )

        qp.setBrush(self._get_key_color(1, 8, n_fingering))
        qp.drawRect(
            int(0.85 * w + r),
            int(cy),
            int(2 * r),
            int(r)
        )
