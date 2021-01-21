from src.NotesAndRests import Note
from src.ScaleManager import ScaleManager
from src.Arpeggiator import Arpeggiator

if __name__ == '__main__':
    sm = ScaleManager()

    print('C Major UP: ', end='')
    sm._set_scale('Major', Note('C', 4), mode=0)
    sm.set_arp(Arpeggiator.UP)
    while not sm.is_arp_done():
        print(sm.next_arp_note().to_str(), end='')
        if not sm.is_arp_done():
            print(', ', end='')
    print()

    print('C Major UP-DOWN: ', end='')
    sm._set_scale('Major', Note('C', 4), mode=0)
    sm.set_arp(Arpeggiator.UP_DOWN)
    while not sm.is_arp_done():
        print(sm.next_arp_note().to_str(), end='')
        if not sm.is_arp_done():
            print(', ', end='')
    print()

    print('C Major THIRDS-UP: ', end='')
    sm._set_scale('Major', Note('C', 4), mode=0)
    sm.set_arp(Arpeggiator.THIRDS_UP)
    while not sm.is_arp_done():
        print(sm.next_arp_note().to_str(), end='')
        if not sm.is_arp_done():
            print(', ', end='')
    print()

    print('C full tone UP: ', end='')
    sm._set_scale('Whole-tone', Note('C', 4), mode=0)
    sm.set_arp(Arpeggiator.UP)
    while not sm.is_arp_done():
        print(sm.next_arp_note().to_str(), end='')
        if not sm.is_arp_done():
            print(', ', end='')
    print()

    print('C full tone UP: ', end='')
    sm._set_scale('Whole-tone', Note('C', 4), mode=0)
    sm.set_arp(Arpeggiator.UP_DOWN)
    while not sm.is_arp_done():
        print(sm.next_arp_note().to_str(), end='')
        if not sm.is_arp_done():
            print(', ', end='')
    print()

    print('C full tone UP: ', end='')
    sm._set_scale('Whole-tone', Note('C', 4), mode=0)
    sm.set_arp(Arpeggiator.THIRDS_UP)
    while not sm.is_arp_done():
        print(sm.next_arp_note().to_str(), end='')
        if not sm.is_arp_done():
            print(', ', end='')
    print()

