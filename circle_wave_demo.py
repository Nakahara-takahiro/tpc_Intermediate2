# circle_wave_demo.py
# デモ教材: 円を回る点が「波」になるところを見る
#
# このファイルは写経しません。GitHubからダウンロードして、そのまま実行してください。
#
#   python circle_wave_demo.py
#
# 左の円のふちを、点が一定の速さでぐるぐる回ります。
# その点の「高さ」を右へ流していくと、右側に波が描かれます。
# これがサイン波の正体です。円を回る点の高さの記録が、そのまま波の形になります。
#
# 画面いちばん下の「周波数」スライダーを、動かしながら実行中にドラッグしてみましょう。
# スライダーを右に動かす(周波数を大きくする)ほど、点の回転が速くなり、波が細かくなります。
#
# 波の大きさ(振幅)を変えたいときは、下の「設定」の amplitude の数字を書きかえてから、
# もう一度実行してください。

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib import font_manager

# --- 画面の文字を日本語で表示するための設定 ---
# パソコンによって入っているフォントが違うため、日本語が使えるフォントを順番にさがす。
_日本語フォント候補 = [
    "Yu Gothic", "Meiryo", "MS Gothic",
    "Noto Sans CJK JP", "IPAexGothic", "TakaoGothic", "VL PGothic",
]
_使えるフォント名 = {f.name for f in font_manager.fontManager.ttflist}
for _名前 in _日本語フォント候補:
    if _名前 in _使えるフォント名:
        plt.rcParams["font.family"] = _名前
        break
plt.rcParams["axes.unicode_minus"] = False  # 日本語フォントだとマイナス記号が文字化けするのを防ぐ

# ============ 設定: ここの数字を変えて実行してみよう ============

amplitude = 1.0   # 波の大きさ(円の半径)。大きくすると波の高さが増え、音が大きくなる

# ==============================================================

window = 2.0          # 右のグラフに表示する時間の幅[秒]
fps = 60              # 1秒あたりの表示コマ数
points = 600          # 波の線を描く点の数(多いほど、周波数が高くてもなめらかに見える)

# --- 画面の準備(左: 円、右: 波、下: スライダー) ---
fig, (ax_circle, ax_wave) = plt.subplots(
    1, 2, figsize=(10, 4.5), sharey=True, gridspec_kw={"width_ratios": [1, 2]}
)
fig.subplots_adjust(bottom=0.25)
fig.canvas.manager.set_window_title("円と波")

limit = amplitude * 1.3

# 左: 円そのものを描いておく(点が通る道)
circle_angle = np.linspace(0, 2 * np.pi, 200)
ax_circle.plot(amplitude * np.cos(circle_angle), amplitude * np.sin(circle_angle),
               color="0.7", linewidth=1)
ax_circle.set_xlim(-limit, limit)
ax_circle.set_ylim(-limit, limit)
ax_circle.set_aspect("equal")
ax_circle.set_title("回転する点")
# 日本語のフォントは、縦書き(回転)で表示すると文字が崩れることがあるため、横書きのまま表示する
ax_circle.set_ylabel("高さ", rotation=0, labelpad=25, ha="right", va="center")

radius_line, = ax_circle.plot([0, amplitude], [0, 0], color="tab:blue", linewidth=1.5)
point, = ax_circle.plot([amplitude], [0], "o", color="tab:red", markersize=9)
circle_guide, = ax_circle.plot([], [], "--", color="tab:red", linewidth=0.8)

# 右: 点の高さを流していく波のグラフ
wave_line, = ax_wave.plot([], [], color="tab:blue", linewidth=1.5)
wave_head, = ax_wave.plot([], [], "o", color="tab:red", markersize=9)
wave_guide, = ax_wave.plot([], [], "--", color="tab:red", linewidth=0.8)
ax_wave.set_xlim(-window, 0)
ax_wave.set_ylim(-limit, limit)
ax_wave.set_xlabel("時間[秒]（いちばん右が「今」）")
ax_wave.axhline(0, color="0.8", linewidth=0.8)

# --- 周波数スライダー: 動かすと、実行中でも回転の速さが変わる ---
ax_slider = fig.add_axes([0.2, 0.1, 0.55, 0.04])
freq_slider = Slider(
    ax_slider, "周波数(しゅうはすう)",
    valmin=0.1, valmax=5.0, valinit=1.0, valstep=0.1,
    valfmt="%.1f Hz",
)

plt.ion()
plt.show()

# --- ここからアニメーション ---
# 波の線は、1コマごとに「今から window 秒前まで」を numpy でまとめて計算し直しています。
# 記録を1点ずつ積み上げる方式だと、周波数を上げたときに点の間隔が粗くなってガタガタに
# 見えてしまうため、コマの表示回数(fps)によらず points 個の点で常になめらかに描いています。
# 周波数は毎回スライダーの値を読みに行くので、動かした瞬間に回転の速さが変わります。
x_axis = np.linspace(-window, 0, points)  # 波を描くための時間軸(今から window 秒前まで)
t = 0.0

while plt.fignum_exists(fig.number):
    t += 1.0 / fps
    frequency = freq_slider.val

    angle = 2 * np.pi * frequency * t   # 時間がたつほど角度が進む = 一定の速さで回る
    height = amplitude * np.sin(angle)  # 円の上の点の「高さ」← これが波になる
    across = amplitude * np.cos(angle)  # 円のどこにいるか(横方向)。点を描くために使う

    # 左の円を更新する
    radius_line.set_data([0, across], [0, height])
    point.set_data([across], [height])
    circle_guide.set_data([across, limit], [height, height])

    # 右の波を更新する(x_axis上の各時刻での高さを、まとめて計算し直す)
    wave_heights = amplitude * np.sin(2 * np.pi * frequency * (t + x_axis))
    wave_line.set_data(x_axis, wave_heights)
    wave_head.set_data([0], [height])
    wave_guide.set_data([-window, 0], [height, height])

    ax_wave.set_title(f"振幅(しんぷく) = {amplitude:.1f}　周波数 = {frequency:.1f} Hz")

    fig.canvas.draw_idle()
    fig.canvas.flush_events()
    plt.pause(0.001)
