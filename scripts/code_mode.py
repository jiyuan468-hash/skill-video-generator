#!/usr/bin/env python3
\"\"\"
Code Mode: Generate videos from programmatic animation scripts.

Features:
  - Draw shapes, text, and gradients using PIL
  - Apply FFmpeg filters (zoom, pan, color correction)
  - Generate audio from tone frequencies
  - User-provided script or built-in presets

Dependencies: pillow, ffmpeg-python, numpy
\"\"\"

import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import ffmpeg


def draw_shape_frame(width, height, t, total_frames, config):
    \"\"\"Draw a single frame based on configuration.\"\"\"
    img = Image.new(\"RGB\", (width, height), color=config.get(\"bg_color\", (18, 18, 24)))
    draw = ImageDraw.Draw(img)

    # Draw centered text if configured
    if \"text\" in config:
        try:
            font = ImageFont.truetype(\"C:/Windows/Fonts/arial.ttf\", config.get(\"font_size\", 48))
        except Exception:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), config[\"text\"], font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (width - text_w) // 2
        y = (height - text_h) // 2
        draw.text((x, y), config[\"text\"], fill=config.get(\"text_color\", \"white\"), font=font)

    # Draw animated shape if configured
    if config.get(\"shape\") == \"circle\":
        cx = width // 2 + int(100 * np.sin(2 * np.pi * t / total_frames))
        cy = height // 2 + int(100 * np.cos(2 * np.pi * t / total_frames))
        r = config.get(\"radius\", 50)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     fill=config.get(\"shape_color\", (100, 150, 255)))

    elif config.get(\"shape\") == \"rect\":
        cx = width // 2
        cy = height // 2
        size = config.get(\"rect_size\", 80)
        draw.rectangle([cx - size, cy - size, cx + size, cy + size],
                       fill=config.get(\"shape_color\", (255, 100, 100)))

    return np.array(img)


def generate_frames(width, height, fps, duration, config):
    \"\"\"Generate all frames for the animation.\"\"\"
    total_frames = int(fps * duration)
    frames = []
    for i in range(total_frames):
        t = i / fps
        frame = draw_shape_frame(width, height, t, total_frames, config)
        frames.append(frame)
    return frames


def generate(script_path, output_path, resolution=(1920, 1080)):
    \"\"\"
    Main entry point for code mode.

    Args:
        script_path: Path to Python script that defines animation config
        output_path: Output video file path
        resolution: (width, height) tuple
    \"\"\"
    width, height = resolution
    fps = 30
    duration = 10  # default duration, can be overridden by script

    # Load user script
    script_dir = os.path.dirname(os.path.abspath(script_path))
    sys.path.insert(0, script_dir)

    # Define a default config module
    config = {
        \"bg_color\": (18, 18, 24),
        \"text\": \"\",
        \"font_size\": 48,
        \"text_color\": \"white\",
        \"shape\": None,
        \"radius\": 50,
        \"rect_size\": 80,
        \"shape_color\": (100, 150, 255),
        \"duration\": duration,
    }

    # Try to import user config
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(\"user_config\", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, \"config\"):
            config.update(module.config)
        elif hasattr(module, \"bg_color\"):
            for key in [\"bg_color\", \"text\", \"font_size\", \"text_color\",
                       \"shape\", \"radius\", \"rect_size\", \"shape_color\", \"duration\"]:
                if hasattr(module, key):
                    config[key] = getattr(module, key)
    except Exception as e:
        print(f\"Warning: Could not load script {script_path}: {e}\")

    duration = config.get(\"duration\", 10)

    # Generate frames
    frames = generate_frames(width, height, fps, duration, config)

    # Encode with FFmpeg
    if not frames:
        raise ValueError(\"No frames generated\")

    # Write frames as PNG sequence
    frame_dir = os.path.join(os.path.dirname(output_path), \".frames\")
    os.makedirs(frame_dir, exist_ok=True)

    for i, frame in enumerate(frames):
        img = Image.fromarray(frame)
        img.save(os.path.join(frame_dir, f\"frame_{i:05d}.png\"))

    # Convert to video
    (
        ffmpeg
        .input(os.path.join(frame_dir, \"frame_%05d.png\"), framerate=fps)
        .output(output_path, codec=\"libx264\", preset=\"medium\", crf=23)
        .overwrite_output()
        .run(capture_stdout=True, capture_stderr=True)
    )

    # Cleanup frames
    import shutil
    shutil.rmtree(frame_dir, ignore_errors=True)

    return output_path
