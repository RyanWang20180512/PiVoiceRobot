import ffmpy3
ff=ffmpy3.FFmpeg(inputs={'output.wav':'-y'},outputs={'output_pcm.pcm':'-f s16le -ac 1 -ar 16000'})
ff.run()
