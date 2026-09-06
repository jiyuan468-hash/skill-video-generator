# Skill Video Generator

一个 Codex Skill，通过文本、图片或代码自动生成视频。支持 **11 个平台**，**93+ 模板**。

## 支持的网站/平台

| 平台 | 模板数 | 格式 |
|------|--------|------|
| 抖音 | 9 | 9:16 竖屏 |
| 小红书 | 9 | 4:5 竖屏 |
| 快手 | 9 | 9:16 竖屏 |
| TikTok | 8 | 9:16 竖屏 |
| YouTube | 10 | 16:9 横屏 |
| Instagram | 11 | 多格式 |
| LinkedIn | 5 | 16:9 横屏 |
| Bilibili | 7 | 16:9 横屏 |
| Pinterest | 4 | 4:5 / 16:9 |
| X (Twitter) | 3 | 16:9 横屏 |
| Facebook | 3 | 16:9 横屏 |
| 通用 | 10 | 默认比例 |

## 快速开始

```bash
# 安装依赖
pip install moviepy pillow ffmpeg-python numpy requests

# 克隆仓库
git clone https://github.com/jiyuan468-hash/skill-video-generator.git
cd skill-video-generator

# 文本模板 → 视频
python scripts/generate.py --mode template \
  --input assets/templates/text/douyin/viral_hook.txt \
  --output video.mp4 --format 9:16

# 动画模板 → 视频
python scripts/generate.py --mode code \
  --script assets/templates/code/douyin/neon_pulse.py \
  --output video.mp4 --format 9:16
```

## 三种生成模式

### 1. Template 模式（文本/图片 → 视频）
将文字内容分段，每段生成一个视频画面，支持字幕、幻灯片效果。

### 2. Code 模式（代码 → 动画视频）
通过 Python 脚本控制图形、颜色、动画，生成动态视频。

### 3. AI 模式（AI API → 视频）
调用 Runway / Pika / Stability AI 生成 AI 视频（需配置 API Key）。

## 输出格式

| 格式参数 | 尺寸 | 适用平台 |
|----------|------|----------|
| `--format 9:16` | 1080×1920 | 抖音、快手、TikTok、Reels |
| `--format 4:5` | 1080×1350 | 小红书、Instagram 帖子 |
| `--format 16:9` | 1920×1080 | YouTube、LinkedIn、X |
| `--format 1:1` | 1080×1080 | Instagram 帖子 |

## 项目结构

```
skill-video-generator/
├── SKILL.md              # Codex Skill 说明
├── README.md             # 本文档
├── requirements.txt      # Python 依赖
├── scripts/
│   ├── generate.py       # 主入口
│   ├── template_mode.py  # 文本/图片生成
│   ├── code_mode.py      # 代码动画
│   ├── ai_mode.py        # AI 视频生成
│   └── audio_utils.py    # 音频工具
├── assets/templates/
│   ├── text/             # 文本模板（按平台分类）
│   ├── code/             # 代码动画模板
│   └── images/           # 图片模板目录
├── references/
│   ├── modes.md          # 模式详细说明
│   └── api-keys.md       # API Key 配置指南
├── tests/
│   └── test_generate.py  # 单元测试
└── website/
    └── index.html        # 网页版模板浏览器
```

## 网页版

运行本地服务器浏览所有模板：

```bash
cd website
python -m http.server 8888
```

然后访问 http://localhost:8888

**在线版**（GitHub Pages）：
https://jiyuan468-hash.github.io/skill-video-generator/

## 测试

```bash
python -m pytest tests/ -v
```

## 依赖

- Python 3.10+
- FFmpeg（[安装指南](https://ffmpeg.org/download.html)）
- `pip install -r requirements.txt`

## License

MIT
