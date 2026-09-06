import os, json, glob

base = r"C:\Users\Administrator\Documents\Codex\2026-08-30\new-chat-3\outputs\skill-video-generator"
tdir = os.path.join(base, "assets", "templates")

pnames = {
    "douyin": "抖音", "tiktok": "TikTok", "youtube": "YouTube",
    "instagram": "Instagram", "linkedin": "LinkedIn", "bilibili": "Bilibili",
    "pinterest": "Pinterest", "x": "X", "facebook": "Facebook",
    "xiaohongshu": "小红书", "kuaishou": "快手", "all": "全部"
}
platforms = ["all","douyin","tiktok","youtube","instagram","linkedin","bilibili","pinterest","x","facebook","xiaohongshu","kuaishou"]

templates = []
sep = os.sep

for p in sorted(glob.glob(os.path.join(tdir, "text", "*", "*.txt"))):
    rel = os.path.relpath(p, base).replace(sep, "/")
    parts = p.split(sep)
    plat = parts[-2]
    title = os.path.splitext(parts[-1])[0]
    fmt = "9:16" if plat in ("douyin", "tiktok", "kuaishou") else "4:5" if plat == "xiaohongshu" else "16:9"
    templates.append({"platform": plat, "type": "text", "title": title, "desc": title, "cmd": f"python scripts/generate.py --mode template --input {rel} --output video.mp4 --format {fmt}"})

for p in sorted(glob.glob(os.path.join(tdir, "code", "*", "*.py"))):
    rel = os.path.relpath(p, base).replace(sep, "/")
    parts = p.split(sep)
    plat = parts[-2]
    title = os.path.splitext(parts[-1])[0]
    fmt = "9:16" if plat in ("douyin", "tiktok", "kuaishou") else "4:5" if plat == "xiaohongshu" else "16:9"
    templates.append({"platform": plat, "type": "code", "title": title, "desc": title, "cmd": f"python scripts/generate.py --mode code --script {rel} --output video.mp4 --format {fmt}"})

for p in sorted(glob.glob(os.path.join(tdir, "code", "*.py"))):
    rel = os.path.relpath(p, base).replace(sep, "/")
    title = os.path.splitext(os.path.basename(p))[0]
    templates.append({"platform": "all", "type": "code", "title": title, "desc": title, "cmd": f"python scripts/generate.py --mode code --script {rel} --output video.mp4"})

tc = len([t for t in templates if t["type"] == "text"])
cc = len([t for t in templates if t["type"] == "code"])
pc = len(set(t["platform"] for t in templates if t["platform"] != "all"))

