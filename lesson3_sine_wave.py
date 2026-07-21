# lesson3_sine_wave.py
# 第3回: 波の正体
#
# 第1〜2回で使っていた tone.play_tone の中身を、今回は自分の手で書いてみます。
# numpy でサイン波のデータ(数字の並び)を作り、sounddevice で再生します。
# 「音 = 波 = 数字の並び」であることを体感するのが目標です。
# あわせて oscilloscope モジュールを使い、再生した波形を画面に表示します。

import numpy as np
import sounddevice as sd
from oscilloscope import show_waveform, keep_open

sample_rate = 44100  # 1秒間に44100個のデータを使う(CD音質と同じ)
duration = 1.0       # 音を鳴らす時間(秒)
frequency = 440      # 周波数(Hz) = ラの音

# 0秒から1秒までを、sample_rate*duration個の点に分けた時間の配列を作る
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# サイン波のデータを作る(これが「波形」そのもの)
wave = np.sin(2 * np.pi * frequency * t)

# 作ったデータを音として再生する
sd.play(wave, sample_rate)
sd.wait()  # 再生が終わるまでプログラムを待たせる

# 再生した波形を、オシロスコープのように画面に表示する
show_waveform(wave, sample_rate, title=f"{frequency}Hz")
keep_open()  # 画面を閉じるまで波形を表示したままにする
