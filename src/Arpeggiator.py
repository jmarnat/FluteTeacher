

class Arpeggiator:
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
        if mode == Arpeggiator.UP:
            self._init_mode_up()
        elif mode == Arpeggiator.UP_DOWN:
            self._init_mode_updown()
        elif mode == Arpeggiator.THIRDS_UP:
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

        # (i'm not sure if counting the last one or not..)
        # for note in self._scale[1:][::-1]:
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
