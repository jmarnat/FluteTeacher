from src.Note import Note


class Bar:
    def __init__(self, beats_number=4, beat_unit=4, notes_and_rests=()):
        """
        :param beats_number: number of beats in the bar
        :param beat_unit: 4 = quarter note, 8 = eighth, ...
        :param notes_and_rests: list of notes and rests
        """
        self._nbeats = beats_number
        self._beat_unit = beat_unit
        self._notes_and_rests = notes_and_rests

    def check_bar(self):
        return (self._nbeats / self._beat_unit) == sum([n.length() for n in self._notes_and_rests])

    def __str__(self):
        _t = "Bar({}/{}) : [".format(self._nbeats, self._beat_unit)
        for note in self._notes_and_rests:
            _t += "\n    {}".format(note)
        return _t
