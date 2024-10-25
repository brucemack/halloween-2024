import pyaudio
import wave
import array 
import numpy as np 
import serial

serial_port_name = "COM10"
#filename = 'c:/tmp/Thunder Track.wav'
filename = 'assets/Thunder Track.wav'
# Each chunk is ten milliseconds
chunk_size = int(44100 / 100)

# Open the serial port
#serial_port = serial.Serial(serial_port_name) 

# Build the rolling average
with wave.open(filename) as wav_file:
    metadata = wav_file.getparams()
    print(metadata)
    frames = wav_file.readframes(metadata.nframes)
    # Convert bytes to 16-bit short integers
    pcm_samples = array.array("h", frames)
    # Compute moving average
    a = np.int32(np.array(pcm_samples))
    a_avg = np.convolve(np.square(a), np.ones(chunk_size), 'valid') / chunk_size

#wav_file.close()

# Create an interface to PortAudio
p = pyaudio.PyAudio()

while True:

    # Open the sound file 
    wf = wave.open(filename, 'rb')

    # Open a .Stream object to write the WAV file to
    # 'output = True' indicates that the sound will be played rather than recorded
    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    # Read data in chunks
    data = wf.readframes(chunk_size)

    # Play the sound by writing the audio data to the stream
    c = 0
    while len(data) != 0:
        # Find the maximum amplitude in the chunk
        chunk = a_avg[c:c+ chunk_size]
        chunk_max = int(np.max(chunk))
        # Look for trigger
        if chunk_max > 0.5e8:
            print("Flash")
        stream.write(data)
        data = wf.readframes(chunk_size)
        c = c + chunk_size
        #print(c)

    # Close and terminate the stream
    print("Closing")
    stream.close()
    wf.close()

p.terminate()
