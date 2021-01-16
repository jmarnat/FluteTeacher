from sys import argv
from src.Note import Note
from src.Arpeggiator import Arpeggiator, ArpeggiatorV2


class Alteration:
    __alt_corresp__ = {'bb': -2, 'b': -1, '': 0, ' ': 0, '#': +1, '##': +2}

    def __init__(self, semitones=None, alt_str=None):
        if semitones is not None:
            self._alt = semitones
        elif alt_str is not None:
            self._alt = Alteration.__alt_corresp__[alt_str]
        else:
            print('ERROR: no semitone or alt_str!')

    def value(self):
        return self._alt

    def to_str(self):
        return str(self)

    def __str__(self):
        return {-2: 'bb', -1: 'b', 0: '', 1: '#', 2: '##'}[self._alt]


class Alterations:
    SHARP = Alteration(semitones=1)
    DOUBLE_SHARP = Alteration(semitones=2)
    NATURAL = Alteration(semitones=0)
    FLAT = Alteration(semitones=-1)
    DOUBLE_FLAT = Alteration(semitones=-2)


class Intervals:
    UNISON_AUGMENTED = (1, Alterations.SHARP)
    SECOND_MINOR = (2, Alterations.FLAT)
    SECOND_MAJOR = (2, Alterations.NATURAL)
    SECOND_AUGMENTED = (2, Alterations.SHARP)


class Scales:
    MAJOR = [
        Intervals.SECOND_MAJOR,
        Intervals.SECOND_MAJOR,
        Intervals.SECOND_MINOR,
        Intervals.SECOND_MAJOR,
        Intervals.SECOND_MAJOR,
        Intervals.SECOND_MAJOR,
        Intervals.SECOND_MINOR
    ]

    MINOR = [
        Intervals.SECOND_MAJOR,
        Intervals.SECOND_MINOR,
        Intervals.SECOND_MAJOR,
        Intervals.SECOND_MAJOR,
        Intervals.SECOND_MINOR,
        Intervals.SECOND_MAJOR,
        Intervals.SECOND_MAJOR
    ]


class ScaleManager:
    MODES = {
        'Major': (1, 2, 3, 4, 5, 6, 7),
        'Whole-tone': [1]
    }

    def __init__(self, scale_name='Major', base_note=Note(), mode=1, arp=ArpeggiatorV2.UP):
        """
        :param scale_name: implemented: 'Major', 'Whole-tone'
        :param first_note:
        :param mode: from 1 to 7
        :param arp:
        """
        if scale_name not in ScaleManager.MODES.keys():
            print('ERROR: scale name "{}" unknown'.format(scale_name))
            return
        if mode not in ScaleManager.MODES[scale_name]:
            print('ERROR: mode no {} non-available for scale "{}"'.format(mode, scale_name))
            return

        self._scale = None
        self._mode = mode
        self._arp_type = arp
        self._arpeggiator = None
        self.set_scale(scale_name, base_note, mode)
        self.init_arp()

    @staticmethod
    def _get_scales_json():
        return

    def set_scale(self, scale_name, base_note, mode):
        """
        :param scale_name: Major/Minor
        :param base_note: note object for the base scale
        :param mode: mode (ideally from 0 fo len(scale)-1)
        :return: nothing
        """

        if scale_name == 'Major':
            self._scale = ScaleManager._compute_scale(base_note, Scales.MAJOR, mode)
        elif scale_name == 'Minor':
            self._scale = ScaleManager._compute_scale(base_note, Scales.MINOR, mode)
        # elif scale_name == 'Whole-tone':
        #     self._scale = ScaleManager._compute_scale(base_note, mode)
        else:
            print('WARNING: unknown scale name "{}"'.format(scale_name))
            self._scale = ScaleManager._compute_scale(base_note, Scales.MAJOR, mode)
        self.init_arp()

    @staticmethod
    def _compute_scale(base_note, scale_intervals, mode=1):
        # TODO: MODES
        current_note = base_note
        _sc = [current_note]

        for next_scale_note, interval in zip(scale_intervals[1:], scale_intervals[:-1]):
            next_note = current_note.add_interval(interval)
            _sc.append(next_note)
            current_note = next_note

        return _sc

    def set_arp(self, arp_type):
        self._arp_type = arp_type
        self.init_arp()

    def init_arp(self):
        self._arpeggiator = ArpeggiatorV2(self._scale, self._arp_type)

    def next_arp_note(self):
        return self._arpeggiator.pick_note()

    def is_arp_done(self):
        return self._arpeggiator.is_done()
