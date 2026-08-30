#!/usr/bin/env python3
\"\"\"
Template Mode: Generate videos from text files or image directories.

Features:
  - Text file input: one line per scene, rendered as centered text
  - Image directory input: slideshow with fade transitions
  - Multiple background styles: dark, light, gradient, custom
  - Configurable resolution, duration, font size, and transitions

Dependencies: moviepy, pillow
\"\"\"

import os
import glob
from pathlib import Path

from moviepy.editor import (
    TextClip,
    ImageClip,
    CompositeVideoClip,
    ColorClip,
    concatenate_videoclips,
)


# Background color presets
STYLES = {
    \"dark\":    (18, 18, 24),
    \"light\":   (245, 245, 250),
    \"gradient\": \"gradient\",  # handled specially
    \"custom\":  None,
}

# Common fonts (check what's available on the system)
FONTS = [
    \"Arial\",
    \"Helvetica\",
    \"Times New Roman\",
    \"Georgia\",
    \"Courier New\",
]


def find_font(size=48):
    \"\"\"Find a suitable font file for the system.\"\"\"
    import shutil
    candidates = [
        \"C:/Windows/Fonts/arial.ttf\",
        \"C:/Windows/Fonts/times.ttf\",
        \"C:/Windows/Fonts/impact.ttf\",
        \"C:/Windows/Fonts/verdana.ttf\",
    ]
    for font_path in candidates:
        if os.path.exists(font_path):
            return font_path
    return None


