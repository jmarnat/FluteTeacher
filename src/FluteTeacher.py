import threading
from time import sleep

from src.Note import Note
from src.HearAI import HearAI
from src.ScaleManager import ScaleManager
from src.Arpeggiator import Arpeggiator
from src.Alteration import Alterations
from src.MainWindow import MainWindow


VALIDATE_NOTE = True
BLINKING_TIME = 0.6
BLINKING_LOOPS = 3


class FluteTeacher:
    NOTE_MODE_RANDOM_1 = 1
    NOTE_MODE_RANDOM_2 = 2
    NOTE_MODE_SCALE = 0

    def __init__(self):
        self._current_note = None
        self._heard_note = None
        self._listening = False
        self._autonext = False
        self._scale_manager = ScaleManager(scale_name='Major',
                                           mode=1,
                                           base_note=Note('C', 4, Alterations.NATURAL),
                                           arp=Arpeggiator.UP_DOWN)

        self._note_mode = FluteTeacher.NOTE_MODE_SCALE

        # MAIN WINDOW
        self._main_window = MainWindow(flute_teacher=self)

        # NOTE RECOGNITION
        self._hear_ai = HearAI()

    def is_autonext(self):
        return self._autonext

    def is_listening(self):
        return self._listening

    def set_autonext(self, val):
        self._autonext = val

    def hearing_loop(self):
        while self._listening:
            dec = self.hear_sample()
            if self._autonext and (dec is not None) and (dec == 0):
                self.next_note(validate=True)

    def start_listening(self):
        print('FT: start listening')
        self._listening = True
        thr = threading.Thread(target=self.hearing_loop)
        thr.start()

    def stop_listening(self):
        print('FT: stop listening')
        self._listening = False

    def blink_notes(self):
        btime = (BLINKING_TIME / (2 * BLINKING_LOOPS))
        for blink_loop in range(BLINKING_LOOPS):
            self._main_window.display_note(staff='left', note=self._current_note, ndec=0)
            self._main_window.display_note(staff='right', note=self._current_note, ndec=0)
            sleep(btime)
            self._main_window.erase_note(staff='left')
            self._main_window.erase_note(staff='right')
            sleep(btime)
        return

    def next_note(self, validate=False):
        if VALIDATE_NOTE and validate and (self._current_note is not None):
            thr = threading.Thread(target=self.blink_notes())
            print('blinking thread')
            thr.start()
            thr.join()
            print('done.')

        if self._note_mode == FluteTeacher.NOTE_MODE_RANDOM_1:
            self._current_note = Note.random_note(difficulty=1, last_note=self._current_note)
        elif self._note_mode == FluteTeacher.NOTE_MODE_RANDOM_2:
            self._current_note = Note.random_note(difficulty=2, last_note=self._current_note)
        elif self._note_mode == FluteTeacher.NOTE_MODE_SCALE:
            self._current_note = self._scale_manager.next_arp_note()
        else:
            exit(0)

        if self._current_note is None:
            print('ERROR: NEW NOTE IS NONE')
            exit(0)

        self._main_window.display_note(staff='left', note=self._current_note)
        self._main_window.set_fingering(self._current_note)

    def hear_sample(self):
        self._hear_ai.record(millis=200)
        heard_note = self._hear_ai.get_last_note(alteration=self._current_note.alteration)

        if heard_note is not None:
            self._heard_note = heard_note
            dec = heard_note.midi_code - self._current_note.midi_code
            print('head note: {}'.format(heard_note))
            self._main_window.display_note(staff='right', note=heard_note, ndec=dec)
            return dec

        self._main_window.erase_note(staff='right')
        return None

    def set_scale(self, scale_name, base_note, mode):
        self._scale_manager.set_scale(scale_name, base_note, mode)
        self._scale_manager.init_arp()
        self.next_note()
