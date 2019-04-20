import ffmpy3
ff=ffmpy3.FFmpeg(inputs={'output_pcm.pcm':'-y -f s16le -ac 1 -ar 1600'},outputs={'output_wav.wav':'-ac 2 -ar 44100'})
ff.run()
