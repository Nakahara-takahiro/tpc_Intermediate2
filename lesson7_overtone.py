# lesson7_overtone.py
# 第7回: 倍音体験 ― 自分だけの音色を作る
#
# 第6回では、サイン波を「決まった混ぜ方」で足し算して矩形波を組み立てました。
# 今回は混ぜ方を自分で決めます。倍音をどれだけ混ぜるかを並べたリストを
# 「レシピ(recipe)」と呼び、レシピを変えると、まだ誰も知らない音色が作れます。
# 楽器の音色の違いも、この「倍音の混ざり方」の違いで生まれています。

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

# 倍音のレシピ: 左から 1倍(基音), 2倍, 3倍, 4倍, 5倍 の音をどれだけ混ぜるか
recipe = [1.0, 0.5, 0.3, 0.2, 0.1]


def make_recipe_wave(frequency, duration):
    """レシピどおりに倍音を足し算して、波形データを作る"""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.zeros_like(t)

    for i, amount in enumerate(recipe):
        n = i + 1  # 何倍の音か(リストの0番目が1倍)
        wave = wave + amount * np.sin(2 * np.pi * frequency * n * t)

    # 音量が大きくなりすぎないように、最大値が1になるよう調整(正規化)
    wave = wave / np.max(np.abs(wave))
    return t, wave


# ---------------------------------------------
# 1. レシピと、できあがった波形を見る
# ---------------------------------------------
t, wave = make_recipe_wave(note_to_freq(note_names["A4"]), 1.0)
display_samples = int(sample_rate * 0.01)

fig, axes = plt.subplots(2, 1)
axes[0].bar(range(1, len(recipe) + 1), recipe)  # 棒グラフ: 倍音ごとの混ぜる量
axes[0].set_title("Recipe")
axes[0].set_xlabel("Harmonic (x times)")
axes[1].plot(t[:display_samples], wave[:display_samples])
axes[1].set_title("My Wave")
plt.tight_layout()
plt.show()

# ---------------------------------------------
# 2. 自分の音色でドレミファソラシドを演奏する
# ---------------------------------------------
scale = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]

for name in scale:
    t, wave = make_recipe_wave(note_to_freq(note_names[name]), 0.4)
    sd.play(wave * volume, sample_rate)
    sd.wait()
