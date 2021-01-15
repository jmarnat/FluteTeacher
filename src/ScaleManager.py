from sys import argv
from .Note import Note
from .Arpeggiator import Arpeggiator


class ScaleManager:
    def __init__(self, str_name='F Major', mode=0, arp=Arpeggiator.UP_DOWN):
        self._scale = None
        self._mode = mode
        # self._len = 0
        self._arpeggiator = None
        self._scales_dict = {
            'Chromatic-sharp': 'C4,C#4,D4,D#4,E4,F4,F#4,G4,G#4,A4,A#4,B4',
            'Chromatic-flat': 'C4,Db4,D4,Eb4,E4,F4,Gb4,G4,Ab4,A4,Bb4,B4',
            'C Major': 'C4,D4,E4,F4,G4,A4,B4',
            'C# Major': 'C#4,D#4,E#4,F#4,G#4,A#4,B#4,C#5',
            'D Major': 'D4,E4,F#4,G4,A4,B4,C#5',
            'E Major': 'E4,F#4,G#4,A4,B4,C#5,D#5',
            'F Major': 'F4,G4,A4,Bb4,C5,D5,E5'
        }
        self.set_scale(str_name)
        self.init_arp(arp)

    def set_scale(self, scale_name):
        if scale_name in self._scales_dict.keys():
            _scale_name = scale_name
        else:
            print('WARNING: no scale named "{}"'.format(scale_name))
            _scale_name = list(self._scales_dict.keys())[0]

        self._scale = []
        for note_str in self._scales_dict[scale_name].split(','):
            note_obj = Note.from_str(note_str)
            self._scale.append(note_obj)

        self._scale.append(self._scale[0].get_8va())

    def init_arp(self, arp):
        self._arpeggiator = Arpeggiator(self._scale, arp)

    def next_arp_note(self):
        print('next_arp_note, self._arpeggiator=', self._arpeggiator)
        return self._arpeggiator.get_note()

    def is_arp_done(self):
        return self._arpeggiator.is_done()


if __name__ == '__main__':
    if (len(argv) > 1) and (argv[1] == 'test'):
        scale = ScaleManager(arp=Arpeggiator.UP)
        print('C major:')
        while not scale.is_arp_done():
            next_note = scale.next_arp_note()
            print(next_note.to_str())
