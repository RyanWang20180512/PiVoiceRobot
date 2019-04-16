# -*- coding: utf-8 -*-
from configparser import ConfigParser
from aip import AipSpeech
import os
import urllib3

class BaiduAipSpeech:
    '''
    Use baidu aip api to do speech recognition and synthesis
    '''
    def __init__(self):
        cp=ConfigParser()
        cp.read('./Configs/baiduAipApp.cfg')
        #print(len(cp.sections()))
        section=cp.sections()[0]
        self._APP_ID=cp.get(section,'APP_ID')
        self._API_KEY=cp.get(section,'API_KEY')
        self._SECRET_KEY=cp.get(section,'SECRET_KEY')
        self._VOL=cp.get(section,'VOL')
        self._PER=cp.get(section,'PER')
        self._client=AipSpeech(self._APP_ID,self._API_KEY,self._SECRET_KEY)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def get_file_content(self,filePath):
        with open(filePath,'rb') as fp:
            return fp.read()

    def speechRecognition(self,input_file):
        '''
        Input a pcm file, return the recognition result
        '''
        if input_file.endswith('.pcm') is not True:
            raise Exception('Input file is not a pcm file!')
        response=self._client.asr(self.get_file_content(input_file),'pcm',16000,{'dev_pid':1536})
        #if response['err_no']=='0':
        #    raise Exception(response['err_msg'])
        if ('result' in response.keys()) is False:
            return None
        return response['result'][0]

    def speechSynthesis(self,input_sentense,output_path):
        '''
        Input the sentense, return the synthesis result
        '''
        if output_path.endswith('.wav') is not True:
            raise Exception('Output format should be .mp3')
        result=self._client.synthesis(input_sentense,'zh',1,{'vol':self._VOL,'per':self._PER,'aue':6})
        if not isinstance(result,dict):
            with open(output_path,'wb') as f:
                f.write(result)
        else:
            raise Exception(result['err_msg'])

