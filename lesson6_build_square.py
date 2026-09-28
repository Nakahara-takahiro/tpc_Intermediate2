# lesson6_build_square.py
# 第6回: 矩形波の中にはサイン波が隠れている
#
# 第5回で「波形が違うと音色が変わる」ことを確かめました。では、なぜ変わるのでしょう?
# 実は矩形波は、サイン波を何枚も足し算して作ることができます。
#   矩形波 = 1倍の音 + 3倍の音/3 + 5倍の音/5 + 7倍の音/7 + ...
# 足していくと、グラフの形も、聞こえる音色も、少しずつ矩形波に近づいていきます。
# この「1倍の音(基音)に混ざっている、2倍・3倍…の音」を倍音(ばいおん)といいます。

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

# お手本の矩形波(第5回と同じ作り方)
sine_wave = np.sin(2 * np.pi * frequency * t)
square_wave = np.sign(sine_wave)

display_samples = int(sample_rate * 0.01)

# ---------------------------------------------
# サイン波を足し算して、矩形波を組み立てる
# ---------------------------------------------
harmonics = [1, 3, 5, 7, 9]      # 足していく倍音(何倍の音か)
height_fix = 4 / np.pi           # 高さを矩形波(+1〜-1)にそろえるための数(約1.27)
built_wave = np.zeros_like(t)    # 最初は全部0の波(何も鳴らない)

fig, axes = plt.subplots(len(harmonics), 1, sharex=True)

for i, n in enumerate(harmonics):
    # n倍の周波数のサイン波を、1/n の大きさにして足す
    built_wave = built_wave + height_fix * np.sin(2 * np.pi * frequency * n * t) / n

    # グラフ: 灰色がお手本の矩形波、青が組み立て中の波
    axes[i].plot(t[:display_samples], square_wave[:display_samples], color="lightgray")
    axes[i].plot(t[:display_samples], built_wave[:display_samples])
    axes[i].set_title(f"up to x{n}")
    plt.tight_layout()
    plt.pause(0.1)  # ここまでのグラフを画面に表示する

    # 組み立て中の音を鳴らす(足すたびに音色が変わっていく)
    sd.play(built_wave * volume, sample_rate)
    sd.wait()

# 最後にお手本の矩形波を鳴らして、組み立てた音と聞き比べる
sd.play(square_wave * volume, sample_rate)
sd.wait()

plt.show()  # 画面を閉じるまでグラフを表示したままにする
