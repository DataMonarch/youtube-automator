import moviepy.editor as mp
import speech_recognition as sr
import pysrt

def transcribe_audio(audio_file_path: str) -> str:
    """Transcribe an audio file and return its transcription"""
    r = sr.Recognizer()
    audio_file = sr.AudioFile(audio_file_path)

    with audio_file as source:
        audio = r.record(source)

    # Using Sphinx for speech recognition
    transcription = r.recognize_sphinx(audio, show_all=True)

    # Accessing the recognized words with timestamps
    for word in transcription["words"]:
        print(f"{word['word']} - start: {Timestamp(word['start_time'])}, end: {Timestamp(word['end_time'])}")


video = mp.VideoFileClip("C:\\Users\\togru\\python-playground\\yt_automator\\data\\videos\\output\\Zh-AcF_4Hao-1.50\Zh-AcF_4Hao-1.50.mp4")
audio = video.audio
audio.write_audiofile("C:\\Users\\togru\\python-playground\\yt_automator\\data\\videos\\output\\Zh-AcF_4Hao-1.50\Zh-AcF_4Hao-1.50.wav")
transcribe_audio("C:\\Users\\togru\\python-playground\\yt_automator\\data\\videos\\output\\Zh-AcF_4Hao-1.50\Zh-AcF_4Hao-1.50.wav")