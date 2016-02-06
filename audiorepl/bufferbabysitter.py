from threading import Thread
from time import sleep


class BufferBabysitter(Thread):
    """
    This class is for internal use only.  This class solves the problem, albeit
    in a bit of a klunky way, of passing numpy arrays (which are subject to
    garbage collection) into my JACK event queue.  If no reference to the
    numpy array of audio samples exists in python code, it's likely that the
    array will be garbage collected before, or during the time the audio is
    playing. C code will then attempt to access the memory, and a segfault
    will occur. This class is meant to solve the problem of one-off previews
    of audio, e.g.
    """

    def __init__(self, buf):
        super(BufferBabysitter, self).__init__()
        self._buf = buf
        self.daemon = True
        # BUG: This only works for 44.1Khz. How do I know what samplerate the
        # buffer is?
        self._seconds = len(buf) / 44100.
        self._pos = 0
        self._should_stop = False

    def run(self):
        while self._pos < self._seconds and not self._should_stop:
            sleep(.5)
            self._pos += .5

        self.cleanup()

    def cleanup(self):
        del self._buf