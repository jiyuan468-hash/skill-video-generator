#!/usr/bin/env python3
import os, sys, numpy as np, shutil, math
from PIL import Image, ImageDraw, ImageFont

def draw_frame(w, h, t, total, cfg):
    img = Image.new('RGB', (w, h), color=cfg.get('bg_color', (18,18,24)))
    d = ImageDraw.Draw(img)
    # Draw text
    if cfg.get('text'):
        try: font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', cfg.get('font_size', 48))
        except: font = ImageFont.load_default()
        bbox = d.textbbox((0,0), cfg['text'], font=font)
        d.text(((w-bbox[2]+bbox[0])//2, (h-bbox[3]+bbox[1])//2), cfg['text'], fill=cfg.get('text_color', 'white'), font=font)
    # Draw animated shape
    shape = cfg.get('shape')
    if shape == 'circle':
        cx = w//2 + int(100*np.sin(2*np.pi*t/total))
        cy = h//2 + int(100*np.cos(2*np.pi*t/total))
        r = cfg.get('radius', 50) + int(20*np.sin(4*np.pi*t/total))
        d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=cfg.get('shape_color', (100,150,255)))
    elif shape == 'rect':
        cx, cy = w//2, h//2
        s = cfg.get('rect_size', 80) + int(15*np.sin(3*np.pi*t/total))
        rot = int(360*t/total)
        cos_a, sin_a = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        hs = s//2
        pts = []
        for dx, dy in [(-hs,-hs),(hs,-hs),(hs,hs),(-hs,hs)]:
            rx = int(cx + dx*cos_a - dy*sin_a)
            ry = int(cy + dx*sin_a + dy*cos_a)
            pts.append((rx, ry))
        d.polygon(pts, fill=cfg.get('shape_color', (255,100,100)))
    elif shape == 'triangle':
        cx, cy = w//2, h//2
        r = cfg.get('radius', 60) + int(15*np.sin(3*np.pi*t/total))
        rot = int(120*t/total)
        pts = []
        for i in range(3):
            angle = math.radians(rot + i*120 - 90)
            px = int(cx + r*math.cos(angle))
            py = int(cy + r*math.sin(angle))
            pts.append((px, py))
        d.polygon(pts, fill=cfg.get('shape_color', (100,255,150)))
    elif shape == 'star':
        cx, cy = w//2, h//2
        outer_r = cfg.get('radius', 60) + int(10*np.sin(4*np.pi*t/total))
        inner_r = outer_r * 0.4
        rot = int(72*t/total)
        pts = []
        for i in range(10):
            angle = math.radians(rot + i*36 - 90)
            r = outer_r if i % 2 == 0 else inner_r
            px = int(cx + r*math.cos(angle))
            py = int(cy + r*math.sin(angle))
            pts.append((px, py))
        d.polygon(pts, fill=cfg.get('shape_color', (255,200,50)))
    elif shape == 'particles':
        cx, cy = w//2, h//2
        colors = [(255,100,100), (100,255,100), (100,100,255), (255,255,100), (255,100,255)]
        for i in range(12):
            angle = 2*np.pi*i/12 + t*2
            dist = 50 + int(30*np.sin(3*np.pi*t/total + i))
            px = int(cx + dist*math.cos(angle))
            py = int(cy + dist*math.sin(angle))
            r = 8 + int(4*np.sin(5*np.pi*t/total + i))
            d.ellipse([px-r, py-r, px+r, py+r], fill=colors[i%len(colors)])
    return np.array(img)

def generate(script_path, output_path, resolution=(1920,1080)):
    w, h = resolution
    fps = 30
    duration = 10
    cfg = {
        'bg_color': (18,18,24),
        'text': '',
        'font_size': 48,
        'text_color': 'white',
        'shape': None,
        'radius': 50,
        'rect_size': 80,
        'shape_color': (100,150,255),
        'duration': 10,
    }
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location('uc', script_path)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        if hasattr(m, 'config'):
            cfg.update(m.config)
        else:
            for k in cfg:
                if hasattr(m, k):
                    cfg[k] = getattr(m, k)
    except Exception as e:
        print(f'Warning: {e}')
    duration = cfg.get('duration', 10)
    fd = os.path.join(os.path.dirname(output_path), '.frames')
    os.makedirs(fd, exist_ok=True)
    total = int(fps * duration)
    for i in range(total):
        Image.fromarray(draw_frame(w, h, i/fps, total, cfg)).save(os.path.join(fd, f'frame_{i:05d}.png'))
    import ffmpeg
    (ffmpeg.input(os.path.join(fd, 'frame_%05d.png'), framerate=fps)
     .output(output_path, codec='libx264', preset='medium', crf=23)
     .overwrite_output().run(capture_stdout=True, capture_stderr=True))
    shutil.rmtree(fd, ignore_errors=True)
    return output_path
