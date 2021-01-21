from numpy.random import permutation
from fractions import Fraction

from src.Bar import Bar
from src.NotesAndRests import Note
from src.TimeSignature import TimeSignatures


class Arpeggiator:
    RANDOM = 0
    UP = 1
    UP_DOWN = 2
    DOWN = 3
    THIRDS_UP = 4
    THIRDS_DOWN = 5
    THIRDS_UP_DOWN = 6
    DOREMIDO = 7

    def __init__(self, scale_manager, kind=UP, n_octaves=1):
        self._scale_manager = scale_manager
        self._kind = kind
        self._noct = n_octaves

        self._pos = 0
        self._bar_pos = 0
        self._notes_per_bar = 4
        self._notes = []
        self._time_signature = TimeSignatures.TS_4_4

        self._isdone = False
        self._is_end_of_bar = False

        self._init_mode()

    def copy(self):
        return Arpeggiator(scale_manager=self._scale_manager,
                           kind=self._kind,
                           n_octaves=self._noct)

    def set_scale_manager(self, scale_mgr):
        self._scale_manager = scale_mgr
        self._init_mode()

    # ununsed?
    def set_mode(self, mode):
        self._kind = mode
        self._init_mode()

    # ununsed?
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
        elif self._kind == Arpeggiator.DOREMIDO:
            self._init_mode_doremido()
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
        _sc_down = self._init_mode_down()

        thirds_a = _sc_down[:-1]
        thirds_b = thirds_a[2:] + [_sc[-1].get_8va(-self._noct), _sc[-2].get_8va(-self._noct)]

        self._notes = []
        for note_a, note_b in zip(thirds_a, thirds_b):
            self._notes.append(note_a)
            self._notes.append(note_b)

        self._notes.append(_sc[0])
        return self._notes

    def _init_mode_thirds_up_down(self):
        _scale_up = self._init_mode_thirds_up()
        _scale_down = self._init_mode_thirds_down()
        self._notes = _scale_up[:-1] + _scale_down
        return self._notes

    def _init_mode_doremido(self):
        _scale_up_1 = self._init_mode_up()[:-1]
        _scale_up_2 = _scale_up_1[1:] + [_scale_up_1[0].get_8va(self._noct)]
        _scale_up_3 = _scale_up_2[1:] + [_scale_up_2[0].get_8va(self._noct)]
        _scale_up_4 = _scale_up_1
        self._notes = []
        for (_n1, _n2, _n3, _n4) in zip(_scale_up_1, _scale_up_2, _scale_up_3, _scale_up_4):
            self._notes.append(_n1)
            self._notes.append(_n2)
            self._notes.append(_n3)
            self._notes.append(_n4)
        self._notes.append(_scale_up_1[0].get_8va(self._noct))
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
            Arpeggiator.DOREMIDO: "Do ré mi do, ré mi fa ré, ...",
            Arpeggiator.RANDOM: "Random"
        }
    #
    # @staticmethod
    # def arp_dict_v2():
    #     return {
    #         "Up (quarter notes)": (Arpeggiator.UP, )
    #     }

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

    # def pick_pos_and_note(self):
    #     current_note = self._notes[self._pos]
    #     current_pos = self._pos
    #     self.pick_note()
    #     return current_pos, current_note

    def reset(self):
        self._pos = 0
        self._bar_pos = 0
        self._isdone = False
        self._is_end_of_bar = False
        self._init_mode()

    def pick_note(self):
        """
        picks the current note, and prepare the next one.
        :return: Note
        """
        current_note = self._notes[self._pos]

        if self._bar_pos >= (self._notes_per_bar-1):
            self._is_end_of_bar = True
            self._bar_pos = 0
        else:
            self._is_end_of_bar = False
            self._bar_pos += 1

        if self._pos >= (len(self._notes) - 1):
            self._isdone = True
            self._pos = 0
            # in the RANDOM case, change permutation each time.
            if self._kind == Arpeggiator.RANDOM:
                self._init_mode_random()
        else:
            self._isdone = False
            self._pos += 1

        print('Arpeggiator: picking note {}'.format(current_note))
        return current_note

    def is_end_of_bar(self):
        return self._is_end_of_bar

    def get_current_bar(self, length=4):
        """
        picks a current bar associated to the current settings
        :return:
        """
        # TODO: return the needed number of notes, not always 4
        bar = Bar(length, Note.QUARTER_NOTE)
        _pos_min = self._pos
        _pos_max = min(len(self._notes), _pos_min + length)
        for note in self._notes[_pos_min:_pos_max]:
            note.set_length(Note.QUARTER_NOTE)
            bar.add_note(note)
        return bar

    def get_notes(self):
        return self._notes

    def is_done(self):
        return self._isdone
