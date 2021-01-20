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

raw_audio, extension = load_from_disk("../data_benchmark/test_eq.wav")

song = Song(raw_audio, extension)

song.print_attributes()

# %%
# Analyze song

song_analyzer = SongAnalyzer(song)
