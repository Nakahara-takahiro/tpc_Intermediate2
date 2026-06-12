# lesson12_mini_synth.py
# 第12回: 完成・発表
#
# これまでの全機能を統合したミニシンセサイザーです。
# - ミニ鍵盤(キー入力で演奏)
# - 音色切替(sine/square/triangle)
# - エンベロープ(なめらかな音の始まり・終わり)
# - メロディの自動演奏

import numpy as np
import sounddevice as sd
import keyboard
import time

sample_rate = 44100


def apply_envelope(wave, fade_ratio=0.1):
    """波の最初と最後をなめらかに変化させる(フェードイン・フェードアウト)"""
    n = len(wave)
    fade_len = int(n * fade_ratio)
    envelope = np.ones(n)
    envelope[:fade_len] = np.linspace(0, 1, fade_len)
    envelope[-fade_len:] = np.linspace(1, 0, fade_len)
    return wave * envelope


def make_wave(frequency, duration, wave_type="sine"):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sine_wave = np.sin(2 * np.pi * frequency * t)
    if wave_type == "sine":
        wave = sine_wave
    elif wave_type == "square":
        wave = np.sign(sine_wave)
    elif wave_type == "triangle":
        wave = (2 / np.pi) * np.arcsin(sine_wave)
    else:
        raise ValueError(f"unknown wave_type: {wave_type}")
    return apply_envelope(wave)


def play_wave(frequency, duration, wave_type="sine"):
    wave = make_wave(frequency, duration, wave_type)
    sd.play(wave, sample_rate)
    sd.wait()


# キー -> 周波数(Hz) の対応表(ドレミファソラシド)
key_to_freq = {
    "a": 262, "s": 294, "d": 330, "f": 349,
    "g": 392, "h": 440, "j": 494, "k": 523,
}

# 音色を切り替えるキー
wave_type = "sine"
wave_keys = {"1": "sine", "2": "square", "3": "triangle"}

# メロディの自動演奏(きらきら星の最初の部分)
melody = ["a", "a", "g", "g", "f", "f", "g"]


def play_melody():
    print("メロディを演奏します")
    for key in melody:
        play_wave(key_to_freq[key], 0.4, wave_type)


print("=== ミニシンセサイザー ===")
print("A〜Kキー: 演奏 / 1,2,3キー: 音色切替(sine/square/triangle) / Mキー: メロディ再生 / ESCキー: 終了")

while True:
    # 音色の切り替え
    for k, wt in wave_keys.items():
        if keyboard.is_pressed(k):
            wave_type = wt
            print(f"音色を {wave_type} に切り替えました")
            time.sleep(0.2)

    # 鍵盤の演奏
    for key, freq in key_to_freq.items():
        if keyboard.is_pressed(key):
            play_wave(freq, 0.3, wave_type)

    # メロディの自動演奏
    if keyboard.is_pressed("m"):
        play_melody()
        time.sleep(0.2)

    if keyboard.is_pressed("esc"):
        break

print("終了しました")
