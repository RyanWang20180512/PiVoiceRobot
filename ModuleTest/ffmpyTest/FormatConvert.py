from ffmpy3 import FFmpeg

'''
Use ffmpy3 to convert .wav to .pcm, or .mp3 to .wav
'''
def WavToPcm(input_path,output_path):
    if input_path.endswith('.wav') is not True:
        raise Exception('Input is not wav file!')
    if output_path.endswith('.pcm') is not True:
        raise Exception('Output is not pcm file')
    ff=FFmpeg(inputs={input_path:'-y'},
              outputs={output_path:'-f s16le -ac 1 -ar 16000'})
    ff.run()

def Mp3ToWav(input_path,output_path):
    if input_path.endswith('.mp3') is not True:
        raise Exception('Input is not mp3 file!')
    if output_path.endswith('.wav') is not True:
        raise Exception('Output is not wav file!')
    ff=FFmpeg(inputs={input_path:'-y'},
              outputs={output_path:None})
    ff.run()
