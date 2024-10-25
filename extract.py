import wave
import array
import matplotlib.pyplot as plt
import numpy as np

with wave.open("c:/tmp/Thunder Track.wav") as wav_file:
    metadata = wav_file.getparams()
    print(metadata)
    frames = wav_file.readframes(metadata.nframes)
    # Convert bytes to 16-bit short integers
    pcm_samples = array.array("h", frames)

    # Compute duration in minutes
    print((len(pcm_samples) / metadata.framerate) / 60)

    # Compute moving average
    a = np.int32(np.array(pcm_samples))
    # Millisecond window
    average_window = int(44100 / 100)
    a_avg = np.convolve(np.square(a), np.ones(average_window), 'valid') / average_window

    # Find the loud parts
    
    plt.plot(a_avg)
    plt.show()