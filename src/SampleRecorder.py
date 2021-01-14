import pyaudio
import wave
import sys
import numpy as np

from scipy.fft import fft


class SampleRecorder:
    def __init__(self,
                 rate=44100,
                 chunk=1024,
                 channels=1):
        self._rate = rate
        self._chunk = chunk
        self._channels = channels
        self._audio_format = pyaudio.paInt16

        self._pyaudio = pyaudio.PyAudio()
        self._stream = self._pyaudio.open(format=self._audio_format,
                                          channels=channels,
                                          rate=rate,
                                          input=True,
                                          frames_per_buffer=chunk)
        self._stream.stop_stream()
        self._last_frames = None

        self._notes = ['A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D',
                       'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab']

        self._notes_freqs = {}
        for i in range(-48, 48):
            bound_l = 440 * (2 ** ((i - 0.5) / 12))
            bound_r = 440 * (2 ** ((i + 0.5) / 12))
            self._notes_freqs[i] = (bound_l, bound_r)

    def record(self, millis=200):
        # length_secs = ((millis + 10) / 1000)
        length_secs = millis / 1000
        self._stream.start_stream()
        self._last_frames = []
        nb_chunks = int(length_secs * (self._rate / self._chunk))
        for i in range(nb_chunks):
            data = self._stream.read(self._chunk)
            self._last_frames.append(data)
        self._stream.stop_stream()

        return  # self._last_frames.copy()

    def last_rec(self):
        if not self._last_frames:
            print('ERROR: please record first', file=sys.stderr)
            return None
        return np.frombuffer(b''.join(self._last_frames), np.int16)

    def last_rec_f0(self):
        full_sample = self.last_rec()
        q1 = len(full_sample) // 4
        q3 = 3 * q1
        sample = full_sample[q1:q3]
        n_samples = len(sample)
        sample_duration = 1 / self._rate
        res_fft_bis = fft(sample)
        res_fft = np.abs(res_fft_bis[:n_samples // 2])
        f0 = np.argmax(res_fft) / (n_samples * sample_duration)
        return f0

    def _note_fullname(self, note):
        return "{} {}".format(self._notes[note % 12], ((note // 12) + 4))

    def _get_note(self, f0):
        for note, (left, right) in self._notes_freqs.items():
            if left <= f0 < right:
                return note
        return None

    def get_last_note(self):
        """
            (f0, note, name) with:
            f0:   FFT main frequency
            note: corresponding note if found (with respect to A4=440Hz)
            name: name of the note

        """
        f0 = self.last_rec_f0()
        if f0 is None:
            return None

        note = self._get_note(f0)
        if note is None:
            return f0, None, None

        name = self._note_fullname(note)
        if name is None:
            return f0, note, None

        return f0, note, name

    # def save(self, path):
    #     if not path.lower().endswith('.wav'):
    #         print('ERROR: file extension should be .wav', file=sys.stderr)
    #         return None
    #     wf = wave.open(path, 'wb')
    #     wf.setnchannels(self._channels)
    #     wf.setsampwidth(p.get_sample_size(self._audio_format))
    #     wf.setframerate(self._rate)
    #     wf.writeframes(b''.join(self._last_frames))
    #     wf.close()

    # def plot(self, figsize=(20, 4)):
    #     fig, ax = plt.subplots(figsize=figsize)
    #     rec16 = self.last_rec()
    #     ax.plot(rec16)

    def close(self):
        self._stream.close()
        self._pyaudio.terminate()
