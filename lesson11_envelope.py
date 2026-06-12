# lesson11_envelope.py
# 第11回: エンベロープ
#
# 音の立ち上がり(フェードイン)と減衰(フェードアウト)を追加します。
# これにより、音の始まりと終わりが「ブツッ」とならず、なめらかになります。

import numpy as np
import sounddevice as sd
import keyboard

sample_rate = 44100


def apply_envelope(wave, fade_ratio=0.1):
    """波の最初と最後をなめらかに変化させる(フェードイン・フェードアウト)"""
    n = len(wave)
    fade_len = int(n * fade_ratio)

    envelope = np.ones(n)
    envelope[:fade_len] = np.linspace(0, 1, fade_len)   # フェードイン(音量0→1)
    envelope[-fade_len:] = np.linspace(1, 0, fade_len)  # フェードアウト(音量1→0)

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


key_to_freq = {
    "a": 262, "s": 294, "d": 330, "f": 349,
    "g": 392, "h": 440, "j": 494, "k": 523,
}

print("A〜Kのキーで音階が鳴ります。音の始まりと終わりがなめらかになりました。ESCキーで終了します。")

while True:
    for key, freq in key_to_freq.items():
        if keyboard.is_pressed(key):
            play_wave(freq, 0.5)

    if keyboard.is_pressed("esc"):
        break
