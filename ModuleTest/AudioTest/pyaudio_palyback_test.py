import pyaudio
import os
import sys

os.close(sys.stderr.fileno())

CHUNK=1024
WIDTH=2
CHANNELS=2
RATE=44100
RECORD_SECONDS=10

p=pyaudio.PyAudio()

stream=p.open(format=p.get_format_from_width(WIDTH),
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK)

print('recording...')

for i in range(0,int(RATE/CHUNK*RECORD_SECONDS)):
    data=stream.read(CHUNK)
    stream.write(data,CHUNK)

print('done...')

stream.stop_stream()
stream.close()

p.terminate()


