# AudioRepl
`audiorepl` is a python module written to play audio interactively in the repl, but could be embedded in any program that needs to play audio.

## Interactive Repl Session
```python
>>> import audiorepl
>>> import numpy as np
>>> player = audiorepl.AudioPlayer()
>>> player.start_audio_engine()
>>> samples = np.random.random_sample(44100 * 2)
>>> player.play(samples) # you should hear two seconds of white noise
>>> player.stop_audio_engine()
```

## Embedded in a Program as a Context Manager
```python
import audiorepl
import numpy as np

samples = np.random.random_sample(44100 * 2)
with audiorepl.AudioPlayer() as player:
    player.play(samples)
```
