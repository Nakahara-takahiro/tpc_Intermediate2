# lesson6_wave_shapes.py
# 第6回: 波形の種類
#
# サイン波(sine)のほかに、矩形波(square)・三角波(triangle)を作って
# 見比べ・聞き比べをします。同じ高さの音でも、波形が違うと音色が変わります。

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

sample_rate = 44100
duration = 1.0
frequency = 440

t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# サイン波(なめらかな波)
sine_wave = np.sin(2 * np.pi * frequency * t)

# 矩形波(値が+1と-1だけを行き来するガタガタの波)
square_wave = np.sign(sine_wave)

# 三角波(直線的に上下するギザギザの波)
triangle_wave = (2 / np.pi) * np.arcsin(sine_wave)

# 3つの波形を見比べる(最初の0.01秒だけ表示)
display_samples = int(sample_rate * 0.01)

fig, axes = plt.subplots(3, 1)
axes[0].plot(t[:display_samples], sine_wave[:display_samples])
axes[0].set_title("Sine")
axes[1].plot(t[:display_samples], square_wave[:display_samples])
axes[1].set_title("Square")
axes[2].plot(t[:display_samples], triangle_wave[:display_samples])
axes[2].set_title("Triangle")
plt.tight_layout()
plt.show()

# 3つの音を順番に聞き比べる
for wave in [sine_wave, square_wave, triangle_wave]:
    sd.play(wave, sample_rate)
    sd.wait()
