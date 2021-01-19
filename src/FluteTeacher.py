import threading
from time import sleep
from copy import copy

from src.Note import Note
from src.HearAI import HearAI
from src.ScaleManager import ScaleManager
from src.Arpeggiator import Arpeggiator
from src.MainWindow import MainWindow
from src.Fingerings import Fingerings, FingeringError
from src.Settings import Settings


VALIDATE_NOTE = True
VALIDATE_TIME = 0.2


class FluteTeacher:
    def __init__(self):
        self._current_note = None
        self._heard_note = None
        self._listening = Settings.START_LISTENING_AT_STARTUP
        self._autonext = Settings.START_AUTONEXT_AT_STARTUP
        #-- self._start_octave = Settings.DEFAULT_BASE_NOTE_OCTAVE

        # MAIN WINDOW
        self._main_window = MainWindow(flute_teacher=self)

        # SCALE MANAGER AND ARPEGGIATOR
        self._scale_manager = ScaleManager(scale_name=Settings.DEFAULT_SCALE_NAME,
                                           base_note=Note(letter=Settings.DEFAULT_BASE_NOTE_LETTER,
                                                          alteration=Settings.DEFAULT_BASE_NOTE_ALTERATION,
                                                          octave=Settings.DEFAULT_BASE_NOTE_OCTAVE),
                                           mode=Settings.DEFAULT_SCALE_MODE)

        self._arpeggiator = Arpeggiator(self._scale_manager,
                                        kind=Settings.DEFAULT_ARPEGGIATOR_KIND,
                                        n_octaves=Settings.DEFAULT_ARP_N_OCTAVES)
        self.next_note()

        # NOTE RECOGNITION
        self._hear_ai = HearAI()
        if self._autonext:
            self.set_autonext(True)
        if self._listening:
            self.start_listening()

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

    def validate_notes_gui(self):
        self._main_window.display_note(staff='left', note=self._current_note, ndec=0)
        self._main_window.display_note(staff='right', note=self._current_note, ndec=0)
        sleep(VALIDATE_TIME)
        self._main_window.erase_note(staff='left')
        self._main_window.erase_note(staff='right')

    def next_note(self, validate=False):
        if VALIDATE_NOTE and validate and (self._current_note is not None):
            self.validate_notes_gui()

        self._current_note = self._arpeggiator.pick_note()

        if self._current_note is None:
            print('ERROR: NEW NOTE IS NONE')
            exit(0)

        self._main_window.display_note(staff='left', note=self._current_note)
        self._main_window.fingering.set_fingering(self._current_note)

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

    # def check_playability(self):
    #     Fingering.check_notes(self._arpeggiator.get_notes())
        # is_ok = Fingering.check_notes(self._arpeggiator.get_notes())
        # if not is_ok:
        #     print('WARNING: CONTAINS UNREGISTERED FINGERINGS')
        #     self._main_window.display_fingering_warning()

    # def get_start_octave(self):
    #     return self._start_octave

    def set_scale(self, scale_name, mode):
        _scale_mgr_tmp = copy(self._scale_manager)
        _scale_mgr_tmp.set_scale(scale_name, mode)
        _arpeggiator_tmp = copy(self._arpeggiator)
        _arpeggiator_tmp.set_scale_manager(_scale_mgr_tmp)

        if Fingerings.check_notes(_arpeggiator_tmp.get_notes()):
            self._scale_manager = _scale_mgr_tmp
            self._arpeggiator = _arpeggiator_tmp
            self.next_note()
        else:
            print('FluteTeacher.set_scale() -> FingeringError')
            raise FingeringError

    def set_base_note(self, letter, alteration):
        _scale_mgr_tmp = copy(self._scale_manager)
        _scale_mgr_tmp.set_basenote(letter, alteration)
        _arpeggiator_tmp = copy(self._arpeggiator)
        _arpeggiator_tmp.set_scale_manager(_scale_mgr_tmp)

        if Fingerings.check_notes(_arpeggiator_tmp.get_notes()):
            self._scale_manager = _scale_mgr_tmp
            self._arpeggiator = _arpeggiator_tmp
            self.next_note()
        else:
            print('FluteTeacher.set_base_note() -> FingeringError')
            raise FingeringError

    def set_start_octave(self, start_octave=4):
        _scale_mgr_tmp = copy(self._scale_manager)
        _scale_mgr_tmp.set_octave(start_octave)
        _arpeggiator_tmp = copy(self._arpeggiator)
        _arpeggiator_tmp.set_scale_manager(_scale_mgr_tmp)

        if Fingerings.check_notes(_arpeggiator_tmp.get_notes()):
            self._scale_manager = _scale_mgr_tmp
            self._arpeggiator = _arpeggiator_tmp
            self.next_note()
        else:
            print('FluteTeacher.set_start_octave() -> FingeringError')
            raise FingeringError

    def set_arpeggiator(self, kind, n_octaves):
        _arpeggiator_tmp = Arpeggiator(self._scale_manager, kind, n_octaves)

        if Fingerings.check_notes(_arpeggiator_tmp.get_notes()):
            self._arpeggiator = _arpeggiator_tmp
            self.next_note()
        else:
            print('FluteTeacher.set_arpeggiator() -> FingeringError')
            raise FingeringError

    def set_fingering_display_mode(self, mode, delay):
        self._main_window.fingering.set_display_mode(mode, delay)

    def set_fingering_key_color(self, color):
        self.fingering.set_fingering_key_color(color)

    def set_fingering_delay_color(self, color):
        self.fingering.set_fingering_delay_color(color)
