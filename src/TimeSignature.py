from src.NotesAndRests import Note


class TimeSignature:
    def __init__(self, beats, beat_length):
        self._nbeats = beats
        self._blen = beat_length

    def get_nbeats(self):
        return self._nbeats

    def groups(self):
        if (self._nbeats, self._blen) == (4, 4):
            return (Note.QUARTER_NOTE,
                    Note.QUARTER_NOTE,
                    Note.QUARTER_NOTE,
                    Note.QUARTER_NOTE)
        elif (self._nbeats, self._blen) == (4, 4):
            return (Note.QUARTER_NOTE,
                    Note.QUARTER_NOTE,
                    Note.QUARTER_NOTE)
        else:
            print('TimeSignature Error')


class TimeSignatures:
    TS_4_4 = TimeSignature(4, Note.QUARTER_NOTE)
    TS_3_4 = TimeSignature(3, Note.QUARTER_NOTE)
    # TS_12_8 = TimeSignature(12, Note.QUARTER_NOTE)
