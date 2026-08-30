#!/usr/bin/env python3
import os, sys, numpy as np, shutil
from PIL import Image, ImageDraw, ImageFont

def draw_frame(w, h, t, total, cfg):
    img = Image.new("RGB", (w, h), color=cfg.get("bg_color", (18,18,24)))
    d = ImageDraw.Draw(img)
    if cfg.get("text"):
        try: font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", cfg.get("font_size",48))
        except: font = ImageFont.load_default()
        bbox = d.textbbox((0,0), cfg["text"], font=font)
        d.text(((w-bbox[2]+bbox[0])//2,(h-bbox[3]+bbox[1])//2), cfg["text"], fill=cfg.get("text_color","white"), font=font)
    if cfg.get("shape") == "circle":
        cx=w//2+int(100*np.sin(2*np.pi*t/total)); cy=h//2+int(100*np.cos(2*np.pi*t/total))
        r=cfg.get("radius",50); d.ellipse([cx-r,cy-r,cx+r,cy+r], fill=cfg.get("shape_color",(100,150,255)))
    return np.array(img)

def generate(script_path, output_path, resolution=(1920,1080)):
    w,h = resolution; fps=30; duration=10
    cfg={"bg_color":(18,18,24),"text":"","font_size":48,"text_color":"white","shape":None,"radius":50,"rect_size":80,"shape_color":(100,150,255),"duration":10}
    try:
        import importlib.util
        spec=importlib.util.spec_from_file_location("uc",script_path)
        m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        if hasattr(m,"config"): cfg.update(m.config)
        else:
            for k in cfg:
                if hasattr(m,k): cfg[k]=getattr(m,k)
    except Exception as e: print(f"Warning: {e}")
    duration=cfg.get("duration",10)
    fd=os.path.join(os.path.dirname(output_path),".frames")
    os.makedirs(fd,exist_ok=True)
    for i in range(int(fps*duration)):
        Image.fromarray(draw_frame(w,h,i/fps,int(fps*duration),cfg)).save(os.path.join(fd,f"frame_{i:05d}.png"))
    import ffmpeg
    (ffmpeg.input(os.path.join(fd,"frame_%05d.png"),framerate=fps).output(output_path,codec="libx264",preset="medium",crf=23).overwrite_output().run(capture_stdout=True,capture_stderr=True))
    shutil.rmtree(fd,ignore_errors=True)
    return output_path