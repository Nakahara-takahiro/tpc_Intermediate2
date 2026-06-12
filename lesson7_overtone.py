# lesson7_overtone.py
# 第7回: 倍音体験
#
# 2つのサイン波(基音と倍音)を足し算して、新しい波形を作ります。
# 楽器の音色の違いは、この「倍音の混ざり方」の違いによるものです。

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

sample_rate = 44100
duration = 1.0
frequency = 440

t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# 基音(きおん): もとになる音の高さ
fundamental = np.sin(2 * np.pi * frequency * t)

# 倍音(ばいおん): 基音の2倍の周波数を持つ音
overtone = np.sin(2 * np.pi * (frequency * 2) * t)

# 2つの波を足し算する(倍音は基音より小さめに混ぜる)
combined = fundamental + 0.5 * overtone

# 音量が大きくなりすぎないように、最大値が1になるよう調整(正規化)
combined = combined / np.max(np.abs(combined))

# 波形を見比べる
display_samples = int(sample_rate * 0.01)
plt.plot(t[:display_samples], combined[:display_samples])
plt.title("Fundamental + Overtone")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()

# 足し算した音を鳴らす
sd.play(combined, sample_rate)
sd.wait()
