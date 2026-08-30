# Platform Template Reference

Complete reference for all platform templates in this repository.

## Format Quick Reference

| Platform | Format | Resolution | Best Use |
|----------|--------|-----------|----------|
| YouTube Long | 16:9 | 1920x1080 | In-depth tutorials, reviews |
| YouTube Shorts | 9:16 | 1080x1920 | Quick tips, hooks |
| TikTok | 9:16 | 1080x1920 | Viral content, trends |
| Instagram Reels | 9:16 | 1080x1920 | Lifestyle, product demos |
| Instagram Stories | 9:16 | 1080x1920 | Polls, countdowns |
| Instagram Feed | 1:1 | 1080x1080 | Quotes, tips, carousels |
| Instagram Feed Portrait | 4:5 | 1080x1350 | Personal brand |
| LinkedIn | 16:9 | 1280x720 | Professional updates, case studies |
| X (Twitter) | 16:9 | 1280x720 | Thread previews, hot takes |
| Facebook | 16:9 | 1280x720 | Events, testimonials |
| Pinterest | 9:16 | 1000x1500 | Recipes, DIY, lists |
| Bilibili | 16:9 | 1920x1080 | Tutorials, intros, outros |

## Template Directory Structure

\assets/templates/
├── QUICK_REF.md
├── PLATFORMS.md
├── text/
│   ├── youtube/      (8 templates)
│   ├── tiktok/       (6 templates)
│   ├── instagram/    (8 templates)
│   ├── linkedin/     (4 templates)
│   ├── pinterest/    (3 templates)
│   ├── x/            (2 templates)
│   ├── facebook/     (2 templates)
│   └── bilibili/     (4 templates)
├── code/
│   ├── youtube/      (2 templates)
│   ├── tiktok/       (2 templates)
│   ├── instagram/    (3 templates)
│   ├── linkedin/     (1 template)
│   ├── pinterest/    (1 template)
│   ├── x/            (1 template)
│   ├── facebook/     (1 template)
│   └── bilibili/     (2 templates)
└── images/
    └── README.md
\
## Usage Examples

### Platform-Specific Commands

\\ash
# YouTube long-form intro
python scripts/generate.py --mode template   --input assets/templates/text/youtube/intro.txt   --output video.mp4 --format 16:9

# TikTok viral hook
python scripts/generate.py --mode template   --input assets/templates/text/tiktok/hook_viral.txt   --output video.mp4 --format 9:16

# Instagram Reels lifestyle
python scripts/generate.py --mode template   --input assets/templates/text/instagram/reels_lifestyle.txt   --output reels.mp4 --format 9:16

# Instagram Feed quote (square)
python scripts/generate.py --mode template   --input assets/templates/text/instagram/feed_quote.txt   --output post.mp4 --format 1:1

# LinkedIn professional update
python scripts/generate.py --mode template   --input assets/templates/text/linkedin/professional_update.txt   --output update.mp4 --format 16:9

# Bilibili 一键三连
python scripts/generate.py --mode code   --script assets/templates/code/bilibili/three_clicks.py   --output 三连.mp4 --format 9:16

# Pinterest recipe
python scripts/generate.py --mode template   --input assets/templates/text/pinterest/recipe.txt   --output recipe.mp4 --format 9:16

# X thread preview
python scripts/generate.py --mode template   --input assets/templates/text/x/thread_preview.txt   --output thread.mp4 --format 16:9
\
## Template Descriptions

### YouTube
| File | Type | Format | Description |
|------|------|--------|-------------|
| intro.txt | text | 16:9 | Channel intro, welcome message |
| outro.txt | text | 16:9 | Subscribe CTA, end screen |
| howto_steps.txt | text | 16:9 | Step-by-step tutorial |
| top5.txt | text | 16:9 | Ranking/list video |
| links.txt | text | 16:9 | Link cards for description |
| shorts_hook.txt | text | 9:16 | Shorts attention-grabber |
| shorts_dailylife.txt | text | 9:16 | Day-in-the-life shorts |
| shorts_fact.txt | text | 9:16 | Fun fact/trivia shorts |

### TikTok
| File | Type | Format | Description |
|------|------|--------|-------------|
| hook_viral.txt | text | 9:16 | POV/viral hook format |
| transformation.txt | text | 9:16 | Before/after reveal |
| listicle.txt | text | 9:16 | N-things list format |
| mythbust.txt | text | 9:16 | Myth-busting format |
| trending_sound.txt | text | 9:16 | Trending meme format |
| storytime.txt | text | 9:16 | Personal story format |

### Instagram
| File | Type | Format | Description |
|------|------|--------|-------------|
| reels_lifestyle.txt | text | 9:16 | Lifestyle/aesthetic reels |
| reels_product.txt | text | 9:16 | Product showcase reels |
| reels_bts.txt | text | 9:16 | Behind-the-scenes reels |
| story_poll.txt | text | 9:16 | Poll/engagement story |
| story_countdown.txt | text | 9:16 | Countdown/announcement |
| feed_quote.txt | text | 1:1 | Quote carousel card |
| feed_tips.txt | text | 1:1 | Tips carousel card |
| feed_portfolio.txt | text | 4:5 | Personal brand intro |

### LinkedIn
| File | Type | Format | Description |
|------|------|--------|-------------|
| professional_update.txt | text | 16:9 | Announcement/update |
| industry_insights.txt | text | 16:9 | Trend/thought leadership |
| company_culture.txt | text | 16:9 | Employer branding |
| case_study.txt | text | 16:9 | Results showcase |

### Pinterest
| File | Type | Format | Description |
|------|------|--------|-------------|
| diy_tutorial.txt | text | 9:16 | Step-by-step DIY |
| recipe.txt | text | 9:16 | Cooking instructions |
| listicle.txt | text | 9:16 | Collection/list pin |

### X (Twitter)
| File | Type | Format | Description |
|------|------|--------|-------------|
| thread_preview.txt | text | 16:9 | Thread promo |
| hot_take.txt | text | 16:9 | Opinion/discussion starter |

### Facebook
| File | Type | Format | Description |
|------|------|--------|-------------|
| event_announce.txt | text | 16:9 | Event invitation |
| testimonial.txt | text | 16:9 | Social proof/reviews |

### Bilibili
| File | Type | Format | Description |
|------|------|--------|-------------|
| intro.txt | text | 16:9 | 片头欢迎 |
| tutorial_outline.txt | text | 16:9 | 教程目录 |
| outro.txt | text | 16:9 | 片尾感谢 |
| viral_hook.txt | text | 16:9 | 爆款开头 |
