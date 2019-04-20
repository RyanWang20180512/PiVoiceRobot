# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 19:41:06 2019

@author: wzy11
"""

import requests
import json
from configparser import ConfigParser

class TuringRobot:
    '''
    Use turing robot aip to get response
    '''
    def __init__(self):
        cp=ConfigParser()
        cp.read('/home/pi/VoiceRobot/Configs/turingRobotApp.cfg')
        section=cp.sections()[0]
        self._URL=cp.get(section,'URL')
        self._API_KEY=cp.get(section,'API_KEY')
        self._USER_ID=cp.get(section,'USER_ID')
        
    def getResponse(self,question):
        params={
        'reqType':0,
        'perception':{
                    'inputText':{
                            'text':''
                    }
                },
        'userInfo':{
                'apiKey':self._API_KEY,
                'userId':self._USER_ID
            }
        }
        params['perception']['inputText']['text']=question
        response=requests.post(self._URL,json=params)
        answer=json.loads(response.text)
        if 'results' in answer.keys():
            return answer['results'][0]['values']['text']
        else:
            raise Exception(answer['intent']['code'])
