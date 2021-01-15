from sys import argv
from .Note import Note


class Scale:
    C_MAJOR = 'C,D,E,F,G,A,B'
    # G_MAJOR
    D_MAJOR = 'D,E,F#,G,A,B,C#'

    ARP_SCALE_1 = [0, 1, 2, 3, 4, 5, 6, 7]
    ARP_SCALE_2 = [0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0]

    def __init__(self, pos=0, arp=ARP_SCALE_1):
        self._scale = [
            Note(-9),
            Note(-7),
            Note(-5),
            Note(-4),
            Note(-2),
            Note(0),
            Note(2),
            Note(3),
        ]
        self._len = len(self._scale)
        self._arp = arp
        self._arp_pos = pos
        self._is_arp_done = False

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
        scale = Scale(arp=Scale.ARP_SCALE_1)
        print('C major:')
        while not scale.is_arp_done():
            print(scale.get_arp_note().to_str())

        print()
        print('C major arpegio:')
        scale = Scale(arp=Scale.ARP_SCALE_2)
        while not scale.is_arp_done():
            print(scale.get_arp_note().to_str())
