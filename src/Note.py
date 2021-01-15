import random


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

    def __init__(self, letter, octave, alt=''):
        self.letter = letter
        self.octave = octave
        self.alt = alt

        self.midi_code = Note._get_midi_code(letter, octave, alt)

        # computing graph values
        notes_order = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        if self.alt == '#':
            self.b_index = (notes_order.index(self.letter)) + (7 * (self.octave - 5)) + 1
        elif self.alt == 'b':
            self.b_index = (notes_order.index(self.letter)) + (7 * (self.octave - 5)) + 1
        else:
            self.b_index = (notes_order.index(self.letter)) + (7 * (self.octave - 5)) + 1

    # def same_code(self, other_note):
    #     return self.midi_code == other_note.midi_code
    #
    # def same_graph(self, other_note):
    #     return self.letter == other_note.letter \
    #         and self.octave == other_note.octave \
    #         and self.alt == other_note.alt

    def to_str(self):
        return "{}{} {}".format(self.letter, self.alt, self.octave)

    # def to_graph(self):
    #     """returns the line-index + alteration"""
    #     return self.b_index, self.alt

    @staticmethod
    def _get_midi_code(letter, octave, alt):
        _note_decay = Note.NOTE_DECAYS[letter]
        _octave_devay = 12 * (octave+1)
        _alt_decay = {'': 0, '#': +1, 'b': -1}[alt]
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
