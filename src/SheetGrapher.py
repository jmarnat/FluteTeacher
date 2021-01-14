from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class SheetGrapher(QWidget):
    def __init__(self, kind='normal'):
        super(SheetGrapher, self).__init__()
        self.height()
        self.notes = []


        self.qimages = {
            'sharp': QImage('res/sharp.png'),
            'flat': QImage('res/flat.png'),
            'g-clef': QImage('res/g-clef.png')
        }
        # self.image_sharp = QImage('res/sharp.png')
        # self.image_flat = QImage('res/flat.png')
        # self.image_g_clef = QImage('res/g-clef.png')
        self.kind = kind

    def mid_height(self):
        return self.height() / 2

    def il(self):
        """inter-line height"""
        return self.height() / 12

    def display_note(self, val, alt):
        self.notes = [(val, alt)]
        self.repaint()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(Qt.black))

        clef_h = int(self.il() * 8)
        clef_w = int(clef_h * (self.qimages['g-clef'].width() / self.qimages['g-clef'].height()))
        clef_xpos = 0
        clef_ypos = int(self.mid_height() - (clef_h/2))
        qp.drawImage(QRect(clef_xpos, clef_ypos, clef_w, clef_h), self.qimages['g-clef'])

        for i in [-2, -1, 0, 1, 2]:
            ypos = int(self.mid_height() - (i * self.il()))
            xpos = int(self.width() / 2)
            qp.drawLine(0, ypos, xpos+100, ypos)

        xdec = -50
        for (note, alt) in self.notes:
            self._paint_note(qp, note_index=note, xdec=xdec, alt=alt)
            xdec += 50
        qp.end()

    def _paint_note(self, qp, note_index, xdec, alt=''):
        qp.setPen(QColor(Qt.black))
        qp.setBrush(QBrush(Qt.black))
        lh = self.il()

        # note
        xpos = int(xdec + (self.width() / 2) - (1.25 * lh / 2))
        ypos = int(self.mid_height() - (note_index * lh/2) - (lh/2))
        qp.drawEllipse(xpos, ypos, int(1.25 * lh), int(lh))

        # sharp if needed
        if alt == '#':
            sharp_h = int(3 * lh)
            sharp_w = int(sharp_h * (self.qimages['sharp'].width() / self.qimages['sharp'].height()))
            sharp_xpos = int(xpos - sharp_h / 2)
            sharp_ypos = int(self.mid_height() - (note_index * lh/2) - (sharp_h / 2))
            qp.drawImage(QRect(sharp_xpos, sharp_ypos, sharp_w, sharp_h), self.qimages['sharp'])
        elif alt == 'b':
            flat_h = int(2.5 * lh)
            flat_w = int(flat_h * (self.qimages['flat'].width() / self.qimages['flat'].height()))
            flat_xpos = int(xpos - flat_w - 5)
            flat_ypos = int(self.mid_height() - (note_index * lh / 2) - (flat_h * 0.75))
            qp.drawImage(QRect(flat_xpos, flat_ypos, flat_w, flat_h), self.qimages['flat'])

        # lower bar(s) if needed
        if note_index <= -6:
            lower_bar = note_index + (note_index % 2)
            qp.setPen(QColor(Qt.black))
            for ydec in range(lower_bar, -5, 2):
                ypos = int(self.mid_height() - (ydec * lh/2))
                xpos_l = int(xpos - (0.5 * lh)) - 1
                xpos_r = int(xpos + (1.25 * lh) + (0.5 * lh)) + 1
                qp.drawLine(xpos_l, ypos, xpos_r, ypos)

        # upper bar(s) if needed
        elif note_index >= 6:
            higher_bar = note_index - (note_index % 2)
            qp.setPen(QColor(Qt.black))
            for ydec in range(higher_bar, 5, -2):
                ypos = int(self.mid_height() - (ydec * lh/2))
                xpos_l = int(xpos - (0.5 * lh)) - 1
                xpos_r = int(xpos + (1.25 * lh) + (0.5 * lh)) + 1
                qp.drawLine(xpos_l, ypos, xpos_r, ypos)

        # vertical bar
        if note_index > 0:
            qp.setPen(QColor(Qt.black))
            bar_xpos = int(xdec + (self.width() / 2) - (1.25 * lh / 2))
            bar_ypos_a = int(self.mid_height() - (note_index * lh/2))
            bar_ypos_b = int(bar_ypos_a + (3.5 * lh))
            qp.drawLine(bar_xpos, bar_ypos_a, bar_xpos, bar_ypos_b)
        else:
            qp.setPen(QColor(Qt.black))
            bar_xpos = int(xdec + (self.width() / 2) + (1.25 * lh / 2))
            bar_ypos_a = int(self.mid_height() - (note_index * lh / 2))
            bar_ypos_b = int(bar_ypos_a - (3.5 * lh))
            qp.drawLine(bar_xpos, bar_ypos_a, bar_xpos, bar_ypos_b)
            # xpos = int(xdec + (self.width() / 2) - (1.25 * lh / 2))
            # ypos = int(self.mid_height() - (note_index * lh/2) - (lh/2))
