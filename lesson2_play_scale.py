# lesson2_play_scale.py
# 第2回: 音階の演奏
#
# リストと for文を使って、ドレミファソラシドを順番に鳴らします。

import winsound

# ドレミファソラシド の周波数(Hz)をリストに入れる
notes = [262, 294, 330, 349, 392, 440, 494, 523]

# リストの中身を先頭から順番に取り出して鳴らす
for freq in notes:
    winsound.Beep(freq, 500)  # 0.5秒ずつ鳴らす
