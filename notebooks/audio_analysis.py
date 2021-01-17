# %%
# Imports
import sys

sys.path.insert(0, "..")

from sunflower.song_loader import Song, load_from_disk
from sunflower.song_analyzer import SongAnalyzer
from sunflower.utils import export_wav
from sunflower.benchmark import run_benchmark
from sunflower.song_visualizer import visualize_waveform, visualize_waveform_plotly
from moviepy.editor import *
from moviepy.audio.AudioClip import AudioArrayClip
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import librosa
import soundfile as sf
import pygame

# %%
# Loading example file

raw_audio, extension = load_from_disk("../data_benchmark/drums.wav")

song = Song(raw_audio, extension)

song.print_attributes()

# %%
# Analyze song

song_analyzer = SongAnalyzer(song)

# %%
def clamp(min_value, max_value, value):

    if value < min_value:
        return min_value

    if value > max_value:
        return max_value

    return value


class AudioBar:
    def __init__(
        self,
        x,
        y,
        freq,
        decibel,
        color=(0, 0, 0),
        width=50,
        min_height=10,
        max_height=100,
        min_decibel=-80,
        max_decibel=0,
    ):

        self.x, self.y, self.freq = x, y, freq

        self.color = color

        self.width, self.min_height, self.max_height = width, min_height, max_height

        self.height = min_height

        self.min_decibel, self.max_decibel = min_decibel, max_decibel

        self.__decibel_height_ratio = (self.max_height - self.min_height) / (
            self.max_decibel - self.min_decibel
        )

        desired_height = decibel * self.__decibel_height_ratio + self.max_height

        self.height = clamp(self.min_height, self.max_height, desired_height)


def draw_rectangle(frame, audiobar):
    """Draw a rectangle in the frame.
    """

    # Change (top, bottom, left, right) to your coordinates
    left = int(audiobar.x)
    right = left + int(audiobar.width)
    bottom = 0
    top = int(bottom) + int(audiobar.height)
    frame[bottom:top, left:right] = audiobar.color

    return frame


# %%
# getting a matrix which contains amplitude values according to frequency and time indexes


def color_clip(size, duration, fps=25, color=(50, 50, 50)):
    return ColorClip(size, color, duration=duration)


frequencies = np.arange(100, 8000, 100)
size = (400, 400)
audioclip = AudioArrayClip(song.waveform.reshape(-1, 2), song.sr)
duration = audioclip.duration

fps_equalizer = 0.01
time = 0
width = 1
clips = []

while len(clips) * fps_equalizer < duration:
    x = 0
    clip = color_clip(size, fps_equalizer)

    for c in frequencies:

        clip = clip.fl_image(
            lambda image: draw_rectangle(
                image,
                AudioBar(
                    x,
                    300,
                    c,
                    song_analyzer.get_decibel(time, c),
                    max_height=400,
                    width=width,
                ),
            )
        )

        x += width

    clip = clip.set_duration(fps_equalizer).set_start(time)
    clips.append(clip)

    time += fps_equalizer

clip = CompositeVideoClip(clips)
clip = clip.set_audio(audioclip)

# %%
clip.write_videofile(
    "eq.mp4",
    fps=24,
    temp_audiofile="../temp-audio.m4a",
    remove_temp=True,
    codec="libx264",
    audio_codec="aac",
)
# %%
# getting a matrix which contains amplitude values according to frequency and time indexes
