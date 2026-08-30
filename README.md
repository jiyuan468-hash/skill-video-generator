# Skill Video Generator

An automated video generation skill for Codex. Create videos from text, images, or code using three modes.

## Modes

- **Template**: Text and images → video (subtitles, slideshows)
- **Code**: Programmatic animation (motion graphics, shapes)
- **AI**: External API generation (Runway, Pika, Stability AI)

## Quick Start

`ash
# Install dependencies
pip install moviepy pillow ffmpeg-python numpy requests

# Template mode (text)
python scripts/generate.py --mode template --input scenes.txt --output video.mp4

# Template mode (images)
python scripts/generate.py --mode template --input images/ --output video.mp4

# Code mode
python scripts/generate.py --mode code --script scripts/code/draw.py --output video.mp4

# AI mode (requires API key)
python scripts/generate.py --mode ai --prompt \"sunset\" --output video.mp4
`

## Output Formats

- --format 16:9 — YouTube, desktop (1920×1080)
- --format 9:16 — TikTok, Reels, Shorts (1080×1920)
- --format 1:1 — Instagram feed (1080×1080)

## Requirements

- Python 3.10+
- FFmpeg (installed separately: rew install ffmpeg or from https://ffmpeg.org)
- API keys for AI mode (see eferences/api-keys.md)

## Project Structure

`
skill-video-generator/
├── SKILL.md              # Skill instructions
├── scripts/
│   ├── generate.py       # Entry point
│   ├── template_mode.py  # Template/text-to-video
│   ├── code_mode.py      # Code animation
│   └── ai_mode.py        # AI generation
├── references/
│   ├── modes.md          # Mode documentation
│   └── api-keys.md       # API key setup
└── assets/
    └── templates/        # Style templates
`

## License

MIT
