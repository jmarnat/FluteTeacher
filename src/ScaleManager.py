from sys import argv
from src.Note import Note
from src.Arpeggiator import Arpeggiator, ArpeggiatorV2
from src.Intervals import Intervals
# from src.Alteration import *


class ScaleManager:
    VALID_MODES = {
        'Major': (1, 2, 3, 4, 5, 6, 7),
        'Whole-tone': [1]
    }

    VALID_SCALES = {
        'Major': {
            '': ('C', 'D', 'E', 'F', 'G', 'A', 'B'),
            '#': ('C', 'D', 'F', 'G', 'A'),
            'b': ('D', 'E', 'G', 'A', 'B')
        },
        'Minor': {
            '': ('C', 'D', 'E', 'F', 'G', 'A', 'B'),
            '#': ('C', 'D', 'F', 'G', 'A'),
            'b': ('D', 'E', 'G', 'A', 'B')
        },
        'Whole-tone': {
            '': ('C', 'D', 'E', 'F', 'G', 'A', 'B'),
            '#': ('C', 'D', 'F', 'G', 'A'),
            'b': ('D', 'E', 'G', 'A', 'B')
        }
    }

    def __init__(self, scale_name='Major', base_note=Note(), mode=1, arp=ArpeggiatorV2.UP):
        """
        :param scale_name: str
        :param base_note: first note of the scale
        :param mode: from 1 to 7
        :param arp: class ArpeggiatorV2
        """
        if not ScaleManager._is_valid_scale(scale_name, base_note, mode):
            print('ERROR: not valid scale "{} {} - mode {}"'.format(str(base_note), scale_name, mode))
            exit(0)

        self._scale = None
        self._mode = mode
        self._arp_type = arp
        self._arpeggiator = None

        if scale_name == 'Major':
            self._scale = ScaleManager._compute_major_scale(base_note, mode)
        elif scale_name == 'Minor':
            self._scale = ScaleManager._compute_minor_scale(base_note, mode)
        else:
            print('ERROR: unknown scale "{}"'.format(scale_name))
            exit(0)

        self.init_arp()

    @staticmethod
    def _is_valid_scale(scale_name, base_note, mode):
        _letter = base_note.letter
        _alt = str(base_note.alteration)

        if scale_name not in ScaleManager.VALID_SCALES.keys():
            return False
        if _alt not in ScaleManager.VALID_SCALES[scale_name]:
            return False
        if _letter not in ScaleManager.VALID_SCALES[scale_name][_alt]:
            return False
        if mode not in ScaleManager.VALID_MODES[scale_name]:
            return False
        return True

    @staticmethod
    def _compute_major_scale(base_note, mode=1):
        scale_intervals = [
            Intervals.SECOND_MAJOR,
            Intervals.SECOND_MAJOR,
            Intervals.SECOND_MINOR,
            Intervals.SECOND_MAJOR,
            Intervals.SECOND_MAJOR,
            Intervals.SECOND_MAJOR,
            Intervals.SECOND_MINOR
        ]
        current_note = base_note
        _sc = [current_note]

        for next_scale_note, interval in zip(scale_intervals[1:], scale_intervals[:-1]):
            next_note = current_note.add_interval(interval)
            _sc.append(next_note)
            current_note = next_note

        _sc_mode = _sc[(mode - 1):] + _sc[:(mode - 1)]
        return _sc_mode

    @staticmethod
    def _compute_minor_scale(base_note, mode=1):
        scale_intervals = [
            Intervals.SECOND_MAJOR,
            Intervals.SECOND_MINOR,
            Intervals.SECOND_MAJOR,
            Intervals.SECOND_MAJOR,
            Intervals.SECOND_MINOR,
            Intervals.SECOND_MAJOR,
            Intervals.SECOND_MAJOR
        ]
        current_note = base_note
        _sc = [current_note]

        for next_scale_note, interval in zip(scale_intervals[1:], scale_intervals[:-1]):
            next_note = current_note.add_interval(interval)
            _sc.append(next_note)
            current_note = next_note

        _sc_mode = _sc[(mode - 1):] + _sc[:(mode - 1)]
        return _sc_mode

    def set_arp(self, arp_type):
        self._arp_type = arp_type
        self.init_arp()

    def init_arp(self):
        self._arpeggiator = ArpeggiatorV2(self._scale, self._arp_type)

    def next_arp_note(self):
        return self._arpeggiator.pick_note()

    def is_arp_done(self):
        return self._arpeggiator.is_done()
