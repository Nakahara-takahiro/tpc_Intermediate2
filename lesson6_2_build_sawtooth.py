# lesson6_2_build_sawtooth.py
# 第6回(発展): ノコギリ波の中にもサイン波が隠れている
#
# lesson6_build_square.py では、奇数倍(1, 3, 5, ...)の音だけを足して矩形波を作りました。
# では、偶数倍の音も入れて「すべての倍音」を足すとどうなるでしょう?
#   ノコギリ波 = 1倍の音 + 2倍の音/2 + 3倍の音/3 + 4倍の音/4 + ...
# 足していくと、グラフはギザギザの「ノコギリ」の形に近づいていきます。

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

duration = 1.0
frequency = note_to_freq(note_names["A4"])
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# お手本のノコギリ波(+1から-1へまっすぐ下がり、またすぐ+1に戻る)
# (frequency * t) % 1 は、1周期の中で 0 → 1 へ増えていく数
sawtooth_wave = 1 - 2 * ((frequency * t) % 1)

display_samples = int(sample_rate * 0.01)

# ---------------------------------------------
# サイン波を足し算して、ノコギリ波を組み立てる
# ---------------------------------------------
harmonics = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # 足していく倍音(偶数倍も入れる)
height_fix = 2 / np.pi                   # 高さをノコギリ波(+1〜-1)にそろえるための数(約0.64)
built_wave = np.zeros_like(t)            # 最初は全部0の波(何も鳴らない)

fig, axes = plt.subplots(len(harmonics), 1, sharex=True, figsize=(6, 9))

for i, n in enumerate(harmonics):
    # n倍の周波数のサイン波を、1/n の大きさにして足す
    built_wave = built_wave + height_fix * np.sin(2 * np.pi * frequency * n * t) / n

    # グラフ: 灰色がお手本のノコギリ波、青が組み立て中の波
    axes[i].plot(t[:display_samples], sawtooth_wave[:display_samples], color="lightgray")
    axes[i].plot(t[:display_samples], built_wave[:display_samples])
    axes[i].set_title(f"up to x{n}")
    plt.tight_layout()
    plt.pause(0.1)  # ここまでのグラフを画面に表示する

    # 組み立て中の音を鳴らす(足すたびに音色が変わっていく)
    sd.play(built_wave * volume, sample_rate)
    sd.wait()

# 最後にお手本のノコギリ波を鳴らして、組み立てた音と聞き比べる
sd.play(sawtooth_wave * volume, sample_rate)
sd.wait()

plt.show()  # 画面を閉じるまでグラフを表示したままにする
