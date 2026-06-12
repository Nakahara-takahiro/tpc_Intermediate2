# lesson9_key_input.py
# 第9回: キー入力で音
#
# keyboard ライブラリを使って、キーを押すと音が鳴る仕組みを作ります。

import numpy as np
import sounddevice as sd
import keyboard

sample_rate = 44100


def make_wave(frequency, duration, wave_type="sine"):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sine_wave = np.sin(2 * np.pi * frequency * t)
    if wave_type == "sine":
        return sine_wave
    elif wave_type == "square":
        return np.sign(sine_wave)
    elif wave_type == "triangle":
        return (2 / np.pi) * np.arcsin(sine_wave)
    raise ValueError(f"unknown wave_type: {wave_type}")


def play_wave(frequency, duration, wave_type="sine"):
    wave = make_wave(frequency, duration, wave_type)
    sd.play(wave, sample_rate)
    sd.wait()


print("スペースキーを押すとラの音(440Hz)が鳴ります。ESCキーで終了します。")

# キーが押されているかを繰り返しチェックする
while True:
    if keyboard.is_pressed("space"):
        play_wave(440, 0.3)

    if keyboard.is_pressed("esc"):
        break
