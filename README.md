# FluteTeacher
Since I'm cheap and nerdy, I've made myself an Artificial Flute Teacher!

Here is a screenshot of the actual version:
![Screen1](doc_res/screen2.png)

## To-do list:
### Sure:
- [ ] training mode selection:
  - [ ] Modes
  - [ ] Random + difficulty
- [ ] Arp THIRDS_UP_DOWN
- [ ] "About" window for copyright + website
- [ ] add "start at octave" menu 
- [ ] add French translation
- [ ] finish notes
- [ ] add harmonic-minor scales
- [ ] add melodic-minor scales 

### For compilation:
- [ ] check requirements
- [ ] compile on MacOS
- [ ] compile on Windows 10

### Maybe:
- [ ] adding register information + draw ?
- [ ] encapsulate in a specific window
- [ ] add tuning setting
- [ ] add visual tuner
- [ ] better drawings?
- [ ] for multiple notes: better auto placement (100px + proportion?)

## Version History:
### v0.4:
- Whole-tone scale + mode

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
