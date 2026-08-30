---
name: skill-video-generator
description: Generate videos from text, images, or code using three modes: template (text-to-video), AI (API-based generation), and code (scripted animation). Supports portrait and landscape aspect ratios.
---

# Skill Video Generator

Generate videos programmatically. Supports three modes—**template**, **AI**, and **code**—with configurable output formats.

## Mode Selection

| Mode | When to use | Input |
|------|-------------|-------|
| 	emplate | Subtitles, photo slideshows, text animations | Text, images, style preset |
| i | AI-generated video from prompts | Text prompt, aspect ratio, API key |
| code | Programmatic animations, motion graphics | Script or parameters, aspect ratio |

## Quick Start

`ash
python scripts/generate.py --mode template --input text.txt --output video.mp4
python scripts/generate.py --mode template --input images/*.png --output video.mp4 --format 9:16
python scripts/generate.py --mode code --script draw.py --output video.mp4
python scripts/generate.py --mode ai --prompt "a sunset over the ocean" --output video.mp4 --aspect 16:9
`

## Template Mode

Uses **moviepy** to compose videos from images or text overlays.

**Prerequisites:** pip install moviepy pillow

**Supported inputs:**
- Text file: one line per scene, rendered as centered text on a solid color background
- Image directory: images rendered as a slideshow with fade transitions
- Style presets: dark, light, gradient, custom

**Options:**
- --format 16:9 or --format 9:16 (default: 16:9)
- --duration N seconds per scene (default: 3)
- --style dark|light|gradient|custom
- --font-size (default: 48)
- --transition seconds fade duration (default: 0.5)

## Code Mode

Uses **ffmpeg-python** and **PIL** to generate frames programmatically, then compiles to video.

**Supported operations:**
- Drawing shapes, text, and gradients with PIL
- Applying FFmpeg filters (zoom, pan, color correction)
- Generating audio tracks from tone frequencies

**Input:** A Python script in scripts/code/ that defines the animation, or pass parameters directly.

## AI Mode

Calls external AI video APIs. Requires an API key configured in eferences/api-keys.md.

**Supported providers:**
- Runway Gen-3 (RUNWAY_API_KEY)
- Pika Labs (PIKA_API_KEY)
- Stability AI (STABILITY_API_KEY)

**Options:**
- --aspect 16:9|9:16|1:1
- --duration 5|10|15 (seconds, provider-dependent)
- --quality standard|high

## Output Formats

- 16:9 — YouTube, desktop (1920×1080)
- 9:16 — TikTok, Reels, Shorts (1080×1920)
- 1:1 — Instagram feed (1080×1080)
- 4:3 — Traditional (800×600)

## Project Structure

`
skill-video-generator/
├── SKILL.md
├── scripts/
│   ├── generate.py          # Unified entry point
│   ├── template_mode.py     # Template/text-to-video
│   ├── code_mode.py         # Code animation
│   └── ai_mode.py           # AI API generation
├── references/
│   ├── modes.md             # Detailed mode guide
│   └── api-keys.md          # API key setup
└── assets/
    └── templates/           # Default style templates
`

## Dependencies

`ash
# Core (template & code modes)
pip install moviepy pillow ffmpeg-python numpy

# AI mode (optional, uncomment provider as needed)
# pip install requests
`

## Validation

`ash
python scripts/generate.py --mode template --input text.txt --output test.mp4 --format 16:9
`

See eferences/modes.md for detailed examples and eferences/api-keys.md for API configuration.
