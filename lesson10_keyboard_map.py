# lesson10_keyboard_map.py
# 第10回: ミニ鍵盤
#
# 複数のキーに音階を割り当て、辞書で「キー -> 周波数」の対応表を作ります。
# これでパソコンのキーボードが、ミニ鍵盤になります。
# あわせて oscilloscope モジュールを使い、音を鳴らすたびに波形を画面に表示します。

import numpy as np
import sounddevice as sd
import keyboard
from oscilloscope import show_waveform

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
    show_waveform(wave, sample_rate, title=f"{frequency}Hz")


# キー -> 周波数(Hz) の対応表(ドレミファソラシド)
key_to_freq = {
    "a": 262,  # ド
    "s": 294,  # レ
    "d": 330,  # ミ
    "f": 349,  # ファ
    "g": 392,  # ソ
    "h": 440,  # ラ
    "j": 494,  # シ
    "k": 523,  # ド(高い)
}

print("A〜Kのキーを押すと、ドレミファソラシドが鳴ります。ESCキーで終了します。")

while True:
    # 辞書の中身を1つずつチェックして、押されていたら鳴らす
    for key, freq in key_to_freq.items():
        if keyboard.is_pressed(key):
            play_wave(freq, 0.3)

    if keyboard.is_pressed("esc"):
        break
