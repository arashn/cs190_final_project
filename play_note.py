from __future__ import division #to avoid division truncation
import math
import pyaudio
import sys

PyAudio = pyaudio.PyAudio

RATE = 16000 #number of frames per second/frameset. 
BPM = 60 #beats per minute
VOLUME = 70 #min 0-127 max
CLEF = "treble" #if we ever get to detect the type of clef...
MAJOR = "D" #major

def beats2length(beats_list): #returns list of durations given list of beats of 0.5, 1, 2, etc.
	length_list = []
	for beat in beats_list:
		length_list.append((1/(BPM/beat/60))) 
	return length_list

def play_note(note_info): #note info is a list of two-element lists [duration, freq]
	for note in note_info:
		freq = note[1] #freq to play

		#For D major ONLY
		if freq == 349.2: #if F4, change to F#4
			freq = 370 
		if freq == 698.5: #if F5, change to F#5
			freq = 740

		length =  4/note[0] #seconds to play sound

		num_frames = int(RATE * length)
		rest_frame = num_frames % RATE
		WAVEDATA = ''    

		#127 is max volume, add 128 to stay in frame range
		for x in xrange(num_frames):
			WAVEDATA = WAVEDATA+chr(int(math.sin(x/((RATE/freq)/(2*math.pi)))*VOLUME+128))    

		p = PyAudio()
		stream = p.open(format = p.get_format_from_width(1), 
		                channels = 1, 
		                rate = RATE, 
		                output = True)
		stream.write(WAVEDATA)
		
	stream.stop_stream()
	stream.close()
	p.terminate()



