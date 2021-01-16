

class ArpeggiatorV2:
    UP = 1
    UP_DOWN = 2
    THIRDS_UP = 3
    THIRDS_DOWN = 4
    THIRDS_UP_DOWN = 5

    def __init__(self, scale, mode):
        self._notes = []
        self._scale = scale
        self._mode = mode
        self._pos = 0
        self._isdone = False
        if mode == ArpeggiatorV2.UP:
            self._init_mode_up()
        elif mode == ArpeggiatorV2.UP_DOWN:
            self._init_mode_updown()
        elif mode == ArpeggiatorV2.THIRDS_UP:
            self._init_mode_thirds()
        else:
            print('WARNING: ArpeggiatorV2: no mode {}'.format(mode))
            self._init_mode_up()

    def _init_mode_up(self):
        self._notes = []
        for note in self._scale:
            self._notes.append(note)
        self._notes.append(self._scale[0].get_8va())
        return

    def _init_mode_updown(self):
        self._notes = []
        for note in self._scale:
            self._notes.append(note)
        self._notes.append(self._scale[0].get_8va())
        for note in reversed(self._scale):
            self._notes.append(note)
        return

    def _init_mode_thirds(self):
        thirds_a = self._scale
        thirds_b = self._scale[2:] + [self._scale[0].get_8va(), self._scale[1].get_8va()]

        self._notes = []
        for a, b in zip(thirds_a, thirds_b):
            self._notes.append(a)
            self._notes.append(b)
        self._notes.append(self._scale[0].get_8va())
        return

    def pick_note(self):
        """
        picks the current note, and prepare the next one.
        :return: Note
        """
        current_note = self._notes[self._pos]
        if self._pos == (len(self._notes) - 1):
            self._isdone = True
            self._pos = 0
        else:
            self._isdone = False
            self._pos += 1
        return current_note

    def is_done(self):
        return self._isdone


class Arpeggiator:
    UP = 1
    UP_DOWN = 2

    def __init__(self, scale, kind=UP):
        """
        :param scale: list of Notes
        :param kind:
        """
        self._kind = kind
        self._scale = scale
        self._step = 0
        self._idx = 0
        self._isdone = False

    def get_note(self):
        idx = self._idx

        if self._kind == Arpeggiator.UP:
            if (self._step + 1) >= len(self._scale):
                self._step = 0
                self._isdone = True
            else:
                self._step += 1
                self._isdone = False
            self._idx = self._step
            return self._scale[idx]

        elif self._kind == Arpeggiator.UP_DOWN:
            if (self._step + 1) >= (2 * len(self._scale) - 2):
                self._step = 0
                self._idx = 0
                self._isdone = True
            elif (self._step + 1) < len(self._scale):
                self._step += 1
                self._idx += 1
                self._isdone = False
            else:
                self._step += 1
                self._idx -= 1
                self._isdone = False
            return self._scale[idx]

        else:
            print('ERROR: no such Arpeggio')

    def is_done(self):
        return self._isdone
