from src.NotesAndRests import Note


class Bar:
    def __init__(self, beats_number=4, beat_unit=Note.WHOLE_NOTE, notes_and_rests=None):
        """
        :param beats_number: number of beats in the bar
        :param beat_unit: 1/4 = quarter note, 1/8 = eighth, ...
        :param notes_and_rests: list of notes and rests
        """
        self._nbeats = beats_number
        self._beat_unit = beat_unit
        self._pos_frac = 0
        if notes_and_rests:
            self._notes_and_rests = notes_and_rests
        else:
            self._notes_and_rests = []

    def set_cursor(self, pos_frac):
        self._pos_frac = pos_frac

    def get_cursor(self):
        return self._pos_frac

    def check_bar(self):
        return int(self._nbeats * self._beat_unit) == sum([n.length() for n in self._notes_and_rests])

    def add_note(self, note):
        self._notes_and_rests.append(note)

    def add_rest(self, rest):
        self._notes_and_rests.append(rest)

    def get_notes_and_rests(self):
        return self._notes_and_rests

    def get_time_signature(self):
        return self._nbeats, self._beat_unit

    def get_note(self, pos):
        return self._notes_and_rests[pos]

    def __str__(self):
        _t = "Bar({}/{}) : [".format(self._nbeats, self._beat_unit)
        for note in self._notes_and_rests:
            _t += "\n    {}".format(note)
        return _t
