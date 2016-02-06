import pyximport
pyximport.install()
from play import start, stop, usecs, put, cancel_all
from audioplayer import AudioPlayer