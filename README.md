# FluteTeacher
Since I'm cheap and nerdy, I've made myself an Artificial Flute Teacher!

Here is a screenshot of the actual version:
![Screen1](doc_res/screen2.png)

## To-do list:
### Tuner:
- [ ] Add a tuner in HearAI
- [ ] Add the tuner in GUI
- [ ] Add the option in the menubar
### Staffs:
- [ ] add view choices : single / continuous
- [ ] add corresponding GUI option
### Fingering:
- [ ] add color for optional fingers 
- [ ] How to treat multiple fingering possibilities ?? (ex: A#4)
### Arpeggiator:
- [ ] THIRDS_UP_DOWN
- [ ] Treat random as random choice over current scale
- [ ] Add note 1 / nnotes for arpeggiator?
### General GUI:
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
### v0.5
- Starting note and octave:
- Change to `Start from note` -> `Octave` -> `Note`
- Scale and Modes
  - Make modes only from Major, Minor harmonic and Minor melodic scales
  - MenuBar integration -> look alright 
- Scales:
  - add harmonic-minor scales
  - add melodic-minor scales
  - add pentatonics

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