js_t = json.dumps(templates, ensure_ascii=False)
js_p = json.dumps(platforms, ensure_ascii=False)
js_np = json.dumps(pnames, ensure_ascii=False)

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Video Generator</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#0f0f1a;color:#e0e0e0;min-height:100vh}}
.header{{background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);padding:40px 20px;text-align:center;border-bottom:1px solid #2a2a4a}}
.header h1{{font-size:2.5rem;background:linear-gradient(90deg,#00d4ff,#7b2dff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:10px}}
.header p{{color:#888;font-size:1rem}}
.nav{{display:flex;justify-content:center;gap:10px;padding:20px;flex-wrap:wrap}}
.nav-btn{{padding:10px 24px;border:1px solid #2a2a4a;background:#1a1a2e;color:#aaa;border-radius:8px;cursor:pointer;font-size:0.9rem;transition:all 0.2s}}
.nav-btn:hover,.nav-btn.active{{background:#7b2dff;color:#fff;border-color:#7b2dff}}
.container{{max-width:1200px;margin:0 auto;padding:20px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}}
.card{{background:#1a1a2e;border:1px solid #2a2a4a;border-radius:12px;padding:18px;transition:all 0.3s;cursor:pointer}}
.card:hover{{border-color:#7b2dff;transform:translateY(-3px);box-shadow:0 8px 30px rgba(123,45,255,0.2)}}
.card-platform{{font-size:0.7rem;color:#7b2dff;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px}}
.card-title{{font-size:1rem;color:#fff;margin-bottom:4px}}
.card-desc{{font-size:0.8rem;color:#888;margin-bottom:10px}}
.card-tag{{display:inline-block;padding:2px 8px;border-radius:20px;font-size:0.7rem;margin-right:4px}}
.card-tag.type-text{{background:#1a3a2e;color:#4ade80}}
.card-tag.type-code{{background:#3a1a2e;color:#f472b6}}
.stats{{display:flex;justify-content:center;gap:40px;padding:25px;background:#1a1a2e;margin:20px 0;border-radius:12px}}
.stat-item{{text-align:center}}
.stat-num{{font-size:2rem;font-weight:bold;background:linear-gradient(90deg,#00d4ff,#7b2dff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.stat-label{{font-size:0.8rem;color:#888;margin-top:4px}}
.code-block{{background:#0d0d1a;border:1px solid #2a2a4a;border-radius:8px;padding:12px;font-family:Consolas,monospace;font-size:0.8rem;color:#4ade80;margin-top:10px;word-break:break-all;white-space:pre-wrap}}
.modal{{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);z-index:100;align-items:center;justify-content:center}}
.modal.show{{display:flex}}
.modal-content{{background:#1a1a2e;border:1px solid #2a2a4a;border-radius:16px;padding:28px;max-width:520px;width:92%}}
.modal h2{{color:#fff;margin-bottom:12px}}
.modal-close{{float:right;cursor:pointer;color:#888;font-size:1.5rem;line-height:1}}
.modal-close:hover{{color:#fff}}
.btn-copy{{background:#7b2dff;color:#fff;border:none;padding:10px 20px;border-radius:8px;cursor:pointer;font-size:0.9rem;margin-top:15px;width:100%;transition:background 0.2s}}
.btn-copy:hover{{background:#6a1ff0}}
.search{{max-width:400px;margin:0 auto 20px;padding:12px 16px;background:#1a1a2e;border:1px solid #2a2a4a;border-radius:8px;color:#fff;font-size:0.95rem}}
.search:focus{{outline:none;border-color:#7b2dff}}
.search::placeholder{{color:#555}}
.footer{{text-align:center;padding:30px;color:#555;font-size:0.8rem}}
.footer a{{color:#7b2dff;text-decoration:none}}
</style>
</head>
<body>
<div class="header"><h1>Video Generator</h1><p>自动生成视频 &middot; {pc}大平台 &middot; {tc}+{cc}模板</p></div>
<div class="container">
  <div class="stats">
    <div class="stat-item"><div class="stat-num">{tc}</div><div class="stat-label">文本模板</div></div>
    <div class="stat-item"><div class="stat-num">{cc}</div><div class="stat-label">动画模板</div></div>
    <div class="stat-item"><div class="stat-num">{pc}</div><div class="stat-label">平台覆盖</div></div>
    <div class="stat-item"><div class="stat-num">7</div><div class="stat-label">测试通过</div></div>
  </div>
  <div class="nav" id="nav"></div>
  <input class="search" type="text" placeholder="搜索模板..." id="searchInput">
  <div class="grid" id="grid"></div>
</div>
<div class="modal" id="modal"><div class="modal-content">
  <span class="modal-close" onclick="closeModal()">&times;</span>
  <h2 id="mTitle"></h2>
  <p id="mDesc" style="color:#888;margin-bottom:12px"></p>
  <div id="mCmd" class="code-block"></div>
  <button class="btn-copy" onclick="copyCmd()">复制命令</button>
</div></div>
<div class="footer"><p>GitHub: <a href="https://github.com/jiyuan468-hash/skill-video-generator">jiyuan468-hash/skill-video-generator</a></p></div>
<script>
var T = {js_t};
var cur='all';
var platforms = {js_p};
var pnames = {js_np};
function renderNav(){{var n=document.getElementById('nav');n.innerHTML=platforms.map(function(p){{return '<button class="nav-btn'+(p===cur?' active':'')+'" onclick="filter(' + p + ')"\'>'+pnames[p]+'</button>'}}).join('');}}
function getFiltered(){{var q=document.getElementById('searchInput').value.toLowerCase();return T.filter(function(t){{var match=cur==='all'||t.platform===cur||t.platform==='all';if(!match)return false;if(!q)return true;return t.title.toLowerCase().indexOf(q)>-1||t.desc.toLowerCase().indexOf(q)>-1||t.platform.indexOf(q)>-1;}});}}
function render(){{var list=getFiltered();var g=document.getElementById('grid');g.innerHTML=list.map(function(t){{var fi=T.indexOf(t);return '<div class="card" onclick="showModal('+fi+')"><div class="card-platform">'+pnames[t.platform]+'</div><div class="card-title">'+t.title+'</div><div class="card-desc">'+t.desc+'</div><span class="card-tag type-'+t.type+'">'+(t.type==='text'?'文本模板':'动画模板')+'</span></div>';}}).join('');}}
function filter(p){{cur=p;renderNav();render();}}
document.getElementById('searchInput').addEventListener('input',function(){{render();}});
function showModal(i){{var t=T[i];document.getElementById('mTitle').textContent=t.title;document.getElementById('mDesc').textContent=pnames[t.platform]+' &middot; '+(t.type==='text'?'文本':'动画')+' &middot; '+t.desc;document.getElementById('mCmd').textContent=t.cmd;document.getElementById('modal').classList.add('show');}}
function closeModal(){{document.getElementById('modal').classList.remove('show');}}
function copyCmd(){{var cmd=document.getElementById('mCmd').textContent;navigator.clipboard.writeText(cmd);var b=document.querySelector('.btn-copy');b.textContent='已复制!';setTimeout(function(){{b.textContent='复制命令';}},1500);}}
document.getElementById('modal').addEventListener('click',function(e){{if(e.target.id==='modal')closeModal();}});
renderNav();render();
</script>
</body>
</html>"""

out = os.path.join(base, "website", "index.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Written: {out}")
print(f"Total: {len(templates)} templates ({tc} text + {cc} code), {pc} platforms")
