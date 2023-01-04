from gtts import gTTS
import os
import json
from pydub import AudioSegment
from pydub.effects import speedup
import soundfile as sf
import pyrubberband as pyrb


# with open("../data/submissions_talesfromtechsupport.json") as json_file:
#     data = json.load(json_file)

# text = data[list(data.keys())[0]]["body"]

audio_path = "../data/speech.mp3"

# generate speech from the text string

def text_to_speech(text, audio_path):
    
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(audio_path)



# audio = AudioSegment.from_mp3(audio_path)
# new_file = speedup(audio, 1.5,150)
# new_file.export("../data/speech_fast.mp3", format="mp3")

# speed up an mp3 file

#sound = AudioSegment.from_file("deviprasadgharpehai.mp3")


def speed_change(sound:AudioSegment, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })

    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

sound = AudioSegment.from_mp3(audio_path)
sound = speed_change(sound, speed=1.5)
sound.export("../data/speech_faster.mp3", format="mp3")

# y, sr = sf.read("../data/file.wav")
# # Play back at extra low speed
# y_stretch = pyrb.time_stretch(y, sr, 0.5)
# # Play back extra low tones
# y_shift = pyrb.pitch_shift(y, sr, 0.5)
# sf.write("../data/analyzed_filepathX5.wav", y_stretch, sr, format='wav')

# sound = AudioSegment.from_wav("../data/analyzed_filepathX5.wav")
# sound.export("../data/analyzed_filepathX5.mp3", format="mp3")

# # Play back at low speed
# y_stretch = pyrb.time_stretch(y, sr, 0.75)
# # Play back at low tones
# y_shift = pyrb.pitch_shift(y, sr, 0.75)
# sf.write("../data/analyzed_filepathX75.wav", y_stretch, sr, format='wav')

# sound = AudioSegment.from_wav("../data/analyzed_filepathX75.wav")
# sound.export("../data/analyzed_filepathX75.mp3", format="mp3")

# # Play back at 1.5X speed
# y_stretch = pyrb.time_stretch(y, sr, 1.5)
# # Play back two 1.5x tones
# y_shift = pyrb.pitch_shift(y, sr, 1.5)
# sf.write("../data/analyzed_filepathX105.wav", y_stretch, sr, format='wav')

# sound = AudioSegment.from_wav("../data/analyzed_filepathX105.wav")
# sound.export("../data/analyzed_filepathX105.mp3", format="mp3")

# # Play back at same speed
# y_stretch = pyrb.time_stretch(y, sr, 1)
# # Play back two smae-tones
# y_shift = pyrb.pitch_shift(y, sr, 1)
# sf.write("../data/analyzed_filepathXnormal.wav", y_stretch, sr, format='wav')

# sound = AudioSegment.from_wav("../data/analyzed_filepathXnormal.wav")
# sound.export("../data/analyzed_filepathXnormal.mp3", format="mp3")