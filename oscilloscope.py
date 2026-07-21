# oscilloscope.py
# 共通モジュール: 波形を「オシロスコープ」のように画面へ表示する
#
# 他の lessonN_*.py から import して使います。
#
#   from oscilloscope import show_waveform, keep_open
#   show_waveform(wave, sample_rate, title="440Hz")  # 波形を画面に表示(更新)する
#   keep_open()                                       # プログラムの最後で画面を表示したままにする
#
# 音を鳴らすたびに show_waveform を呼び出すと、1つの画面の波形が
# そのつど新しい音に切り替わり、オシロスコープで観察しているように見えます。

import numpy as np
import matplotlib.pyplot as plt

plt.ion()  # 対話モード: グラフを表示したままプログラムを先に進められるようにする

_fig, _ax = plt.subplots(figsize=(6, 3))
_line, = _ax.plot([0], [0])
_ax.set_xlabel("Time [s]")
_ax.set_ylabel("Amplitude")
_ax.set_ylim(-1.2, 1.2)
_fig.canvas.manager.set_window_title("Oscilloscope")
_fig.tight_layout()


def show_waveform(wave, sample_rate, title="Waveform", duration=0.01):
    """波形データの先頭 duration 秒分を、オシロスコープ画面に表示(更新)する"""
    n = max(1, min(int(sample_rate * duration), len(wave)))
    t = np.arange(n) / sample_rate

    _line.set_data(t, wave[:n])
    _ax.set_xlim(0, t[-1])
    _ax.set_title(title)
    _fig.canvas.draw_idle()
    _fig.canvas.flush_events()
    plt.pause(0.001)


def keep_open():
    """プログラムの最後に呼ぶと、オシロスコープ画面を閉じるまで表示したままにする"""
    plt.ioff()
    plt.show()
