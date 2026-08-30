# Modes Reference

## Template Mode

Best for: subtitles, photo slideshows, text animations, title cards

### Text Input
Create a .txt file with one line per scene:
`
Hello World
This is scene two
Final slide
`

### Image Input
Place images in a folder:
`
assets/images/
├── slide1.png
├── slide2.jpg
└── slide3.png
`

### Commands
`ash
# Basic text video
python scripts/generate.py --mode template --input scenes.txt --output video.mp4

# Portrait format (TikTok/Reels)
python scripts/generate.py --mode template --input scenes.txt --output video.mp4 --format 9:16

# Slideshow
python scripts/generate.py --mode template --input images/ --output video.mp4 --format 16:9

# Custom duration and style
python scripts/generate.py --mode template --input scenes.txt --output video.mp4 --duration 5 --style light
`

### Style Options
| Style | Background |
|-------|-----------|
| dark | Near-black (#121218) |
| light | Off-white (#F5F5FA) |
| gradient | Vertical dark-to-light gradient |
| custom | Use your own background |

---

## Code Mode

Best for: motion graphics, data visualizations, branded animations

### Script Structure
Create a Python script in scripts/code/:
`python
# scripts/code/my_animation.py
config = {
    \"bg_color\": (20, 20, 30),
    \"text\": \"Hello from Code Mode!\",
    \"font_size\": 64,
    \"text_color\": \"#4FC3F7\",
    \"shape\": \"circle\",
    \"radius\": 80,
    \"shape_color\": (255, 100, 100),
    \"duration\": 8,
}
`

### Commands
`ash
python scripts/generate.py --mode code --script scripts/code/my_animation.py --output video.mp4
`

---

## AI Mode

Best for: photorealistic videos, creative concepts, complex scenes

### API Key Setup
See pi-keys.md for configuration.

### Commands
`ash
# Basic generation
python scripts/generate.py --mode ai --prompt \"a cat walking in the rain\" --output video.mp4

# Portrait format
python scripts/generate.py --mode ai --prompt \"mountain sunset\" --output video.mp4 --format 9:16

# Custom duration
python scripts/generate.py --mode ai --prompt \"ocean waves\" --output video.mp4 --ai-duration 10
`

### Provider Comparison
| Provider | Speed | Quality | Best For |
|----------|-------|---------|----------|
| Runway | Fast | High | General use |
| Pika | Fast | Medium | Stylized content |
| Stability AI | Medium | High | Photorealistic |
