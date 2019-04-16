import pyaudio
import os
import sys
import time
import wave
import numpy as np
import pandas as pd
#os.close(sys.stderr.fileno())

WIDTH=2
CHANNELS=1
RATE=44100
CHUNK=1024
RECORD_SECONDS=5
WAVE_OUTPUT_FILENAME='output2.wav'
frames=[]
voice_bytes=[]
index=0
wf=None

p=pyaudio.PyAudio()


def callback(in_data,frame_count,time_info,status):
    global index
    global wf
    if index==0:
        print('recording...')
        print(len(in_data))
        print(type(in_data))
    frames.append(in_data)
    #print('mean value : %f' % np.mean(np.frombuffer(in_data,dtype=np.short)))
    p=np.frombuffer(in_data,dtype=np.short)
    print('std value : %f' % np.std(np.frombuffer(in_data,dtype=np.short)))
    voice_bytes.extend(p)
    index=index+1
    if index==int(RATE/frame_count*RECORD_SECONDS):
        print('done')
        print(len(voice_bytes))
        d=pd.DataFrame(voice_bytes)
        d.to_csv('voice_test2.csv')
        #d=np.frombuffer(in_data,dtype=np.short)
        #print(d)
        #print(d.shape)
        wf=wave.open(WAVE_OUTPUT_FILENAME,'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(WIDTH)
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        wf=wave.open(WAVE_OUTPUT_FILENAME,'rb')


        #return (None,pyaudio.paComplete)
    if index>int(RATE/frame_count*RECORD_SECONDS):
        data=wf.readframes(frame_count)
        if len(data)>0:
            return (data,pyaudio.paContinue)
        else:
            wf.close()
            return (data,pyaudio.paComplete)
    return (bytes(len(in_data)),pyaudio.paContinue)

stream=p.open(format=p.get_format_from_width(WIDTH),
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=True,
        stream_callback=callback)

stream.start_stream()

while stream.is_active():
    pass
    time.sleep(0.1)

stream.stop_stream()
stream.close()

p.terminate()
