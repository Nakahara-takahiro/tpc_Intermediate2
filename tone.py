# tone.py
# 共通モジュール: 音を鳴らす基本部品
#
# 第1〜2回はこの play_tone 関数を使って音を鳴らします。
# 中でどうやって音を作っているかは、まだ知らなくて大丈夫です。
# 第3回「波の正体」で、この中身(numpy + sounddevice)を自分の手で書いて明かします。
#
# winsoundはWindows専用でLinuxでは使えないため、
# クラブのパソコン(Windows/Linux混在)でどちらでも動くよう numpy + sounddevice を使っています。

import numpy as np
import sounddevice as sd

sample_rate = 44100


def play_tone(frequency, duration):
    """周波数[Hz]と鳴らす時間[秒]を指定して、音を鳴らす"""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.sin(2 * np.pi * frequency * t)
    sd.play(wave, sample_rate)
    sd.wait()
    return wave
