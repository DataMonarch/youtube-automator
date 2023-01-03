from gtts import gTTS
import os
import json
from pydub import AudioSegment
from pydub.effects import speedup



with open("../data/submissions_talesfromtechsupport.json") as json_file:
    data = json.load(json_file)

text = data[list(data.keys())[0]]["body"]

audio_path = "../data/speech.mp3"
# generate speech from the text string
tts = gTTS(text=text, lang='en', slow=False)
# save the speech to a file
tts.save(audio_path)



# speed up an mp3 file