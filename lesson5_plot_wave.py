# lesson5_plot_wave.py
# 第5回: 波形を見る
#
# matplotlib を使って、サイン波の形をグラフに表示します。
# x軸 = 時間、y軸 = 振幅(音の大きさ)です。

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

sample_rate = 44100
duration = 1.0
frequency = 440

t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
wave = np.sin(2 * np.pi * frequency * t)

# 波形は1秒分あると細かすぎて見えないので、最初の0.01秒だけ表示する
display_samples = int(sample_rate * 0.01)

plt.plot(t[:display_samples], wave[:display_samples])
plt.xlabel("Time [s]")    # x軸: 時間(秒)
plt.ylabel("Amplitude")   # y軸: 振幅(波の高さ)
plt.title("Sine Wave (440Hz)")
plt.show()

# グラフを閉じたら、同じ波形の音を鳴らす
sd.play(wave, sample_rate)
sd.wait()
