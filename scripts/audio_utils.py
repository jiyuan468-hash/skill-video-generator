#!/usr/bin/env python3
"""Audio support for skill-video-generator."""
import os
import numpy as np

def generate_tone(frequency=440, duration=1.0, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    fade_len = int(sample_rate * 0.05)
    fade_in = np.linspace(0, 1, fade_len)
    fade_out = np.linspace(1, 0, fade_len)
    wave[:fade_len] *= fade_in
    wave[-fade_len:] *= fade_out
    return wave, sample_rate

def add_audio_to_video(video_path, audio_path, output_path):
    import ffmpeg
    (ffmpeg.input(video_path).input(audio_path).output(output_path,
        codec="libx264", audio_codec="aac", shortest=True)
     .overwrite_output().run(capture_stdout=True, capture_stderr=True))
    return output_path

def tts_to_audio(text, output_path, rate=150):
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("rate", rate)
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        return output_path
    except ImportError:
        print("Install pyttsx3: pip install pyttsx3")
        return None