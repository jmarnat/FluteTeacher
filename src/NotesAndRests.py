import random
from fractions import Fraction

from src.Alteration import Alteration, Alterations


class Rests:
    WHOLE_REST = Fraction(1, 1)
    HALF_REST = Fraction(1, 2)
    QUARTER_REST = Fraction(1, 4)
    EIGHTH_REST = Fraction(1, 8)


class Rest:
    def __init__(self, duration=Rests.QUARTER_REST):
        self.duration = duration


class Note:
    """
    - note_number = note indice like MIDI (C4 = 60)
    - note_letter : A, B, C, D, E, F, G
    - note_alt : '', '#' or 'b'
    - note_octave : from 0 to 8 theoretically (but should be 4 -> 6 for flute)
    """

    NOTES_NAMES = {
        '#': ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
        'b': ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    }
    NOTE_DECAYS = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    PURE_INTERVALS = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11, 8: 12}

    WHOLE_NOTE = Fraction(1, 1)
    HALF_NOTE = Fraction(1, 2)
    QUARTER_NOTE = Fraction(1, 4)
    EIGHTH_NOTE = Fraction(1, 8)

    def __init__(self, letter='C', octave=4, alteration=Alterations.NATURAL, length=QUARTER_NOTE):
        """
        :param letter: should be A -> G
        :param octave: ideally 4 -> 6~7
        :param alteration: from class Alteration
        :param length: Note.HAFL_NOTE / Note.QUARTER_NOTE / ...
        """
        self.letter = letter
        self.octave = octave
        self.alteration = alteration
        self.length = length

        self.midi_code = Note._get_midi_code(letter, octave, alteration)

        # computing graph values (B-index = index from B = center line)
        self.b_index = ('CDEFGAB'.index(self.letter)) + (7 * (self.octave - 5)) + 1

    def set_length(self, length):
        """
        Sets the length of the self = current note
        :param length: Note.QUARTER_NOTE, Note.EIGTH_NOTE, ...
        """
        self.length = length

    def to_str(self):
        str(self)

    def __str__(self):
        return self.letter + str(self.alteration) + str(self.octave)

    def get_8va(self, noct=+1):
        return Note(self.letter, self.octave + noct, self.alteration)

    def add_interval(self, interval):
        """
        :param interval: from class Interval
        """
        notes_str = list(Note.NOTE_DECAYS.keys())
        int_val, int_alt = interval

        next_note_letter = notes_str[(notes_str.index(self.letter) + int_val - 1) % 7]
        next_note_octave = self.octave
        next_note_alt = Alterations.NATURAL

        next_note_tmp = Note(next_note_letter, next_note_octave, next_note_alt)
        dec_tmp = next_note_tmp.midi_code - self.midi_code

        if dec_tmp < 0:
            next_note_octave += 1
            next_note_tmp = Note(next_note_letter, next_note_octave, next_note_alt)

        dec_tmp = next_note_tmp.midi_code - self.midi_code
        _int_alt_value = int_alt.value()
        dec_real = Note.PURE_INTERVALS[int_val] + _int_alt_value
        alt_corr = (dec_real - dec_tmp)
        next_note_alt = Alteration(semitones=alt_corr)

        final_note = Note(next_note_letter, next_note_octave, next_note_alt)
        return final_note

    @staticmethod
    def _get_midi_code(letter, octave, alteration):
        """
        :param letter: note letter (A -> G)
        :param octave: ideally from 4 -> 7 for the flute
        :param alteration: from class Alteration
        """
        _note_decay = Note.NOTE_DECAYS[letter]
        _octave_devay = 12 * (octave + 1)
        _alt_decay = alteration.value()
        return _note_decay + _octave_devay + _alt_decay

    @staticmethod
    def from_a440(a440_ref, alt_str):
        return Note.from_midi_number(a440_ref + 69, alt_str)

    @staticmethod
    def from_midi_number(midi_number, alt_str=None):
        _alt = alt_str if (alt_str in ['#', 'b']) else '#'
        note_name = Note.NOTES_NAMES[_alt]
        note_octave = (midi_number // 12) - 1
        found_note_str = note_name[midi_number % 12] + str(note_octave)
        return Note.from_str(found_note_str)

    @staticmethod
    def from_str(note_str):
        _ltr = note_str[0]
        _oct = int(note_str[-1])
        _alt_str = note_str[1] if len(note_str) == 3 else ''
        return Note(_ltr, _oct, Alteration(alt_str=_alt_str))

    @staticmethod
    def random_bis(difficulty=1):
        if difficulty == 1:
            _letters = ['C', 'D', 'E', 'F', 'G', 'A']
            _alts = ['', 'b', '#']
            return Note(letter=random.choice(_letters), octave=4, alteration=Alterations.NATURAL)
        if difficulty == 2:
            _alt = random.choice(['b', '#'])
            _note_str = random.choice(Note.NOTES_NAMES[_alt])
            return Note.from_str(_note_str)

        print('WARNING: unknown difficulty "{}" !'.format(difficulty))
        return Note(letter='C', octave=4)

    @staticmethod
    def random_note(difficulty, last_note=None):
        note = None
        if last_note:
            while (note is None) or (note.to_str() == last_note.to_str()):
                note = Note.random_bis(difficulty)
            return note
        return Note.random_bis(difficulty)
