from __future__ import division #to avoid division truncation
import math
import pyaudio
import sys

PyAudio = pyaudio.PyAudio

RATE = 16000 #number of frames per second/frameset.      

def play_freq(freq_list, length_list):
	#to avoid segfault during following loop
	num_notes = len(freq_list) if len(freq_list) < len(length_list) else len(length_list)

	for i in range(num_notes):
		freq = freq_list[i] #freq to play
		length =  length_list[i] #seconds to play sound

		num_frames = int(RATE * length)
		rest_frame = num_frames % RATE
		WAVEDATA = ''    

		#127 is max volume, add 128 to stay in frame range
		for x in xrange(num_frames):
			WAVEDATA = WAVEDATA+chr(int(math.sin(x/((RATE/freq)/(2*math.pi)))*60+128))    

		#fill remainder of frameset with silence
		for x in xrange(rest_frame): 
			WAVEDATA = WAVEDATA+chr(128)

		p = PyAudio()
		stream = p.open(format = p.get_format_from_width(1), 
		                channels = 1, 
		                rate = RATE, 
		                output = True)
		stream.write(WAVEDATA)
		
	stream.stop_stream()
	stream.close()
	p.terminate()

play_freq([261.63, 440],[2,1])