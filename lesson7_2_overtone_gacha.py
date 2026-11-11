# lesson7_2_overtone_gacha.py
# 第7回(発展): 音色ガチャ
#
# lesson7_overtone.py では、レシピ(recipe)の数字を自分で考えて音色を作りました。
# 今回はコンピュータにレシピをランダムに(でたらめに)決めてもらいます。
# 何が出るかは回してみるまでわかりません。5回まわして「当たり」の音色を探しましょう。
# 気に入った音色が出たら、そのレシピを lesson7_overtone.py にコピーして使えます。

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
    "E4": -5,  # ミ
    "G4": -2,  # ソ
    "C5": 3,   # ド(1オクターブ上)
}

# 倍音のレシピ(ガチャを回すたびに中身が入れかわる)
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
# 音色ガチャを5回まわす
# ---------------------------------------------
display_samples = int(sample_rate * 0.01)
fig, axes = plt.subplots(2, 1)

for number in range(1, 6):
    # 0〜1のでたらめな数を5個作り、小数第1位までに丸める
    recipe = np.round(np.random.rand(5), 1)
    recipe[0] = 1.0  # 基音(1倍)は1.0に固定する(音の高さがそろって聞き比べやすい)
    print(f"ガチャ{number}回目: recipe = {recipe.tolist()}")

    # グラフ: 上がレシピ(棒グラフ)、下ができあがった波形
    t, wave = make_recipe_wave(note_to_freq(note_names["C4"]), 1.0)
    axes[0].cla()  # 前の回のグラフを消す
    axes[0].bar(range(1, len(recipe) + 1), recipe)
    axes[0].set_ylim(0, 1)
    axes[0].set_title(f"Gacha No.{number}")
    axes[1].cla()
    axes[1].plot(t[:display_samples], wave[:display_samples])
    plt.tight_layout()
    plt.pause(0.1)  # ここまでのグラフを画面に表示する

    # 出てきた音色で「ドミソド」を鳴らす
    for name in ["C4", "E4", "G4", "C5"]:
        t, wave = make_recipe_wave(note_to_freq(note_names[name]), 0.3)
        sd.play(wave * volume, sample_rate)
        sd.wait()

print("気に入ったレシピを lesson7_overtone.py の recipe にコピーして、ドレミを弾いてみよう")
plt.show()  # 画面を閉じるまでグラフを表示したままにする
