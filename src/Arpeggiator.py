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