def generate_text_scene(text, resolution, duration, bg_color, font_size, font_path=None):
    \"\"\"Create a single text scene as a VideoClip.\"\"\"
    w, h = resolution

    # Create background
    bg = ColorClip(size=(w, h), color=bg_color, duration=duration)

    # Create text clip
    try:
        text_clip = TextClip(
            text,
            fontsize=font_size,
            color=\"white\",
            font=font_path.replace(\"\\\\\", \"/\") if font_path else None,
            size=(w - 100, h - 100),
            method=\"caption\",
        )
    except Exception:
        # Fallback: use default font
        text_clip = TextClip(
            text,
            fontsize=font_size,
            color=\"white\",
            method=\"caption\",
        )

    text_clip = text_clip.set_position(\"center\").set_duration(duration)
    video = CompositeVideoClip([bg, text_clip])
    return video


def generate_gradient_scene(text, resolution, duration, font_size, font_path=None):
    \"\"\"Create a gradient background scene with text overlay.\"\"\"
    w, h = resolution
    import numpy as np

    # Create gradient frames
    frame = np.zeros((h, w, 3), dtype=float)
    for y in range(h):
        ratio = y / h
        frame[y, :, 0] = 18 + (245 - 18) * ratio * 0.3
        frame[y, :, 1] = 18 + (245 - 18) * ratio * 0.2
        frame[y, :, 2] = 24 + (250 - 24) * ratio * 0.1
    frame = np.clip(frame, 0, 255).astype(np.uint8)

    from moviepy.video.io.VideoFileClip import VideoFileClip
    # Build gradient clip
    import moviepy.video.fx.all as vfx
    from moviepy.video.io.bindings import mplfig_to_npimage
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(w / 100, h / 100), dpi=100)
    gradient = plt.imshow(
        np.linspace([[18, 18, 24], [245, 245, 250]], h, axis=0),
        extent=[0, w, 0, h],
        aspect=\"auto\",
    )
    ax.set_axis_off()
    fig.tight_layout(pad=0)

    def make_frame(t):
        # Simple vertical gradient
        y_ratio = t / duration
        return np.linspace([[18, 18, 24], [250, 250, 255]], 1, h).astype(np.uint8)

    # Simpler approach: create gradient as image sequence
    n_frames = int(duration * 30)
    frames = []
    for i in range(n_frames):
        row = int((i / n_frames) * h)
        color = [
            int(18 + (250 - 18) * (row / h)),
            int(18 + (250 - 18) * (row / h)),
            int(24 + (255 - 24) * (row / h)),
        ]
        frame = np.full((h, w, 3), color, dtype=np.uint8)
        frames.append(frame)

    from moviepy.video.VideoClip import ImageClip
    grad_clip = ImageClip(frames[0]).with_duration(duration)
    grad_clip = grad_clip.set_mask(None)

    # Create text on top
    try:
        text_clip = TextClip(
            text,
            fontsize=font_size,
            color=\"white\",
            font=font_path.replace(\"\\\\\", \"/\") if font_path else None,
            size=(w - 100, h - 100),
            method=\"caption\",
        )
    except Exception:
        text_clip = TextClip(text, fontsize=font_size, color=\"white\", method=\"caption\")

    text_clip = text_clip.set_position(\"center\").set_duration(duration)
    return CompositeVideoClip([grad_clip, text_clip])


def generate_from_text(input_path, resolution, duration, style, font_size, font_path, transition):
    \"\"\"Generate video from a text file (one line per scene).\"\"\"
    scenes = []
    with open(input_path, \"r\", encoding=\"utf-8\") as f:
        lines = [line.strip() for line in f if line.strip()]

    bg_color = STYLES.get(style, (18, 18, 24))

    for i, line in enumerate(lines):
        if style == \"gradient\":
            scene = generate_gradient_scene(line, resolution, duration, font_size, font_path)
        else:
            scene = generate_text_scene(line, resolution, duration, bg_color, font_size, font_path)

        # Add transition (fade out/in) between scenes
        if transition > 0 and i > 0:
            try:
                import moviepy.video.fx.all as vfx
                scene = scene.with_effects([vfx.fadein(transition)])
            except Exception:
                pass

        scenes.append(scene)

    if len(scenes) == 1:
        return scenes[0]

    final = concatenate_videoclips(scenes, method=\"compose\")
    return final


def generate_from_images(input_path, resolution, duration, style, transition):
    \"\"\"Generate slideshow video from an image directory.\"\"\"
    images = sorted(glob.glob(os.path.join(input_path, \"*\")))
    images = [img for img in images if img.lower().endswith((\".png\", \".jpg\", \".jpeg\", \".webp\"))]

    if not images:
        raise ValueError(f\"No images found in {input_path}\")

    w, h = resolution
    bg_color = STYLES.get(style, (18, 18, 24))

    clips = []
    for img_path in images:
        try:
            clip = ImageClip(img_path).resize(newsize=(w, h))
        except Exception:
            # If image doesn't match resolution, create colored bg with image centered
            bg = ColorClip(size=(w, h), color=bg_color, duration=duration)
            img_clip = ImageClip(img_path)
            img_w, img_h = img_clip.size
            clip = CompositeVideoClip([
                bg,
                img_clip.set_position(\"center\")
            ]).with_duration(duration)
        clip = clip.with_duration(duration)
        clips.append(clip)

    if len(clips) == 1:
        return clips[0]

    final = concatenate_videoclips(clips, method=\"compose\")
    return final


def generate(input_path, output_path, resolution, duration=3.0, style=\"dark\",
             font_size=48, transition=0.5):
    \"\"\"
    Main entry point for template mode.

    Args:
        input_path: Path to text file or image directory
        output_path: Output video file path
        resolution: (width, height) tuple
        duration: Seconds per scene
        style: Background style (dark, light, gradient, custom)
        font_size: Font size for text scenes
        transition: Fade transition duration in seconds
    \"\"\"
    font_path = find_font(font_size)

    input_path = Path(input_path)

    if input_path.is_dir():
        video = generate_from_images(str(input_path), resolution, duration, style, transition)
    elif input_path.is_file():
        video = generate_from_text(str(input_path), resolution, duration, style, font_size, font_path, transition)
    else:
        raise FileNotFoundError(f\"Input path not found: {input_path}\")

    video.write_videofile(
        output_path,
        fps=30,
        codec=\"libx264\",
        audio=False,
        preset=\"medium\",
    )

    return output_path
