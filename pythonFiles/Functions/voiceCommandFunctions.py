from pytube import YouTube
from pydub import AudioSegment
import os

def get_commands(filename):
    commands = []
    with open(filename, "r") as f:
        lines = f.readlines()
    
    for items in lines:
        commands.append([items.strip().split(",")[0], items.strip().split(",")[1].replace("\n", "")])
    
    return commands

def download_audio(youtube_url):
    voidFolderPath = os.getcwd().split("\\pythonFiles")[0].replace("\\", "/")
    yt = YouTube(youtube_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(f"{voidFolderPath}/audioFiles/downloads/", "audio.wav")
    
    audio_file = f"{voidFolderPath}/audioFiles/downloads/audio.wav"
    output_wav_file = f"{voidFolderPath}/audioFiles/downloads/audio.wav"
    audio = AudioSegment.from_file(audio_file, format="mp4")
    audio.export(output_wav_file, format="wav")
