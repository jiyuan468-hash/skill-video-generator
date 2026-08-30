#!/usr/bin/env python3
import os, time, requests

PROVIDERS = {
    "runway": {"base":"https://api.runwayml.com/v1","env":"RUNWAY_API_KEY","durations":[5,10]},
    "pika": {"base":"https://api.pika.art/v1","env":"PIKA_API_KEY","durations":[3,5,10]},
    "stability": {"base":"https://api.stability.ai/v1","env":"STABILITY_API_KEY","durations":[5,10,15]},
}

def get_key(provider):
    cfg=PROVIDERS[provider]
    key=os.environ.get(cfg["env"])
    if not key: raise ValueError(f"Set {cfg['env']} env var")
    return key

def generate(prompt, output_path, resolution=(1920,1080), provider="runway", duration=5, quality="standard"):
    api_key=get_key(provider)
    cfg=PROVIDERS[provider]
    dur=min(max(duration,min(cfg["durations"])),max(cfg["durations"]))
    w,h=resolution
    hdr={"Authorization":f"Bearer {api_key}","Content-Type":"application/json"}
    payload={"prompt":prompt,"aspect_ratio":f"{w}:{h}","duration":dur}
    print(f"Submitting to {provider}...")
    resp=requests.post(f"{cfg['base']}/generate",headers=hdr,json=payload,timeout=30)
    resp.raise_for_status()
    job_id=resp.json().get("id")
    if not job_id: raise Exception(f"Failed: {resp.text}")
    print(f"Job: {job_id}, polling...")
    for _ in range(60):
        time.sleep(5)
        pr=requests.get(f"{cfg['base']}/jobs/{job_id}",headers=hdr,timeout=30)
        pr.raise_for_status()
        st=pr.json().get("status","")
        print(f"  {st}")
        if st in ("completed","succeeded","done"):
            url=pr.json().get("video_url") or (pr.json().get("output",[{}])[0].get("url") if pr.json().get("output") else None)
            if url: break
        elif st in ("failed","error"): raise Exception(f"Job failed: {pr.text}")
    print("Downloading...")
    dl=requests.get(url,timeout=120); dl.raise_for_status()
    with open(output_path,"wb") as f: f.write(dl.content)
    return output_path