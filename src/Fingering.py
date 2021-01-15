from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

HANDS_COLORS_1 = {'left': 'blue', 'right': 'red'}
HANDS_COLORS_2 = {'left': 'blue', 'right': 'blue'}
HANDS_COLORS_3 = {'left': 'black', 'right': 'black'}


class Fingering(QWidget):
    def __init__(self):
        super(Fingering, self).__init__()
        self.keys = []
        self.midi_fingerings = {
            60: {'left': [2, 3, 4, 5], 'right': [1, 3, 5, 7]},  # C  4
            61: {'left': [2, 3, 4, 5], 'right': [1, 3, 5, 6]},  # Db 4
            62: {'left': [2, 3, 4, 5], 'right': [1, 3, 5]},  # D  4
            63: {'left': [2, 3, 4, 5], 'right': [1, 3, 5, 6]},  # Eb 4
            64: {'left': [2, 3, 4, 5], 'right': [1, 3, 6]},  # E  4
            65: {'left': [2, 3, 4, 5], 'right': [1, 6]},  # F  4
            66: {'left': [2, 3, 4, 5], 'right': [5, 6]},  # Gb  4
            67: {'left': [2, 3, 4, 5], 'right': [6]},  # G  4
            68: {'left': [2, 3, 4, 5, 6], 'right': [6]},  # Ab 4
            69: {'left': [2, 3, 4], 'right': [6]},  # A  4
            70: {'left': [2, 3], 'right': [1, 6]},  # Bb 4
            71: {'left': [2, 3], 'right': [6]},  # B  4
            72: {'left': [3], 'right': [6]},  # C  5
            73: {'left': [], 'right': [6]},  # Db 5
        }

        self.hands_colors = HANDS_COLORS_3

    def set_fingering(self, note):
        try:
            self.keys = self.midi_fingerings[note.midi_code]
        except KeyError:
            print('warning, no fingering for note no {}'.format(note.midi_code))
            self.keys = [{'left': [], 'right': []}]
        self.update()

    def _get_color(self, n, hand):
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
