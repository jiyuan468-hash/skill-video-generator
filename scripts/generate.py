#!/usr/bin/env python3
import argparse, sys, os

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    parser = argparse.ArgumentParser(description="Generate videos")
    parser.add_argument("--mode", "-m", choices=["template","code","ai"], required=True)
    parser.add_argument("--output", "-o", required=True)
    parser.add_argument("--input", "-i")
    parser.add_argument("--format", "-f", choices=["16:9","9:16","1:1","4:3"], default="16:9")
    parser.add_argument("--duration", "-d", type=float, default=3.0)
    parser.add_argument("--style", choices=["dark","light","gradient","custom"], default="dark")
    parser.add_argument("--font-size", type=int, default=48)
    parser.add_argument("--transition", type=float, default=0.5)
    parser.add_argument("--script")
    parser.add_argument("--prompt", "-p")
    parser.add_argument("--provider", choices=["runway","pika","stability"], default="runway")
    parser.add_argument("--ai-duration", type=int, default=5)
    parser.add_argument("--quality", choices=["standard","high"], default="standard")
    args = parser.parse_args()
    if args.mode == "template" and not args.input: parser.error("--input required for template mode")
    if args.mode == "code" and not args.script: parser.error("--script required for code mode")
    if args.mode == "ai" and not args.prompt: parser.error("--prompt required for ai mode")
    res = {"16:9":(1920,1080),"9:16":(1080,1920),"1:1":(1080,1080),"4:3":(800,600)}
    w, h = res[args.format]
    if args.mode == "template":
        from template_mode import generate as g
        g(args.input, args.output, (w,h), args.duration, args.style, args.font_size, args.transition)
    elif args.mode == "code":
        from code_mode import generate as g
        g(args.script, args.output, (w,h))
    elif args.mode == "ai":
        from ai_mode import generate as g
        g(args.prompt, args.output, (w,h), args.provider, args.ai_duration, args.quality)
    print(f"Video saved to: {args.output}")

if __name__ == "__main__":
    main()