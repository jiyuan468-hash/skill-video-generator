# 平台快速参考

按平台选择正确的格式和模板。

## 平台速查表

| 平台 | 格式 | 分辨率 | 文件位置 |
|------|------|--------|----------|
| **YouTube** 长视频 | 16:9 | 1920×1080 | 	ext/youtube/ / code/youtube/ |
| **YouTube Shorts** | 9:16 | 1080×1920 | 	ext/youtube/ / code/youtube/ |
| **TikTok** | 9:16 | 1080×1920 | 	ext/tiktok/ / code/tiktok/ |
| **Instagram Reels** | 9:16 | 1080×1920 | 	ext/instagram/ / code/instagram/ |
| **Instagram Stories** | 9:16 | 1080×1920 | 	ext/instagram/ |
| **Instagram Feed** | 1:1 | 1080×1080 | 	ext/instagram/ |
| **Instagram Feed 竖版** | 4:5 | 1080×1350 | 	ext/instagram/ |
| **LinkedIn** | 16:9 | 1280×720 | 	ext/linkedin/ / code/linkedin/ |
| **X (Twitter)** | 16:9 | 1280×720 | 	ext/x/ / code/x/ |
| **Facebook** | 16:9 | 1280×720 | 	ext/facebook/ / code/facebook/ |
| **Pinterest** | 9:16 | 1000×1500 | 	ext/pinterest/ / code/pinterest/ |
| **Bilibili** | 16:9 | 1920×1080 | 	ext/bilibili/ / code/bilibili/ |

## 快速命令

`ash
# YouTube 长视频片头
python scripts/generate.py --mode template --input assets/templates/text/youtube/intro.txt --output video.mp4 --format 16:9

# TikTok 病毒式内容
python scripts/generate.py --mode template --input assets/templates/text/tiktok/hook_viral.txt --output video.mp4 --format 9:16

# Instagram Reels
python scripts/generate.py --mode template --input assets/templates/text/instagram/reels_lifestyle.txt --output video.mp4 --format 9:16

# Instagram Feed 方形
python scripts/generate.py --mode template --input assets/templates/text/instagram/feed_quote.txt --output video.mp4 --format 1:1

# LinkedIn 专业动态
python scripts/generate.py --mode template --input assets/templates/text/linkedin/professional_update.txt --output video.mp4 --format 16:9

# Bilibili 一键三连
python scripts/generate.py --mode code --script assets/templates/code/bilibili/three_clicks.py --output video.mp4 --format 9:16

# X/Twitter 推文预览
python scripts/generate.py --mode template --input assets/templates/text/x/thread_preview.txt --output video.mp4 --format 16:9
`

详细平台参考请查看 PLATFORMS.md。
