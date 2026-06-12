# lesson8_tone_select.py
# 第8回: 音色切替
#
# 波形タイプ(sine/square/triangle)を切り替えられる関数にまとめます。
# ここで作る make_wave / play_wave は、次回以降もずっと使う基本パーツです。

import numpy as np
import sounddevice as sd

sample_rate = 44100


def make_wave(frequency, duration, wave_type="sine"):
    """周波数・長さ・波形タイプを指定して、波形データを作る"""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sine_wave = np.sin(2 * np.pi * frequency * t)

    if wave_type == "sine":
        wave = sine_wave
    elif wave_type == "square":
        wave = np.sign(sine_wave)
    elif wave_type == "triangle":
        wave = (2 / np.pi) * np.arcsin(sine_wave)
    else:
        raise ValueError(f"unknown wave_type: {wave_type}")

    return wave


def play_wave(frequency, duration, wave_type="sine"):
    """波形データを作って再生する"""
    wave = make_wave(frequency, duration, wave_type)
    sd.play(wave, sample_rate)
    sd.wait()


# 同じ高さの音(440Hz)を、音色を変えて聞き比べる
play_wave(440, 1.0, "sine")
play_wave(440, 1.0, "square")
play_wave(440, 1.0, "triangle")
