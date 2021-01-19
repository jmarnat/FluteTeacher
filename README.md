# FluteTeacher
Since I'm cheap and nerdy, I've made myself an Artificial Flute Teacher!

Here is an animated GIF of the actual version running:
![Animation](doc_res/animation-v0.7-test2.gif?raw=true)

## To-do list (by decreasing priority):
### Fingerings:
- [ ] Split classes to:
  - Fingerings (= controls, ...)
  - FingeringsWidget
### Timer:
- [ ] Add a practicing timer??
### Staffs:
- [ ] add view choices : single / continuous
  - [ ] add corresponding GUI option
### Help popup:
- [ ] Make a Help popup window explaining How To
- [ ] Add corresponding MenuBar item
### Tuner:
- [ ] Add a tuner in HearAI
- [ ] Add the tuner in GUI
- [ ] Add the option in the menubar
- [ ] add tuning setting
- [ ] set tuning in menubar
  - Standard: 440 Hz
  - Baroque: 415 Hz
  - Berlin Philharmonic: 442 Hz
  - (ref: https://en.wikipedia.org/wiki/Concert_pitch)
### General GUI:
- [ ] "About" window for copyright + website
- [ ] add French translation
- [ ] Display mode:
  - [ ] single note
  - [ ] sheet music
- ( ) HearAI: continuous listening but take the last 200ms? in order to update more quickly and accurately
- [ ] Add Listening option :
  - [ ] play midi sound if available ? -> or pre-recorded sound ?
  - [ ] either single note
  - [ ] or the full scale
- [ ] Add proper quit function
- [ ] Add 'bécarre'
### For compilation:
- [ ] check requirements
- [ ] compile on MacOS
- [ ] compile on Windows 10
### Maybe:
- [ ] adding register information + draw ?
- [ ] encapsulate in a specific window
- [ ] better drawings?
- [ ] for multiple notes: better auto placement (100px + proportion?)

## Version History:
### v0.7
- Default Settings (in class, see later for a configuration file maybe):
  - Take Settings Class's values in account in the MenuBar
- General GUI:
  - When selecting scale / octave / arp in the MenuBar, display warning if not playable &rarr; this was finally pretty complex!
  - Added CSS on for buttons + hovers, pretty nice!
  - Added colors selection for fingerings, including:
    - key pressed: black or blue,
    - delayed keys: grays or rainbow yeah.

### v0.6
- Fingering:
  - Treating multiple fingering possibilities
  - add color for optional fingers
  - show 2 fingerings delays when appropriate
  - when no fingering: show grayed
- Staffs:
  - Added white background + rounded corners
- Arpeggiator:
  -  Thirds Up/Down

### v0.5
- Starting note and octave:
  - Changed to `Start from note` -> `Octave` -> `Note`
- Scale and Modes:
  - Modes available only from Major, Minor harmonic and Minor melodic scales
  - MenuBar integration -> look alright 
  - added harmonic-minor scales
  - added melodic-minor scales
  - added pentatonics
- Arpeggiator:
  - Treating random as random choice over current scale

### v0.4:
- Scales:
  - Whole-tone scale + mode
  - Splitting ScaleManager and Arpeggiator processes
- Staffs:
  - Removed Blinking causing bugs -> single green note now
- Arpeggiator:
  - For each: add 1 oct / 2 oct
  - Added "start at octave no 4/5/6" menu 
- Menubar:
  - add Arpeggiators
  - check current scale / octave / arp
  - training mode selection
  - Random note from scale (deleting difficulty 'cause choosing scale)
- Fingerings: 
  - add following options :
    - constant help
    - fingering (after X secs)
    - disabled
- General GUI:
  - buttons: set fixed height + change look?


### v0.3:
- Scales:
  - True scale generator (with intervals)
  - Adding minor scales
  - Mode computing
  - computed: Major / Minor
- MenuBar:
  - Empty menu bar

### v0.2:
- Internal ("hard coded") options:
  - add "practice mode" selection
  - change "normal mode" to "random notes"
  - add "scale and modes practice" :

### v0.1:
- GUI:
  - Main window creation with 3 rows
  - `next` (note) button
  - upper-left staff draw
  - upper-left note respondive draw
  - upper right basic draw
  - fingering draw
- Notes:
  - note correspondance between text / drawn / A4-indexed
  - add sharp and flat symbols
  - corresp note number -> correct true note
- HearAI (note recognition module):
  - note recognition based on FFT &rarr;
  - HearAI: continuous listening
  - on HearAI: no note if SNR < threshold &rarr; set with volume only
  - recognized note display
  - automatic note validation
