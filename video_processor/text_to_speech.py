from gtts import gTTS
import os
import librosa
import json
from pydub import AudioSegment
from pydub.effects import speedup
from scipy.io import wavfile
import numpy as np

# with open("../data/submissions_talesfromtechsupport.json") as json_file:
#     data = json.load(json_file)

# text = data[list(data.keys())[0]]["body"]


# generate speech from the text string

def text_to_speech(text: str, audio_path: str):

    """
    Converts text to speech and saves it to an audio file.

    :param text: Text to be converted to speech.
    :param audio_path: Path to the audio file.
    :return: None
    """
    
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(audio_path)


def speed_change(sound:AudioSegment, speed: float=1.0):
    # add docstring for speed_change method    
    """
    Multiplies the speed of the sound by the given factor.
    :param sound: AudioSegment to be sped up.
    :param speed: speed-up factor.
    :return: AudioSegment
    """
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })

    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def mp3_to_wav(audio_file_name):
    # add docstring for mp3_to_wav
    """
    Convert mp3 file to wav format and save it to the same directory.
    :param audio_file_name: name of the audio file to be converted.
    """
    if audio_file_name.split('.')[-1] == 'mp3':
        sound = AudioSegment.from_mp3(audio_file_name)
        audio_file_name = ''.join(audio_file_name.split('.')[:-1]) + '.wav'
        sound.export(audio_file_name, format="wav")
    return audio_file_name

# TO-DO: conversion error: wav - mp3
def wav_to_mp3(audio_file_name):
    
    """
    Convert wav file to mp3 format and save it to the same directory.
    :param audio_file_name: name of the audio file to be converted.
    """
    if audio_file_name.split('.')[-1] == 'wav':
        sound = AudioSegment.from_wav(audio_file_name)
        audio_file_name = ''.join(audio_file_name.split('.')[:-1]) + '.mp3'
        sound.export(audio_file_name, format="mp3")
    return audio_file_name

def wav_resampler(wav_path: str, speed_up_ratio: float = 1.0) -> str:
    
    """
    Resample a wav file to a new wav file with a different sampling rate.

    :param wav_path: The path to the wav file to be resampled.
    :param speed_up_ratio: The ratio of the new sampling rate to the old sampling rate.
    :return: The path to the resampled wav file.
    """
    
    speech_rate, speech_data = wavfile.read(wav_path)
    
    out_path = ''.join(wav_path.split('.')[:-1]) + f"_faster." + wav_path.split('.')[-1]
    wavfile.write(out_path, int(speech_rate*speed_up_ratio), speech_data)
    
    return out_path


def mp3_resampler(mp3_path: str, speed_up_ratio: float = 1.0) -> str:
    """
    Resample an mp3 file to a new speed.

    :param mp3_path: The path to the mp3 file to be resampled.
    :param speed_up_ratio: The ratio to speed up the mp3 file.
    :return: The path to the resampled mp3 file.
    """
    wav_path = mp3_to_wav(mp3_path)
    print(wav_path)
    faster_wav_path = wav_resampler(wav_path, speed_up_ratio)
    print(faster_wav_path)
    out_path = wav_to_mp3(faster_wav_path)
    
    return out_path
    
# remove silence from a wav file
    
def wav_silence_remover(wav_path: str, silence_threshold: int = 125) -> str:
    """
    Remove silence from a wav file.

    :param wav_path: path to the wav file
    :param silence_threshold: silence threshold
    :return: path to the wav file without silence
    """
    
    speech_rate, speech_data = wavfile.read(wav_path)
    #identify all samples with an absolute value greater than the threshold
    greater_index = np.greater(np.absolute(speech_data), silence_threshold)
    #filter to only include the identified samples
    above_threshold_data = speech_data[greater_index]
    out_path = ''.join(wav_path.split('.')[:-1]) + f"_silenced_{silence_threshold}." + wav_path.split('.')[-1]

    wavfile.write(out_path, speech_rate, above_threshold_data)

    return out_path

def sfft_audio_stretcher(wav_path: str, stretch_factor=1.5):
    """
    Stretch the audio by a factor of stretch_factor using the SFFT method.

    Args:
        wav_path (str): path to the wav file to be stretched.
        stretch_factor (float, optional): the factor by which sound is to be stretched. Defaults to 1.5.

    Returns:
        str: path of the stretched audio file.
    """
    
    audio, speech_rate = librosa.load(wav_path)

    stretched_audio = librosa.effects.time_stretch(audio, rate=stretch_factor)
    out_path = ''.join(wav_path.split('.')[:-1]) + f"_stretched." + wav_path.split('.')[-1]

    wavfile.write(out_path, speech_rate, stretched_audio)
    
    return out_path

mp3_path = "C:/Users/togru/python-playground/yt_automator/data/speech.mp3"

# mp3_resampler(mp3_path, speed_up_ratio=1.5)
wav_path = mp3_to_wav(mp3_path)
wav_path = sfft_audio_stretcher(wav_path, stretch_factor=1.75)
wav_path = wav_silence_remover(wav_path, silence_threshold=50)
# resampled_silenced_wav_path = wav_resampler(silenced_wav_path, speed_up_ratio=1.2)
print(wav_path)





	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
