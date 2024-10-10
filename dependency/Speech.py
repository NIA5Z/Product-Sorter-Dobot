from gtts import gTTS
from io import BytesIO
import simpleaudio as sa
from pydub import AudioSegment


def speak(string="No String Input",lang="en"):
 mp3_fp = BytesIO()
 tts = gTTS(string, lang=lang)
 tts.write_to_fp(mp3_fp)

 mp3_fp.seek(0) 
 audio_segment = AudioSegment.from_mp3(mp3_fp)
 wav_fp = BytesIO()
 audio_segment.export(wav_fp, format='wav')
 wav_fp.seek(0)

 wave_obj = sa.WaveObject.from_wave_file(wav_fp)
 play_obj = wave_obj.play()
 play_obj.wait_done()

def speak2file(string="No String Input"):
 tts = gTTS(string, lang='en')
 print("Audio saved")
 tts.save('audio.mp3')

