# -*- coding: UTF-8 -*-

import pyaudio
import os
import sys
import time
import wave
import numpy as np
import pandas as pd
from enum import Enum
from FormatConvertModule import FormatConvert
from StopWatchModule.StopWatch import StopWatch
from BaiduAipModule.BaiduAip import BaiduAipSpeech
from TuringRobotModule.TuringRobot import TuringRobot
from configparser import ConfigParser
#os.close(sys.stderr.fileno())
from MatrixLedModule.Matrix_Led import Matrix_Led

cp=ConfigParser()
cp.read('./Configs/MainApp.cfg')
section=cp.sections()[0]
WIDTH=int(cp.get(section,'WIDTH'))
CHANNELS=int(cp.get(section,'CHANNELS'))
RATE=int(cp.get(section,'RATE'))
CHUNK=int(cp.get(section,'CHUNK'))
RECORD_MAX_SECONDS=int(cp.get(section,'RECORD_MAX_SECONDS'))
#RECORD_WAVE_PATH=cp.get(section,'RECORD_WAVE_PATH')
#RESPONSE_MP3_PATH=cp.get(section,'RESPONSE_MP3_PATH')
RESPONSE_WAVE_PATH=cp.get(section,'RESPONSE_WAVE_PATH')
RECORD_PCM_PATH=cp.get(section,'RECORD_PCM_PATH')
VOICE_STD_THRESHOLD=int(cp.get(section,'VOICE_STD_THRESHOLD'))




class AudioState(Enum):
    '''标记音频操作当前的状态'''
    LISTENING=1 #监听状态
    RECORDING=2
    PLAYING=3 #播放状态

def getStdOfVoiceFrame(in_data):
    '''获取一帧音频信号的标准差'''
    return np.std(np.frombuffer(in_data,dtype=np.short))

frames=[]
wf=None
stopWatch_Record=None #用于存储录音时长
baiduAip=BaiduAipSpeech()
turingRobot=TuringRobot()
p=pyaudio.PyAudio()
audioState=AudioState.LISTENING
matrixLed=Matrix_Led(2,90,0)
matrixLed.setScrollChar(27)

def handleVoice(frames):
    '''处理接收到的声音信息'''
    global baiduAip
    np.array(frames).tofile(RECORD_PCM_PATH) #先保存为pcm格式
    question=baiduAip.speechRecognition(RECORD_PCM_PATH) #获取文字 
    if question is None:
        question=''
    print('Ask a question : %s' % question)
    answer=turingRobot.getResponse(question) #获取回应
    print('Answer : %s' % answer)
    baiduAip.speechSynthesis(answer,RESPONSE_WAVE_PATH) #获取应答
    #FormatConvert.Mp3ToWav(RESPONSE_MP3_PATH,RESPONSE_WAVE_PATH) #转成wav格式
    #np.array(response).tofile(RESPONSE_WAVE_PATH)


def callback(in_data,frame_count,time_info,status):
    global audioState
    global frames
    global stopWatch_Record
    global wf


    #如果当前帧的std大于阈值且处于监听状态，开始录音
    if audioState==AudioState.LISTENING and getStdOfVoiceFrame(in_data)>=VOICE_STD_THRESHOLD:
        matrixLed.scrollingChar()
        #print(getStdOfVoiceFrame(in_data))
        stopWatch_Record=StopWatch()
        print('Recording...')
        frames.append(in_data)
        audioState=AudioState.RECORDING #当前处于RECORDING状态
        return (bytes(len(in_data)),pyaudio.paContinue) #如果不是播放状态，应该输入空的数据流
        
    #如果当前处于RECORDING状态
    if audioState==AudioState.RECORDING:
        matrixLed.scrollingChar()
        t0=stopWatch_Record.getSeconds()
        frames.append(in_data)
        #如果录音时长已经超过限定，停止录音，保存音频文件
        if t0>RECORD_MAX_SECONDS:
            print('Done!')
            handleVoice(frames)
            wf=wave.open(RESPONSE_WAVE_PATH,'rb')
            audioState=AudioState.PLAYING #PLAYING状态
            matrixLed.setBrightChar(1)
            frames=[]
            return (bytes(len(in_data)),pyaudio.paContinue) 
    if audioState==AudioState.PLAYING:
        matrixLed.brightChar()
        data=wf.readframes(frame_count)
        if len(data)/WIDTH >= frame_count:
            return (data,pyaudio.paContinue)
        else:
            print('stop playing')
            wf.close()
            audioState=AudioState.LISTENING
            matrixLed.setScrollChar(27)
            return (data,pyaudio.paComplete)
    matrixLed.scrollingChar()
    return (bytes(len(in_data)),pyaudio.paContinue)


stream=p.open(format=p.get_format_from_width(WIDTH),
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=True,
        stream_callback=callback)

stream.start_stream()
print('Listening...')
try:
    while True:
        while stream.is_active():
            pass
        stream.stop_stream()
        stream.close()
        stream=p.open(format=p.get_format_from_width(WIDTH),
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=True,
            stream_callback=callback)
        stream.start_stream()
        print('Listening...')
except Exception as e:
    stream.stop_stream()
    stream.close()
    p.terminate()
    raise e
