import pyaudio
import wave
import playsound
import simpleaudio as sa
import speech_recognition as sr
from gtts import gTTS
import os
from pygame import mixer
from io import BytesIO
import winsound
from pydub import AudioSegment
from pydub.playback import play
import sys
import subprocess
def get_audio():
		chunk = 1024
		sample_format = pyaudio.paInt16
		channels=2
		fs=44100
		seconds=3
		filename="output.wav"

		p = pyaudio.PyAudio()

		print("Recording")

		stream = p.open(
			format=sample_format,
			channels=channels,
			rate=fs,
			frames_per_buffer=chunk,
			input=True
			)

		frames=[]

		for i in range(int(fs/chunk*seconds)):
			data=stream.read(chunk)
			frames.append(data)

		stream.stop_stream()
		stream.close()
		p.terminate()

		print("Finished recording")
		wf = wave.open(filename, 'wb')
		wf.setnchannels(channels)
		wf.setsampwidth(p.get_sample_size(sample_format))
		wf.setframerate(fs)
		wf.writeframes(b''.join(frames))
		wf.close()

def speak(filename):
	# filename="answer.mp3"
	wave_obj = sa.WaveObject.from_wave_file(filename)
	play_obj = wave_obj.play()
	play_obj.wait_done()

def text_to_audio(answer):
	tts = gTTS(text=answer, lang='en')
	filename="answer.mp3"
	tts.save(filename)
	os.system(filename)

def audio_to_text():
	filename="output.wav"
	r = sr.Recognizer()
	try:
		with sr.AudioFile(filename) as source:
			audio_data = r.record(source)
			text=r.recognize_google(audio_data)
			return text
	except sr.UnknownValueError:
		could_not_recognize()

def could_not_recognize():
	language='en'
	myobj = gTTS(text="Could not recognize", lang=language, slow=False)
	myobj.save("cnr.mp3")
	os.system("cnr.mp3")


