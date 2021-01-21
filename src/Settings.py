from src.Arpeggiator import *
from src.Alteration import *


class Settings:
    # Starting mode, either 'SheetMusic' or 'SingleNote'
    # START_IN_MODE = 'SheetMusic'
    START_IN_MODE = 'SingleNote'

    # ------------------ LISTENING AND AUTONEXT AT STARTUP ------------------- #
    START_LISTENING_AT_STARTUP = False
    START_AUTONEXT_AT_STARTUP = False

    # ---------------------------- DEFAULT SCALE ----------------------------- #
    DEFAULT_SCALE_NAME = 'Major'
    DEFAULT_SCALE_MODE = 1

    # ------------------------- DEFAULT ARPEGGIATOR -------------------------- #
    DEFAULT_ARPEGGIATOR_KIND = Arpeggiator.UP
    DEFAULT_ARP_N_OCTAVES = 1

    # -------------------------- DEFAULT BASE NOTE --------------------------- #
    DEFAULT_BASE_NOTE_LETTER = 'C'
    DEFAULT_BASE_NOTE_ALTERATION = Alterations.NATURAL
    DEFAULT_BASE_NOTE_OCTAVE = 4

    # -------------------------- FINGERING SETTINGS -------------------------- #
    FINGERINGS_DELAYS = [0.5, 1, 2, 3, 4, 5, 10]

    #
    TRANSPOSE_INPUT = 0

    # ----------------------------- MAIN APP CSS ----------------------------- #
    MAIN_APP_STYLE_SHEET = """
        QPushButton {
            border-radius: 8px;
            color: #fff;
            font-size: 20pt;
            font-family: "Avenir Next";
            background-color: #64b5f6;
        }
    
        QPushButton:hover {
            background-color: #6e93d6;
        }
    
        QPushButton:focus {
            border: 2px solid #6e93d6;
        }
    """
