

class Arpeggiator:
    UP = 1
    UP_DOWN = 2
    DOWN = 3
    THIRDS_UP = 4
    # THIRDS_DOWN = 5
    # THIRDS_UP_DOWN = 6

    def __init__(self, scale_manager, kind=UP, n_octaves=1, start_octave=4):
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
        elif self._kind == Arpeggiator.UP_DOWN:
            self._init_mode_updown()
        elif self._kind == Arpeggiator.THIRDS_UP:
            self._init_mode_thirds_up()
        else:
            print('WARNING: ArpeggiatorV2: no mode {}'.format(self._kind))
            self._init_mode_up()

    def _init_mode_up(self):
        self._notes = []
        for _oct in range(self._noct):
            _sc = self._scale_manager.get_scale(add_octave=_oct, )
            self._notes += _sc
        self._notes.append(self._scale_manager.get_scale()[0].get_8va(noct=self._noct))
        print('MODE UP, NOCT=', self._noct)
        print('MODE UP, NOTES: ', ', '.join([str(n) for n in self._notes]))
        return

    def _init_mode_updown(self):
        self._init_mode_up()
        self._notes += self._notes[:-1][::-1]
        return

    def _init_mode_thirds_up(self):
        self._init_mode_up()
        _sc = self._scale_manager.get_scale(0)

        thirds_a = _sc
        thirds_b = _sc[2:] + [_sc[0].get_8va(), _sc[1].get_8va()]

        self._notes = []
        for _oct in range(self._noct):
            for note_a, note_b in zip(thirds_a, thirds_b):
                self._notes.append(note_a.get_8va(_oct))
                self._notes.append(note_b.get_8va(_oct))

        self._notes.append(_sc[0].get_8va(self._noct))
        return

    def to_str(self):
        return str(self)

    @staticmethod
    def arp_dict():
        return {
            Arpeggiator.UP: "Up",
            Arpeggiator.UP_DOWN: "Up/Down",
            Arpeggiator.DOWN: "Down",
            Arpeggiator.THIRDS_UP: "Thirds up",
            # Arpeggiator.THIRDS_UP_DOWN: "Thirds up/down"
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
        else:
            self._isdone = False
            self._pos += 1
        return current_note

    def is_done(self):
        return self._isdone

    # def set_mode(self, arp_mode):
    #     self._mode = arp_mode
    #     self.init_arp()

    # def next_arp_note(self):
    #     return self.pick_note()

    # def is_arp_done(self):
    #     return self.is_done()
