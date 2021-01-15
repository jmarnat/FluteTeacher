
class Scale:
    SCALES = {
        'C Major': 'C3,D3,E3,F3,G3,A3,B3',
        'D Major': 'D3,E3,F#3,G3,A3,B3,C#4',
        'E Major': 'E3,F#3,G#3,A3,B3,C#4,D#4',
        'F Major': 'F3,G3,A3,Bb3,C4,D4,E4'
    }

    _NOTES_NAMES = {
        '#': ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#'],
        'b': ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
    }

    def compute(self, scale_name):
        if not (scale_name in Scale.SCALES):
            return None
        scale_notes_str = Scale.SCALES[scale_name].split(',')
        notes = []
        for note_str in scale_notes_str:
            octave = int(note_str[-1])

        return
