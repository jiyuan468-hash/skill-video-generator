#!/usr/bin/env python3
\"\"\"
Video Generator — unified entry point for skill-video-generator.

Modes:
  template  — text/images → video using moviepy
  code      — programmatic animation using PIL + ffmpeg-python
  ai        — AI generation via external APIs

Usage:
  python scripts/generate.py --mode template --input text.txt --output video.mp4
  python scripts/generate.py --mode code    --script draw.py --output video.mp4
  python scripts/generate.py --mode ai      --prompt \"sunset\" --output video.mp4
\"\"\"

import argparse
import sys
import os

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPTS_DIR)


def main():
    parser = argparse.ArgumentParser(
        description=\"Generate videos using template, code, or AI modes.\",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        \"--mode\", \"-m\",
        choices=[\"template\", \"code\", \"ai\"],
        required=True,
        help=\"Generation mode: template, code, or ai\",
    )
    parser.add_argument(
        \"--output\", \"-o\",
        required=True,
        help=\"Output video file path (e.g. video.mp4)\",
    )
    # Template mode args
    parser.add_argument(
        \"--input\", \"-i\",
        help=\"Input text file or image directory for template mode\",
    )
    parser.add_argument(
        \"--format\", \"-f\",
        choices=[\"16:9\", \"9:16\", \"1:1\", \"4:3\"],
        default=\"16:9\",
        help=\"Aspect ratio (default: 16:9)\",
    )
    parser.add_argument(
        \"--duration\", \"-d\",
        type=float,
        default=3.0,
        help=\"Seconds per scene in template mode (default: 3)\",
    )
    parser.add_argument(
        \"--style\",
        choices=[\"dark\", \"light\", \"gradient\", \"custom\"],
        default=\"dark\",
        help=\"Background style for template mode (default: dark)\",
    )
    parser.add_argument(
        \"--font-size\",
        type=int,
        default=48,
        help=\"Font size for text scenes (default: 48)\",
    )
    parser.add_argument(
        \"--transition\",
        type=float,
        default=0.5,
        help=\"Fade transition duration in seconds (default: 0.5)\",
    )
    # Code mode args
    parser.add_argument(
        \"--script\",
        help=\"Path to Python animation script for code mode\",
    )
    # AI mode args
    parser.add_argument(
        \"--prompt\", \"-p\",
        help=\"Text prompt for AI video generation\",
    )
    parser.add_argument(
        \"--provider\",
        choices=[\"runway\", \"pika\", \"stability\"],
        default=\"runway\",
        help=\"AI provider (default: runway)\",
    )
    parser.add_argument(
        \"--ai-duration\",
        type=int,
        default=5,
        help=\"Duration in seconds for AI generation (default: 5)\",
    )
    parser.add_argument(
        \"--quality\",
        choices=[\"standard\", \"high\"],
        default=\"standard\",
        help=\"AI generation quality (default: standard)\",
    )

    args = parser.parse_args()

    # Validate mode-specific required args
    if args.mode == \"template\" and not args.input:
        parser.error(\"--input is required for template mode\")
    if args.mode == \"code\" and not args.script:
        parser.error(\"--script is required for code mode\")
    if args.mode == \"ai\" and not args.prompt:
        parser.error(\"--prompt is required for ai mode\")

    # Map aspect ratio to (width, height)
    RESOLUTIONS = {
        \"16:9\": (1920, 1080),
        \"9:16\": (1080, 1920),
        \"1:1\": (1080, 1080),
        \"4:3\": (800, 600),
    }
    width, height = RESOLUTIONS[args.format]

    if args.mode == \"template\":
        from template_mode import generate as template_generate
        template_generate(
            input_path=args.input,
            output_path=args.output,
            resolution=(width, height),
            duration=args.duration,
            style=args.style,
            font_size=args.font_size,
            transition=args.transition,
        )
    elif args.mode == \"code\":
        from code_mode import generate as code_generate
        code_generate(
            script_path=args.script,
            output_path=args.output,
            resolution=(width, height),
        )
    elif args.mode == \"ai\":
        from ai_mode import generate as ai_generate
        ai_generate(
            prompt=args.prompt,
            output_path=args.output,
            resolution=(width, height),
            provider=args.provider,
            duration=args.ai_duration,
            quality=args.quality,
        )

    print(f\"Video saved to: {args.output}\")


if __name__ == \"__main__\":
    main()
