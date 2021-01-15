from sys import argv
from .Note import Note
from .Arpeggio import Arpeggio


class Scales:
    def __init__(self):
        self.scales_str = {
            'C Major': 'C4,D4,E4,F4,G4,A4,B4',
            'D Major': 'D4,E4,F#4,G4,A4,B4,C#5',
            'E Major': 'E4,F#4,G#4,A4,B4,C#5,D#5',
            'F Major': 'F4,G4,A4,Bb4,C5,D5,E5'
        }


class ScaleManager:
    def __init__(self, str_name='C Major', mode=0, arp=Arpeggio.UP):
        self._scale = None
        self._mode = mode
        self._arp = arp
        self._len = 0
        self._is_arp_done = False
        self._arp_pos = 0
        self.set_scale(str_name)

    def set_scale(self, str_name='C Major'):
        self._scale = [
            Note('C', 4),
            Note('D', 4),
            Note('E', 4),
            Note('F', 4),
            Note('G', 4),
            Note('A', 4),
            Note('B', 4),
            Note('C', 5),
        ]
        self._len = len(self._scale)
        self.reset_arp()

    def get_arp_note(self):
        note = self._scale[self._arp[self._arp_pos]]
        if (self._arp_pos + 1) == len(self._arp):
            self._is_arp_done = True
        self._arp_pos = (self._arp_pos + 1) % len(self._arp)
        return note

    def reset_arp(self):
        self._arp_pos = 0
        self._is_arp_done = False

    def is_arp_done(self):
        return self._is_arp_done


if __name__ == '__main__':
    if (len(argv) > 1) and (argv[1] == 'test'):
        scale = ScaleManager(arp=Arpeggio.UP)
        print('C major:')
        while not scale.is_arp_done():
            print(scale.get_arp_note().to_str())

        print()
        print('C major arpegio:')
        scale = ScaleManager(arp=Arpeggio.UP_DOWN)
        while not scale.is_arp_done():
            print(scale.get_arp_note().to_str())
