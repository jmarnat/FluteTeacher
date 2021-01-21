from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from fractions import Fraction

from src.NotesAndRests import Note, Rest

COLOR_LOW = '#ff8b00'
COLOR_HIGH = '#ff1e00'
COLOR_OK = '#00b454'
COLOR_NORMAL = 'black'

# = percentage of the whole height
INTER_LINE_HEIGHT = 0.06


class Staff(QWidget):
    def __init__(self, kind='SingleNote'):
        """
        :param kind: either "SingleNote" / "SheetMusic"
        """
        super(Staff, self).__init__(flags=Qt.Widget)
        self.notes_and_rests = []
        self.ndec = None
        self.kind = kind

        self._time_signature = (None, None)
        # self._current_bar = 0
        self._current_pos = Fraction(0, 1)

        self.qimages = {
            'sharp': QImage('res/sharp.png'),
            'flat': QImage('res/flat.png'),
            'g-clef': QImage('res/g-clef.png'),
            'double-sharp': QImage('res/double-sharp.png'),
            'double-flat': QImage('res/double-flat.png'),
        }

    def il(self):
        """inter-line height"""
        return self.height() * INTER_LINE_HEIGHT

    def display_bar(self, bar):
        self._time_signature = bar.get_time_signature()
        self.notes_and_rests = bar.get_notes_and_rests()
        self._current_pos = 0
        self.update()

    def set_bar_pos(self, pos_frac):
        self._current_pos = pos_frac
        self.update()

    def display_note(self, note, ndec=None, update=True):
        self.notes_and_rests = [note]
        self.ndec = ndec
        if update:
            self.update()

    def erase_note(self, update=True):
        self.notes_and_rests = []
        self.ndec = None
        if update:
            self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self._paint_staff_and_clef(qp)
        self._paint_notes(qp)
        qp.end()

    def _paint_staff_and_clef(self, qp):
        _vcenter = int(0.6 * self.height())

        qp.setPen(QColor('gray'))
        qp.setBrush(QColor('white'))
        qp.drawRoundedRect(0, 0, self.width(), self.height(), 5, 5)

        # STAFF LINES
        qp.setPen(QColor(Qt.black))
        for i in [-2, -1, 0, 1, 2]:
            ypos = int(_vcenter - (i * self.il()))
            qp.drawLine(10, ypos, self.width()-10, ypos)

        # CLEF
        clef_h = int(self.il() * 8)
        clef_w = int(clef_h * (self.qimages['g-clef'].width() / self.qimages['g-clef'].height()))
        clef_xpos = 10
        clef_ypos = int(_vcenter - (clef_h / 2))
        qp.drawImage(QRect(clef_xpos, clef_ypos, clef_w, clef_h), self.qimages['g-clef'])

    def _get_xlims(self):
        clef_h = int(self.il() * 8)
        clef_w = int(clef_h * (self.qimages['g-clef'].width() / self.qimages['g-clef'].height()))
        _xmin = int(clef_w + 10 + 10)
        _xmax = int(self.width() - 20)
        return _xmin, _xmax

    def _paint_notes(self, qp):
        # 'SingleNote' display mode
        if self._time_signature == (None, None):
            if len(self.notes_and_rests) != 1:
                print('ERROR: Staff._paint_notes() | len(notes and rests) != 1')
                return
            self._paint_note(qp, note=self.notes_and_rests[0], xpos=0.5)

        # 'SheetMusic' display mode
        else:
            xdec_frac = Fraction(0, 1)
            for note_or_rest in self.notes_and_rests:
                if type(note_or_rest) is Note:
                    self._paint_note(qp, note_or_rest, xpos=float(xdec_frac))
                    xdec_frac += note_or_rest.length
                    #print('DEBUG: Staff._paint_notes() | paiting NOTE')
                # elif type(note_or_rest) is Rest:
                #     #print('DEBUG: Staff._paint_notes() | paiting REST')
                # else:
                #     #print('ERROR: Staff._paint_notes() | UNKNOWN TYPE')
                # if note_or_rest is not None:
                #     self._paint_note(qp, note=note, xdec=0)
                # else:
                #     print('Error, note is none')

    # def _paint_arrow(self, qp):
    #     """
    #     paints an arrow bellow the current note that we have to play
    #     :param qp:
    #     :return:
    #     """

    def _note_color(self):
        if self.ndec is not None:
            if self.ndec == 0:
                return QColor(COLOR_OK)
            if self.ndec < 0:
                return QColor(COLOR_LOW)
            if self.ndec > 0:
                return QColor(COLOR_HIGH)

        return QColor(COLOR_NORMAL)

    def _paint_note(self, qp, note, xpos=0.5):
        """

        :param qp:
        :param note:
        :param xpos: between 0 -> 1
        :return:
        """
        # pre-computing note position and color
        lh = self.il()
        w = self.width()
        _vcenter = int(0.6 * self.height())
        # note_center_xpos = int(xpos * w - (1.25 * lh / 2))
        _xmin, _xmax = self._get_xlims()
        note_width = (1.25 * lh)
        note_center_xpos = int(_xmin + xpos * (_xmax - _xmin) + note_width / 2)
        note_center_ypos = int(_vcenter - (note.b_index * lh/2) - (lh/2))
        note_color = self._note_color()

        # note support bar(s) if needed
        if note.b_index <= -6:
            lower_bar = note.b_index + (note.b_index % 2)
            qp.setPen(QColor(Qt.black))
            for ydec in range(lower_bar, -5, 2):
                note_ypos = int(_vcenter - (ydec * lh/2))
                xpos_l = int(note_center_xpos - (0.5 * lh)) - 1
                xpos_r = int(note_center_xpos + note_width + (0.5 * lh)) + 1
                qp.drawLine(xpos_l, note_ypos, xpos_r, note_ypos)
        elif note.b_index >= 6:
            higher_bar = note.b_index - (note.b_index % 2)
            qp.setPen(QColor(Qt.black))
            for ydec in range(higher_bar, 5, -2):
                note_ypos = int(_vcenter - (ydec * lh/2))
                xpos_l = int(note_center_xpos - (0.5 * lh)) - 1
                xpos_r = int(note_center_xpos + note_width + (0.5 * lh)) + 1
                qp.drawLine(xpos_l, note_ypos, xpos_r, note_ypos)

        # note core
        qp.setPen(note_color)
        qp.setBrush(note_color)
        qp.drawEllipse(note_center_xpos, note_center_ypos, note_width, int(lh))

        # note's vertical bar
        if note.b_index > 0:
            qp.setPen(note_color)
            # bar_xpos = int(xpos + (w / 2) - (1.25 * lh / 2))
            bar_xpos = note_center_xpos
            bar_ypos_a = int(_vcenter - (note.b_index * lh/2))
            bar_ypos_b = int(bar_ypos_a + (3.5 * lh))
            qp.drawLine(bar_xpos, bar_ypos_a, bar_xpos, bar_ypos_b)
        else:
            qp.setPen(note_color)
            # bar_xpos = int(xpos + (w / 2) + (1.25 * lh / 2))
            bar_xpos = note_center_xpos + note_width
            bar_ypos_a = int(_vcenter - (note.b_index * lh / 2))
            bar_ypos_b = int(bar_ypos_a - (3.5 * lh))
            qp.drawLine(bar_xpos, bar_ypos_a, bar_xpos, bar_ypos_b)

        # sharp(s) of flat(s) if needed
        qp.setPen(QColor(COLOR_NORMAL))
        if str(note.alteration) == '#':
            sharp_h = int(3 * lh)
            sharp_w = int(sharp_h * (self.qimages['sharp'].width() / self.qimages['sharp'].height()))
            sharp_xpos = int(note_center_xpos - sharp_h / 2)
            sharp_ypos = int(_vcenter - (note.b_index * lh/2) - (sharp_h / 2))
            qp.drawImage(QRect(sharp_xpos, sharp_ypos, sharp_w, sharp_h), self.qimages['sharp'])
        elif str(note.alteration) == 'b':
            flat_h = int(2.5 * lh)
            flat_w = int(flat_h * (self.qimages['flat'].width() / self.qimages['flat'].height()))
            flat_xpos = int(note_center_xpos - flat_w - 5)
            flat_ypos = int(_vcenter - (note.b_index * lh / 2) - (flat_h * 0.75))
            qp.drawImage(QRect(flat_xpos, flat_ypos, flat_w, flat_h), self.qimages['flat'])
        elif str(note.alteration) == '##':
            sharp_h = int(lh)
            sharp_w = int(sharp_h * (self.qimages['double-sharp'].width() / self.qimages['double-sharp'].height()))
            sharp_xpos = int(note_center_xpos - sharp_h / 2)
            sharp_ypos = int(_vcenter - (note.b_index * lh/2) - (sharp_h / 2))
            qp.drawImage(QRect(sharp_xpos, sharp_ypos, sharp_w, sharp_h), self.qimages['double-sharp'])
        elif str(note.alteration) == 'bb':
            flat_h = int(2.5 * lh)
            flat_w = int(flat_h * (self.qimages['double-flat'].width() / self.qimages['double-flat'].height()))
            flat_xpos = int(note_center_xpos - flat_w - 5)
            flat_ypos = int(_vcenter - (note.b_index * lh / 2) - (flat_h * 0.75))
            qp.drawImage(QRect(flat_xpos, flat_ypos, flat_w, flat_h), self.qimages['double-flat'])
