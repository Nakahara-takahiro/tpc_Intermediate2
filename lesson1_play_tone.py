# lesson1_play_tone.py
# 第1回: 音を鳴らす基本
#
# tone モジュールにある play_tone 関数を使って、決まった高さの音を鳴らします。
# 中でどうやって音を作っているかは、まだ知らなくて大丈夫です(第3回で明かします)。
# あわせて oscilloscope モジュールを使い、鳴らした音の波形を画面に表示します。

from tone import play_tone
from oscilloscope import show_waveform, keep_open

# play_tone(周波数[Hz], 鳴らす時間[秒])
# 周波数が高いほど高い音、低いほど低い音になります。
wave = play_tone(440, 1.0)  # 440Hz(ラの音)を1秒間鳴らす

show_waveform(wave, 44100, title="440Hz")
keep_open()  # 画面を閉じるまで波形を表示したままにする
