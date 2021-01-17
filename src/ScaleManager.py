from src.Intervals import Intervals
from src.Note import Note


class ScaleManager:
    VALID_MODES = {
        'Major': {
            1: 'I - Ionian',
            2: 'II - Dorian',
            3: 'III - Phrygian',
            4: 'IV - Lydian',
            5: 'V - Mixolydian',
            6: 'VI - Aeolian (Minor)',
            7: 'VII - Locrian'
        },
        'Minor': None,
        'Melodic Minor': {
            1: 'I - Melodic minor',
            2: 'II - Dorian b2 / Phrygian #6',
            3: 'III -Lydian augmented',
            4: 'IV - Lydian b6',
            5: 'V - Mixolydian b6',
            6: 'VI - Eolian b2',
            7: 'VII - Alterate'
        },
        'Harmonic minor': {
            1: 'I - Harmonic minor',
            2: 'II - Locrian #6',
            3: 'III - Ionian augmented',
            4: 'IV - Dorian #4 / Ukrainian dorian',
            5: 'V - Mixolydian b2 b6 / Phrygian Dominant',
            6: 'VI - Lydian #2',
            7: 'VII - Alterate bb7'
        },
        'Pentatonic': {
            1: 'I - Pentatonic Major',
            5: 'V - Pentatonic Minor'
        },
        'Whole-tone': None,
        'Chromatic': None
    }

    # VALID_SCALES = {
    #     'Major': {
    #         '': ('C', 'D', 'E', 'F', 'G', 'A', 'B'),
    #         '#': ('C', 'D', 'F', 'G', 'A'),
    #         'b': ('D', 'E', 'G', 'A', 'B')
    #     },
    #     'Minor': {
    #         '': ('C', 'D', 'E', 'F', 'G', 'A', 'B'),
    #         '#': ('C', 'D', 'F', 'G', 'A'),
    #         'b': ('D', 'E', 'G', 'A', 'B')
    #     },
    #     'Whole-tone': {
    #         '': ('C', 'D', 'E', 'F', 'G', 'A', 'B'),
    #         '#': ('C', 'D', 'F', 'G', 'A'),
    #         'b': ('D', 'E', 'G', 'A', 'B')
    #     },
    #     'Chromatic': {
    #         '': ('C', 'D', 'E', 'F', 'G', 'A', 'B'),
    #         '#': ('C', 'D', 'F', 'G', 'A'),
    #         'b': ('D', 'E', 'G', 'A', 'B')
    #     }
    # }

    MAJOR_INTERVALS = (
        Intervals.SECOND_MAJOR,
        Intervals.SECOND_MAJOR,
        Intervals.SECOND_MINOR,
        Intervals.SECOND_MAJOR,
        Intervals.SECOND_MAJOR,
        Intervals.SECOND_MAJOR,
        Intervals.SECOND_MINOR
    )

    MINOR_INTERVALS = (
        Intervals.SECOND_MAJOR,     # C  -> D
        Intervals.SECOND_MINOR,     # D  -> Eb
        Intervals.SECOND_MAJOR,     # Eb -> F
        Intervals.SECOND_MAJOR,     # F  -> G
        Intervals.SECOND_MINOR,     # G  -> Ab
        Intervals.SECOND_MAJOR,     # Ab -> Bb
        Intervals.SECOND_MAJOR      # Bb -> C
    )

    MINOR_HARMONIC_INTERVALS = (
        Intervals.SECOND_MAJOR,      # C  -> D
        Intervals.SECOND_MINOR,      # D  -> Eb
        Intervals.SECOND_MAJOR,      # Eb -> F
        Intervals.SECOND_MAJOR,      # F  -> G
        Intervals.SECOND_MINOR,      # G  -> Ab
        Intervals.SECOND_AUGMENTED,  # Ab -> B
        Intervals.SECOND_MINOR       # B  -> C
    )

    MINOR_MELODIC_INTERVALS = (
        Intervals.SECOND_MAJOR,      # C  -> D
        Intervals.SECOND_MINOR,      # D  -> Eb
        Intervals.SECOND_MAJOR,      # Eb -> F
        Intervals.SECOND_MAJOR,      # F  -> G
        Intervals.SECOND_MAJOR,      # G  -> A
        Intervals.SECOND_MAJOR,       # A -> B
        Intervals.SECOND_MINOR       # B  -> C
    )

    PENTATONIC_INTERVALS = (
        Intervals.SECOND_MAJOR,      # C -> D
        Intervals.SECOND_MAJOR,      # D -> E
        Intervals.THIRD_MINOR,       # E -> G
        Intervals.SECOND_MAJOR,      # G -> A
        Intervals.THIRD_MINOR        # A -> C
    )

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
            self._init_7deg_scale(ScaleManager.MAJOR_INTERVALS, allow_modes=True)
        elif self._scale_name == 'Minor':
            self._init_7deg_scale(ScaleManager.MINOR_INTERVALS, allow_modes=False)
        elif self._scale_name == 'Melodic Minor':
            self._init_7deg_scale(ScaleManager.MINOR_MELODIC_INTERVALS, allow_modes=True)
        elif self._scale_name == 'Harmonic Minor':
            self._init_7deg_scale(ScaleManager.MINOR_HARMONIC_INTERVALS, allow_modes=True)
        elif self._scale_name == 'Pentatonic':
            self._init_pentatonic_scale()
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

        # if self._scale_name not in ScaleManager.VALID_SCALES.keys():
        #     return False
        # if _alt not in ScaleManager.VALID_SCALES[self._scale_name]:
        #     return False
        # if _letter not in ScaleManager.VALID_SCALES[self._scale_name][_alt]:
        #     return False

        _available_modes = ScaleManager.VALID_MODES[self._scale_name]
        if _available_modes is not None:
            if self._mode not in _available_modes.keys():
                return False

        return True

    def _init_7deg_scale(self, scale_intervals, allow_modes=False):
        if allow_modes:
            _mode_idx = self._mode - 1
            mode_intervals = scale_intervals[_mode_idx:] + scale_intervals[:_mode_idx]
        else:
            mode_intervals = scale_intervals
        current_note = self._base_note
        self._scale = [current_note]

        for next_scale_note, interval in zip(mode_intervals[1:], mode_intervals[:-1]):
            next_note = current_note.add_interval(interval)
            self._scale.append(next_note)
            current_note = next_note

    def _init_pentatonic_scale(self):
        scale_intervals = ScaleManager.PENTATONIC_INTERVALS
        _mode_idx = self._mode - 1
        mode_intervals = scale_intervals[_mode_idx:] + scale_intervals[:_mode_idx]
        current_note = self._base_note
        self._scale = [current_note]

        for next_scale_note, interval in zip(mode_intervals[1:], mode_intervals[:-1]):
            next_note = current_note.add_interval(interval)
            self._scale.append(next_note)
            current_note = next_note

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

    # def get_mode(self, mode=1, add_octave=0):
    #     _scale = self.get_scale(add_octave=add_octave)
    #     _mode = mode-1
    #     _part_a = _scale[_mode:]
    #     _part_b = [n.get_8va() for n in _scale[:_mode]]
    #     return _part_a + _part_b

    def set_scale(self, name, mode):
        self._scale_name = name
        self._mode = mode
        self._init_scale()

    def set_basenote(self, letter, alteration):
        self._base_note = Note(letter, self._base_note.octave, alteration)
        self._init_scale()

    def set_octave(self, octave=4):
        self._base_note = self._base_note.get_8va(octave - self._base_note.octave)
        self._init_scale()

    def get_octave(self):
        return self._base_note.octave
