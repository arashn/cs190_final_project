from __future__ import division #to avoid division truncation
import math
import pyaudio
import sys

RATE = 44100 #number of frames per second/frameset. 
BPM = 60 #beats per minute
VOLUME = 70 #min 0-127 max
CLEF = "treble" #if we ever get to detect the type of clef...
MAJOR = "C" #major

def beats2length(beats_list): #returns list of durations given list of beats of 0.5, 1, 2, etc.
	length_list = []
	for beat in beats_list:
		length_list.append((1/(BPM/beat/60))) 
	return length_list

def play_note(note_info, bpm, major): #note info is a list of two-element lists [duration, freq]
	BPM = bpm
	MAJOR = major
	for note in note_info:
		freq = note[1] #freq to play

		if (MAJOR == "G") or (MAJOR == "D") or (MAJOR =="A") or (MAJOR =="E") or (MAJOR =="B") or (MAJOR =="F#") or (MAJOR =="C#"):
			if freq == 349.2: #if F4, change to F#4
		 		freq = 370 
			if freq == 698.5: #if F5, change to F#5
				freq = 740
			if (MAJOR == "D") or (MAJOR =="A") or (MAJOR =="E") or (MAJOR =="B") or (MAJOR =="F#") or (MAJOR =="C#"):
				if freq == 261.6:
					freq = 277.2
				if freq == 523.3:
					freq = 554.4

		length =  4/note[0]/(BPM/60) #seconds to play sound

		num_frames = int(RATE * length)
		rest_frame = num_frames % RATE
		wave_data = ''    

		#127 is max volume, add 128 to stay in frame range
		for x in xrange(num_frames):
			wave_data = wave_data+chr(int(math.sin(x/((RATE/freq)/(2*math.pi)))*VOLUME+128))    

		p = pyaudio.PyAudio()
		stream = p.open(format = p.get_format_from_width(1), 
		                channels = 1, 
		                rate = RATE, 
		                output = True)
		stream.write(wave_data)
		
	stream.stop_stream()
	stream.close()
	p.terminate()



