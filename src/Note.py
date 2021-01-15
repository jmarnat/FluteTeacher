import random


class Note:
    def __init__(self, a4index, alt='#'):
        assert alt in ['#', 'b', '']
        if alt == '':
            alt = '#'
        note_names = {
            '#': ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'],
            'b': ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
        }
        self._a4index = a4index
        _found_note = note_names[alt][a4index % 12]
        self.letter = _found_note[0]
        self.octave = (a4index // 12) + 4 + int((a4index % 12) >= 3)
        if len(_found_note) == 2:
            self.alt = _found_note[1]
        else:
            self.alt = ' '

        # computing graph values
        notes_order = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        if self.alt == '#':
            self.b_index = (notes_order.index(self.letter)) + (7 * (self.octave - 5)) + 1
        elif self.alt == 'b':
            self.b_index = (notes_order.index(self.letter)) + (7 * (self.octave - 5)) + 1
        else:
            self.b_index = (notes_order.index(self.letter)) + (7 * (self.octave - 5)) + 1

    def to_str(self):
        return "{}{} {}".format(self.letter, self.alt, self.octave)

    def to_graph(self):
        """returns the line-index + alteration"""
        return self.b_index, self.alt

    def a4index(self):
        return self._a4index

    @staticmethod
    def random(difficulty=1, last_note=None):
        ranges = {
            1: (-9, 3),
            2: (-9, 15)
        }
        rmin, rmax = ranges[difficulty]

        note = None
        if last_note:
            while (note is None) or (note.to_str() == last_note.to_str()):
                a4index = random.randint(rmin, rmax)
                note = Note(a4index=a4index, alt=random.choice(['#', 'b']))
            return note
        return Note(a4index=random.randint(rmin, rmax), alt='#')
