# lesson2_play_scale.py
# 第2回: 音階の演奏
#
# リストと for文を使って、ドレミファソラシドを順番に鳴らします。
# あわせて oscilloscope モジュールを使い、鳴らしている音の波形を画面に表示します。

from tone_util import play_tone
from oscilloscope import show_waveform, keep_open

# ドレミファソラシド の周波数(Hz)をリストに入れる
notes = [262, 294, 330, 349, 392, 440, 494, 523]

# リストの中身を先頭から順番に取り出して鳴らす
for freq in notes:
    wave = play_tone(freq, 0.5)  # 0.5秒ずつ鳴らす
    show_waveform(wave, 44100, title=f"{freq}Hz")

keep_open()  # 画面を閉じるまで波形を表示したままにする
