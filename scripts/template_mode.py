#!/usr/bin/env python3
import os, glob
from pathlib import Path

def find_font(size=48):
    for fp in ["C:/Windows/Fonts/arial.ttf","C:/Windows/Fonts/times.ttf","C:/Windows/Fonts/impact.ttf"]:
        if os.path.exists(fp): return fp
    return None

def generate(input_path, output_path, resolution, duration=3.0, style="dark", font_size=48, transition=0.5):
    from moviepy import TextClip, ImageClip, CompositeVideoClip, ColorClip, concatenate_videoclips
    w, h = resolution
    font_path = find_font(font_size)
    bg_colors = {"dark":(18,18,24), "light":(245,245,250)}
    bg_color = bg_colors.get(style, (18,18,24))
    input_path = Path(input_path)
    if input_path.is_dir():
        images = sorted([img for img in glob.glob(os.path.join(input_path, "*")) if img.lower().endswith((".png",".jpg",".jpeg",".webp"))])
        if not images: raise ValueError(f"No images in {input_path}")
        clips = [ImageClip(img).resize(newsize=(w,h)).with_duration(duration) for img in images]
        video = concatenate_videoclips(clips, method="compose") if len(clips) > 1 else clips[0]
    elif input_path.is_file():
        with open(input_path, "r", encoding="utf-8") as f:
            tlines = [l.strip() for l in f if l.strip()]
        clips = []
        for i, txt in enumerate(tlines):
            bg = ColorClip(size=(w,h), color=bg_color, duration=duration)
            tc = TextClip(text=txt, font_size=font_size, color="white", font=font_path, size=(w-100,h-100), method="caption")
            tc = tc.with_position("center").with_duration(duration)
            scene = CompositeVideoClip([bg, tc])
            clips.append(scene)
        video = concatenate_videoclips(clips, method="compose")
    else:
        raise FileNotFoundError(input_path)
    video.write_videofile(output_path, fps=30, codec="libx264", audio=False, preset="medium")
    return output_path