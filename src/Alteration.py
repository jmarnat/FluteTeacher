
class Alteration:
    __alt_corresp__ = {'bb': -2, 'b': -1, '': 0, ' ': 0, '#': +1, '##': +2}

    def __init__(self, semitones=None, alt_str=None):
        if semitones is not None:
            self._alt = semitones
        elif alt_str is not None:
            self._alt = Alteration.__alt_corresp__[alt_str]
        else:
            print('ERROR: no semitone or alt_str!')

    def value(self):
        return self._alt

    def to_str(self):
        return str(self)

    def __str__(self):
        return {-2: 'bb', -1: 'b', 0: '', 1: '#', 2: '##'}[self._alt]


class Alterations:
    SHARP = Alteration(semitones=1)
    DOUBLE_SHARP = Alteration(semitones=2)
    NATURAL = Alteration(semitones=0)
    FLAT = Alteration(semitones=-1)
    DOUBLE_FLAT = Alteration(semitones=-2)
