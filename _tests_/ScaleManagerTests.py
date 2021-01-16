from src.Note import Note
from src.ScaleManager import ScaleManager
from src.Arpeggiator import ArpeggiatorV2

if __name__ == '__main__':
    sm = ScaleManager()

    print('C Major UP: ', end='')
    sm.set_scale('Major', Note('C', 4), mode=0)
    sm.set_arp(ArpeggiatorV2.UP)
    while not sm.is_arp_done():
        print(sm.next_arp_note().to_str(), end='')
        if not sm.is_arp_done():
            print(', ', end='')
    print()

    print('C Major UP-DOWN: ', end='')
    sm.set_scale('Major', Note('C', 4), mode=0)
    sm.set_arp(ArpeggiatorV2.UP_DOWN)
    while not sm.is_arp_done():
        print(sm.next_arp_note().to_str(), end='')
        if not sm.is_arp_done():
            print(', ', end='')
    print()

    print('C Major THIRDS-UP: ', end='')
    sm.set_scale('Major', Note('C', 4), mode=0)
    sm.set_arp(ArpeggiatorV2.THIRDS_UP)
    while not sm.is_arp_done():
        print(sm.next_arp_note().to_str(), end='')
        if not sm.is_arp_done():
            print(', ', end='')
    print()

    print('C full tone UP: ', end='')
    sm.set_scale('Whole-tone', Note('C', 4), mode=0)
    sm.set_arp(ArpeggiatorV2.UP)
    while not sm.is_arp_done():
        print(sm.next_arp_note().to_str(), end='')
        if not sm.is_arp_done():
            print(', ', end='')
    print()

    print('C full tone UP: ', end='')
    sm.set_scale('Whole-tone', Note('C', 4), mode=0)
    sm.set_arp(ArpeggiatorV2.UP_DOWN)
    while not sm.is_arp_done():
        print(sm.next_arp_note().to_str(), end='')
        if not sm.is_arp_done():
            print(', ', end='')
    print()

    print('C full tone UP: ', end='')
    sm.set_scale('Whole-tone', Note('C', 4), mode=0)
    sm.set_arp(ArpeggiatorV2.THIRDS_UP)
    while not sm.is_arp_done():
        print(sm.next_arp_note().to_str(), end='')
        if not sm.is_arp_done():
            print(', ', end='')
    print()

