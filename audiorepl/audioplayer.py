from time import sleep
import numpy as np
from bufferbabysitter import BufferBabysitter
import pyximport

pyximport.install()
from play import start, stop, usecs, put, cancel_all


class AudioPlayer(object):
    def __init__(self):
        super(AudioPlayer, self).__init__()
        self._started = False

    def __enter__(self):
        self.start_audio_engine()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_audio_engine()

    def __del__(self):
        self.stop_audio_engine()

    def start_audio_engine(self):
        if self._started:
            return
        start()
        self._started = True
        sleep(1)

    def stop_audio_engine(self):
        if not self._started:
            return
        stop()
        self._started = False

    def shush(self):
        """
        Stop all currently playing audio, and cancel any scheduled audio
        """
        cancel_all()

    def _block(self, bb):
        """
        block until the audio is done playing, unless a KeyboardInterrupt
        is received first
        """
        try:
            while bb.is_alive():
                bb.join(5)
        except KeyboardInterrupt:
            bb._should_stop = True
            self.shush()

    def play(self, audio, block=True):
        if audio.dtype != np.float32:
            audio = audio.astype(np.float32)
        self.start_audio_engine()
        bb = BufferBabysitter(audio)
        bb.start()
        fade = np.linspace(0, 1, 10)
        audio[:10] *= fade
        audio[-10:] *= fade[::-1]
        put(audio, 0, len(audio), usecs() + 1e4)

        if block:
            self._block(bb)
