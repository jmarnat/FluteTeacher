import random
from src.Alteration import Alteration, Alterations


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

    def __init__(self, letter='C', octave=4, alteration=Alterations.NATURAL):
        """
        :param letter: should be A -> G
        :param octave: ideally 4 -> 6~7
        :param alt: '', '#' or 'b'
        """
        self.letter = letter
        self.octave = octave
        self.alteration = alteration

        self.midi_code = Note._get_midi_code(letter, octave, alteration)

        # computing graph values (B-index = index from B = center line)
        self.b_index = ('CDEFGAB'.index(self.letter)) + (7 * (self.octave - 5)) + 1

    def to_str(self):
        str(self)

    def __str__(self):
        return self.letter + str(self.alteration) + str(self.octave)

    def get_8va(self):
        return Note(self.letter, self.octave + 1, self.alteration)

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
    def from_a440(a440_ref, alt):
        return Note.from_midi_number(a440_ref + 69, alt)

    @staticmethod
    def from_midi_number(midi_number, alt=None):
        _alt = alt if (alt in ['#', 'b']) else '#'
        note_name = Note.NOTES_NAMES[_alt]
        found_note_str = note_name[midi_number % 12]
        note_letter = found_note_str[0]
        note_alt = found_note_str[1] if (len(found_note_str) == 2) else ''
        note_octave = (midi_number // 12) - 1
        return Note(note_letter, note_octave, note_alt)

    @staticmethod
    def from_str(note_str):
        _ltr = note_str[0]
        _oct = int(note_str[-1])
        _alt = note_str[1] if len(note_str) == 3 else ''
        return Note(_ltr, _oct, _alt)

    @staticmethod
    def random_bis(difficulty=1):
        if difficulty == 1:
            _letters = ['C', 'D', 'E', 'F', 'G', 'A']
            _alts = ['', 'b', '#']
            return Note(letter=random.choice(_letters), octave=4, alt='')
        if difficulty == 2:
            _alt = random.choice(['b', '#'])
            _note_str = random.choice(Note.NOTES_NAMES[_alt])
            note_letter = _note_str[0]
            note_alt = _note_str[1] if len(_note_str) == 2 else ''
            return Note(letter=note_letter, octave=4, alt=note_alt)

        print('unknown difficulty!')
        return Note(letter='C', octave=4, alt='')

    @staticmethod
    def random_note(difficulty, last_note=None):
        note = None
        if last_note:
            while (note is None) or (note.to_str() == last_note.to_str()):
                note = Note.random_bis(difficulty)
            return note
        return Note.random_bis(difficulty)
