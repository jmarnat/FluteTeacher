import sys
import random


class Note:
    SHARP = 1

    # def __init__(self, letter='A', octave=4, alt=' '):
    #     # a_index = decay from a4:
    #     # self.NOTE_A = 0
    #     # self.NOTE_B = 1
    #     # self.NOTE_C = 3
    #     # self.NOTE_D
    #     self.letter = letter
    #     self.octave = octave
    #     self.alt = alt
    #     self.b_index = None

    def __init__(self, a4index, alt='#'):
        assert alt in ['#', 'b', '']
        if alt == '':
            alt = '#'
        note_names = {
            '#': ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'],
            'b': ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
        }
        self.a4index = a4index
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

        toto = 1

    def to_str(self):
        return "{}{} {}".format(self.letter, self.alt, self.octave)

    def to_graph(self):
        """returns the line-index + alteration"""
        return self.b_index, self.alt

    @staticmethod
    def random(difficulty=1, lastNote=None):
        ranges = {
            1: (-9, 3),
            2: (-9, 15)
        }
        rmin, rmax = ranges[difficulty]

        note = None
        if lastNote:
            while (note is None) or (note.to_str() == lastNote.to_str()):
                a4index = random.randint(rmin, rmax)
                note = Note(a4index=a4index, alt=random.choice(['#', 'b']))
            return note
        return Note(a4index=random.randint(rmin, rmax), alt='#')


def test():
    # print('A  4:', Note(0).to_str())
    # print('Ab 4:', Note(-1, 'b').to_str())
    # print('G# 4:', Note(-1, '#').to_str())
    # print('G# 4:', Note(-1).to_str())
    # print('G  4:', Note(-2).to_str())
    # print('B  4:', Note(2).to_str())
    # print('C  5:', Note(3).to_str())
    # print('C# 5:', Note(4).to_str())
    # print('D  5:', Note(5).to_str())
    #
    # print('C# 4:', Note(-8, '#').to_graph())
    # print('Db 4:', Note(-8, 'b').to_graph())
    # print('D  4:', Note(-7).to_graph())
    # print('D# 4:', Note(-6).to_graph())
    # print('Eb 4:', Note(-6, 'b').to_graph())
    # print('E  4:', Note(-5).to_graph())
    # print('F  4:', Note(-4).to_graph())
    # print('F# 4:', Note(-3, '#').to_graph())
    # print('Gb 4:', Note(-3, 'b').to_graph())
    # print('G  4:', Note(-2).to_graph())
    # print('G# 4:', Note(-1, '#').to_graph())
    # print('Ab 4:', Note(-1, 'b').to_graph())
    # print('A  4:', Note(0).to_graph())
    # print('B  4:', Note(2).to_graph())
    # print('C  5:', Note(3).to_graph())
    # print('C# 5:', Note(4).to_graph())
    # print('Db 5:', Note(4, 'b').to_graph())
    # print('D  5:', Note(5).to_graph())

    for i in range(30):
        rand_note = Note.random()
        print(rand_note.to_str(), rand_note.to_graph())


if __name__ == '__main__':
    if (len(sys.argv) > 1) and (sys.argv[1] == 'test'):
        test()
