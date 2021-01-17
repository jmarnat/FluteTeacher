# FluteTeacher
Since I'm cheap and nerdy, I've made myself an Artificial Flute Teacher!

Here is a screenshot of the actual version:
![Screen1](doc_res/screen2.png)

## To-do list:
### Tuner:
- [ ] Add a tuner in HearAI
- [ ] Add the tuner in GUI
- [ ] Add the option in the menubar
### MenuBar:
- [x] add Arpeggiators
- [ ] check current scale / octave / arp
- [ ] training mode selection -> arp nan ?
- [ ] Modes
- [ ] Random note from scale + difficulty
### Scales:
- [ ] add harmonic-minor scales
- [ ] add melodic-minor scales
### Staffs:
- [ ] add view choices : single / continuous
- [ ] add corresponding GUI option
### Fingering:
- [ ] add color for optional fingers 
- [ ] How to treat multiple fingering possibilities ?? (ex: A#4)
- [x] add following options :
  - [x] constant help
  - [x] fingering (after X secs)
  - [x] disabled
### Arpeggiator:
- [ ] THIRDS_UP_DOWN
- [ ] Treat random as random choice over current scale
- [ ] Add note 1 / nnotes for arpeggiator?
### General GUI:
- [x] buttons: set fixed height + change look?
- [ ] "About" window for copyright + website
- [ ] add French translation
- [ ] Display mode:
  - [ ] single note
  - [ ] sheet music
- [ ] HearAI: continuous listening but take the last 200ms? in order to update more quickly and accurately
- [ ] Add Listening option :
  - [ ] play midi sound if available ? -> or pre-recorded sound ?
  - [ ] either single note
  - [ ] or the full scale
- [ ] Add proper close function
- [ ] Add 'bécarre'

### For compilation:
- [ ] check requirements
- [ ] compile on MacOS
- [ ] compile on Windows 10

### Maybe:
- [ ] adding register information + draw ?
- [ ] encapsulate in a specific window
- [ ] add tuning setting
- [ ] better drawings?
- [ ] for multiple notes: better auto placement (100px + proportion?)

## Version History:
### v0.4:
- Removed Blinking causing bugs
- Whole-tone scale + mode
- Splitting ScaleManager and Arpeggiator processes
- Arpeggiator:
  - For each: add 1 oct / 2 oct
  - Added "start at octave no 4/5/6" menu 


### v0.3:
- True scale generator (with intervals)
- Adding minor scales
- Mode computing
- Empty menu bar
- Scales : Major / Minor

### v0.2:
- add "practice mode" selection
- change "normal mode" to "random notes"
- add "scale and modes practice" :

### v0.1:
- Main window creation with 3 rows
- `next` (note) button
- upper-left staff draw
- upper-left note respondive draw
- note correspondance between text / drawn / A4-indexed
- add sharp and flat symbols
- corresp note number -> correct true note
- upper right basic draw
- flute draw
- note recognition based on FFT &rarr;
- HearAI: continuous listening
- on HearAI: no note if SNR < threshold &rarr; set with volume only
- recognized note display
- automatic note validation
