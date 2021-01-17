from src.Intervals import Intervals
from src.Note import Note


class ScaleManager:
    VALID_MODES = {
        'Major': {
            1: 'Ionian',
            2: 'Dorian',
            3: 'Phrygian',
            4: 'Lydian',
            5: 'Mixolydian',
            6: 'Aeolian (Minor)',
            7: 'Locrian'
        },
        'Minor': {
            1: 'Aeolian',
            2: 'Locrian',
            3: 'Ionian (Major)',
            4: 'Dorian',
            5: 'Phrygian',
            6: 'Lydian',
            7: 'Mixolydian',
        },
        'Whole-tone': {1: 'Whole-tone'},
        'Chromatic': {1: 'Chromatic'}
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
        },
        'Chromatic': {
            '': ('C', 'D', 'E', 'F', 'G', 'A', 'B'),
            '#': ('C', 'D', 'F', 'G', 'A'),
            'b': ('D', 'E', 'G', 'A', 'B')
        }
    }

    def __init__(self, scale_name='Major', base_note=Note(), mode=1):
        """
        :param scale_name: str
        :param base_note: first note of the scale
        :param mode: from 1 to 7
        """

        self._scale = None
        self._scale_name = scale_name
        self._mode = mode
        self._base_note = base_note
        self._init_scale()

    def _init_scale(self):
        if not self._is_valid_scale():
            print('ERROR: not valid scale "{} {} - mode {}"'.format(str(self._base_note), self._scale_name, self._mode))
            exit(0)

        print('ScaleManager: setting scale {} {} - mode {}'.format(str(self._base_note), self._scale_name, self._mode))

        if self._scale_name == 'Major':
            self._init_major_scale()
        elif self._scale_name == 'Minor':
            self._init_minor_scale()
        elif self._scale_name == 'Whole-tone':
            self._init_wholetone_scale()
        elif self._scale_name == 'Chromatic':
            self._init_chromatic_scale()
        else:
            print('ERROR: unknown scale "{}"'.format(self._scale_name))
            exit(0)

    def _is_valid_scale(self):
        _letter = self._base_note.letter
        _alt = str(self._base_note.alteration)

        if self._scale_name not in ScaleManager.VALID_SCALES.keys():
            return False
        if _alt not in ScaleManager.VALID_SCALES[self._scale_name]:
            return False
        if _letter not in ScaleManager.VALID_SCALES[self._scale_name][_alt]:
            return False
        if self._mode not in ScaleManager.VALID_MODES[self._scale_name].keys():
            return False
        return True

    def _init_major_scale(self):
        scale_intervals = [
            Intervals.SECOND_MAJOR,
            Intervals.SECOND_MAJOR,
            Intervals.SECOND_MINOR,
            Intervals.SECOND_MAJOR,
            Intervals.SECOND_MAJOR,
            Intervals.SECOND_MAJOR,
            Intervals.SECOND_MINOR
        ]
        current_note = self._base_note
        _sc = [current_note]

        for next_scale_note, interval in zip(scale_intervals[1:], scale_intervals[:-1]):
            next_note = current_note.add_interval(interval)
            _sc.append(next_note)
            current_note = next_note

        _sc_mode = _sc[(self._mode - 1):] + _sc[:(self._mode - 1)]
        self._scale = _sc_mode

    def _init_minor_scale(self):
        scale_intervals = [
            Intervals.SECOND_MAJOR,
            Intervals.SECOND_MINOR,
            Intervals.SECOND_MAJOR,
            Intervals.SECOND_MAJOR,
            Intervals.SECOND_MINOR,
            Intervals.SECOND_MAJOR,
            Intervals.SECOND_MAJOR
        ]
        current_note = self._base_note
        _sc = [current_note]

        for next_scale_note, interval in zip(scale_intervals[1:], scale_intervals[:-1]):
            next_note = current_note.add_interval(interval)
            _sc.append(next_note)
            current_note = next_note

        _sc_mode = _sc[(self._mode - 1):] + _sc[:(self._mode - 1)]
        self._scale = _sc_mode

    def _init_wholetone_scale(self):
        _scale1 = ['C', 'D', 'E', 'F#', 'G#', 'A#']
        _scale2 = ['C', 'D', 'E', 'Gb', 'Ab', 'Bb']
        _scale3 = ['C#', 'D#', 'F', 'G', 'A', 'B']
        _scale4 = ['Db', 'Eb', 'F', 'G', 'A', 'B']

        _oct = self._base_note.octave
        for _scale_str_list in [_scale1, _scale2, _scale3, _scale4]:
            _note_str = "{}{}".format(self._base_note.letter, self._base_note.alteration)
            if _note_str in _scale_str_list:
                _note_idx = _scale_str_list.index(_note_str)
                _scale_part1 = [Note.from_str("{}{}".format(n, _oct)) for n in _scale_str_list[_note_idx:]]
                _scale_part2 = [Note.from_str("{}{}".format(n, _oct)).get_8va() for n in _scale_str_list[:_note_idx]]
                print('full wholetone mode computed ok')
                self._scale = _scale_part1 + _scale_part2
                break

    def _init_chromatic_scale(self):
        _scale_sharps = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        _scale_flats = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        _oct = self._base_note.octave
        for _scale_str_list in [_scale_sharps, _scale_flats]:
            _note_str = "{}{}".format(self._base_note.letter, self._base_note.alteration)
            if _note_str in _scale_str_list:
                _note_idx = _scale_str_list.index(_note_str)
                _scale_part1 = [Note.from_str("{}{}".format(n, _oct)) for n in _scale_str_list[_note_idx:]]
                _scale_part2 = [Note.from_str("{}{}".format(n, _oct)).get_8va() for n in _scale_str_list[:_note_idx]]
                print('full wholetone mode computed ok')
                self._scale = _scale_part1 + _scale_part2
                break

    def get_scale(self, add_octave=0):
        _sc = self._scale
        for i in range(add_octave):
            _sc = [note.get_8va() for note in _sc]
        return _sc

    def get_mode(self, mode=1, add_octave=0):
        _scale = self.get_scale(add_octave=add_octave)
        _mode = mode-1
        _part_a = _scale[_mode:]
        _part_b = [n.get_8va() for n in _scale[:_mode]]
        return _part_a + _part_b

    def set_octave(self, octave=4):
        self._base_note = self._base_note.get_8va(octave - self._base_note.octave)
        self._init_scale()

    def get_octave(self):
        return self._base_note.octave
