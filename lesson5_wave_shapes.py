# lesson5_wave_shapes.py
# 第5回: 波形で音色が変わる
#
# サイン波(sine)のほかに、矩形波(square)・三角波(triangle)を作って
# 見比べ・聞き比べをします。同じ高さの音でも、波形が違うと音色が変わります。
# 最後に、3つの音色でドレミファソラシドを演奏します。
#
# 第3回で作った note_to_freq 関数と note_names 辞書は、そのまま使います。

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

sample_rate = 44100
volume = 0.3  # 音量(1.0だと大きすぎるので小さめにする)

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

# ---------------------------------------------
# 1. 同じ高さ(ラ)の音を、3つの波形で作る
# ---------------------------------------------
duration = 1.0
frequency = note_to_freq(note_names["A4"])
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

# 3つの音を順番に聞き比べる(グラフを閉じると鳴る)
for wave in [sine_wave, square_wave, triangle_wave]:
    sd.play(wave * volume, sample_rate)
    sd.wait()

# ---------------------------------------------
# 2. ドレミファソラシドを演奏する
# ---------------------------------------------
scale = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]
note_length = 0.8  # 1音の長さ(秒)

for name in scale:
    freq = note_to_freq(note_names[name])
    t = np.linspace(0, note_length, int(sample_rate * note_length), endpoint=False)

    sine_wave = np.sin(2 * np.pi * freq * t)
    square_wave = np.sign(sine_wave)
    triangle_wave = (2 / np.pi) * np.arcsin(sine_wave)

    wave = [sine_wave, square_wave, triangle_wave]  # 3つの波形を順番に演奏する

    for w in wave:
        sd.play(w * volume, sample_rate)
        sd.wait()