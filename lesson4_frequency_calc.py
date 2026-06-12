# lesson4_frequency_calc.py
# 第4回: 周波数の計算
#
# 平均律(へいきんりつ)の計算式を関数にして、音名から周波数を求められるようにします。

import numpy as np
import sounddevice as sd

sample_rate = 44100

# 基準の音: ラ(A4) = 440Hz
A4 = 440


def note_to_freq(n):
    """A4から半音いくつ離れているか(n)を渡すと、その音の周波数を返す"""
    # 平均律では、半音1つ上がると周波数は 2の12乗根 倍になる
    return A4 * (2 ** (n / 12))


# 音名 -> A4(ラ)からの半音差 の対応表(辞書)
note_names = {
    "C4": -9,  # ド
    "D4": -7,  # レ
    "E4": -5,  # ミ
    "F4": -4,  # ファ
    "G4": -2,  # ソ
    "A4": 0,   # ラ
    "B4": 2,   # シ
    "C5": 3,   # ド(1オクターブ上)
}


def play_note(name, duration=1.0):
    """音名(例:"C4")を受け取って、その音を鳴らす"""
    freq = note_to_freq(note_names[name])
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.sin(2 * np.pi * freq * t)
    sd.play(wave, sample_rate)
    sd.wait()


# ド・ミ・ソ を順番に鳴らす
play_note("C4")
play_note("E4")
play_note("G4")
