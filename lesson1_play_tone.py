# lesson1_play_tone.py
# 第1回: 音を鳴らす基本
#
# winsound という標準ライブラリを使って、決まった高さの音(ビープ音)を鳴らします。

import winsound

# winsound.Beep(周波数[Hz], 鳴らす時間[ミリ秒])
# 周波数が高いほど高い音、低いほど低い音になります。
winsound.Beep(440, 1000)  # 440Hz(ラの音)を1秒間鳴らす
