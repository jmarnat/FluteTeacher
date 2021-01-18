from numpy.random import permutation


class Arpeggiator:
    RANDOM = 0
    UP = 1
    UP_DOWN = 2
    DOWN = 3
    THIRDS_UP = 4
    THIRDS_DOWN = 5
    THIRDS_UP_DOWN = 6

    def __init__(self, scale_manager, kind=UP, n_octaves=1):
        self._notes = []
        self._scale_manager = scale_manager
        self._kind = kind
        self._noct = n_octaves
        self._pos = 0
        self._isdone = False

        self._init_mode()

    def set_scale_manager(self, scale_mgr):
        self._scale_manager = scale_mgr
        self._init_mode()

    def set_mode(self, mode):
        self._kind = mode
        self._init_mode()

    def set_noctaves(self, n_octaves):
        self._noct = n_octaves
        self._init_mode()

    def _init_mode(self):
        self._pos = 0
        self._isdone = False

        if self._kind == Arpeggiator.UP:
            self._init_mode_up()
        elif self._kind == Arpeggiator.DOWN:
            self._init_mode_down()
        elif self._kind == Arpeggiator.UP_DOWN:
            self._init_mode_updown()
        elif self._kind == Arpeggiator.THIRDS_UP:
            self._init_mode_thirds_up()
        elif self._kind == Arpeggiator.THIRDS_DOWN:
            self._init_mode_thirds_down()
        elif self._kind == Arpeggiator.THIRDS_UP_DOWN:
            self._init_mode_thirds_up_down()
        elif self._kind == Arpeggiator.RANDOM:
            self._init_mode_random()
        else:
            print('WARNING: ArpeggiatorV2: no mode {}'.format(self._kind))
            self._init_mode_up()

    def _init_mode_up(self):
        self._notes = []
        for _oct in range(self._noct):
            self._notes += self._scale_manager.get_scale(add_octave=_oct)
        self._notes.append(self._scale_manager.get_scale()[0].get_8va(noct=self._noct))
        return self._notes

    def _init_mode_down(self):
        _scale_up = self._init_mode_up()
        self._notes = _scale_up[::-1]
        return self._notes

    def _init_mode_updown(self):
        _scale_up = self._init_mode_up()
        _scale_down = self._init_mode_down()
        self._notes = _scale_up + _scale_down[1:]

    def _init_mode_thirds_up(self):
        _sc = self._init_mode_up()[:-1]

        thirds_a = _sc
        thirds_b = _sc[2:] + [_sc[0].get_8va(self._noct), _sc[1].get_8va(self._noct)]

        self._notes = []
        for note_a, note_b in zip(thirds_a, thirds_b):
            self._notes.append(note_a)
            self._notes.append(note_b)

        self._notes.append(_sc[0].get_8va(self._noct))
        return self._notes

    def _init_mode_thirds_down(self):
        _sc = self._init_mode_up()
        # _sc_down = [_sc[0].get_8va(self._noct)] + _sc[1:][::-1]
        _sc_down = self._init_mode_down()

        thirds_a = _sc_down[:-1]
        thirds_b = thirds_a[2:] + [_sc[-1].get_8va(-self._noct), _sc[-2].get_8va(-self._noct)]

        self._notes = []
        # for _oct in range(self._noct, 0, -1):
        for note_a, note_b in zip(thirds_a, thirds_b):
            self._notes.append(note_a)#.get_8va(_oct-1))
            self._notes.append(note_b)#.get_8va(_oct-1))

        self._notes.append(_sc[0])
        return self._notes

    def _init_mode_thirds_up_down(self):
        _scale_up = self._init_mode_thirds_up()
        _scale_down = self._init_mode_thirds_down()
        self._notes = _scale_up[:-1] + _scale_down
        return self._notes

    def _init_mode_random(self):
        self._init_mode_up()
        self._notes = permutation(self._notes)

    def to_str(self):
        return str(self)

    @staticmethod
    def arp_dict():
        return {
            Arpeggiator.UP: "Up",
            Arpeggiator.DOWN: "Down",
            Arpeggiator.UP_DOWN: "Up/Down",
            Arpeggiator.THIRDS_UP: "Thirds up",
            Arpeggiator.THIRDS_DOWN: "Thirds down",
            Arpeggiator.THIRDS_UP_DOWN: "Thirds up/down",
            Arpeggiator.RANDOM: "Random"
        }

    @staticmethod
    def noct_dict():
        return {
            1: "1 Octave",
            2: "2 Octaves"
        }

    def __str__(self):
        _mode_dict = Arpeggiator.arp_dict()
        _noct_dict = Arpeggiator.noct_dict()
        return _mode_dict[self._kind] + " - " + _noct_dict[self._noct]

    def pick_note(self):
        """
        picks the current note, and prepare the next one.
        :return: Note
        """
        current_note = self._notes[self._pos]
        if self._pos == (len(self._notes) - 1):
            self._isdone = True
            self._pos = 0
            # in the RANDOM case, change permutation each time.
            if self._kind == Arpeggiator.RANDOM:
                self._init_mode_random()
        else:
            self._isdone = False
            self._pos += 1
        return current_note

    def is_done(self):
        return self._isdone
