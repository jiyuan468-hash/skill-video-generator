import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


def test_find_font():
    from template_mode import find_font
    font = find_font()
    assert font is not None
    assert os.path.exists(font)


def test_generate_text_template():
    from template_mode import generate
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write('Hello\nWorld\n')
        txt_path = f.name
    out = tempfile.mktemp(suffix='.mp4')
    try:
        generate(txt_path, out, (800, 600), duration=1.0, style='dark')
        assert os.path.exists(out)
        assert os.path.getsize(out) > 1000
    finally:
        if os.path.exists(out):
            os.remove(out)
        os.remove(txt_path)


def test_generate_image_template():
    from template_mode import generate
    with tempfile.TemporaryDirectory() as td:
        from PIL import Image
        img = Image.new('RGB', (100, 100), color='red')
        img.save(os.path.join(td, 'test.png'))
        out = tempfile.mktemp(suffix='.mp4')
        try:
            generate(td, out, (800, 600), duration=1.0)
            assert os.path.exists(out)
            assert os.path.getsize(out) > 1000
        finally:
            if os.path.exists(out):
                os.remove(out)


def test_code_mode_shapes():
    from code_mode import draw_frame
    import numpy as np
    frame = draw_frame(800, 600, 0.5, 30, {'shape': 'circle', 'radius': 40, 'bg_color': (0, 0, 0)})
    assert frame.shape == (600, 800, 3)
    frame2 = draw_frame(800, 600, 0.5, 30, {'shape': 'rect', 'rect_size': 50, 'bg_color': (0, 0, 0)})
    assert frame2.shape == (600, 800, 3)
    frame3 = draw_frame(800, 600, 0.5, 30, {'text': 'Hello', 'bg_color': (0, 0, 0)})
    assert frame3.shape == (600, 800, 3)


def test_code_mode_generate():
    from code_mode import generate
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write("config = {'shape': 'circle', 'radius': 40, 'duration': 2}\n")
        script = f.name
    out = tempfile.mktemp(suffix='.mp4')
    try:
        generate(script, out, (400, 300))
        assert os.path.exists(out)
        assert os.path.getsize(out) > 1000
    finally:
        if os.path.exists(out):
            os.remove(out)
        os.remove(script)


def test_platform_templates_exist():
    base = os.path.join(os.path.dirname(__file__), '..', 'assets', 'templates')
    platforms = ['youtube', 'tiktok', 'instagram', 'linkedin', 'pinterest', 'x', 'facebook', 'bilibili']
    for plat in platforms:
        text_dir = os.path.join(base, 'text', plat)
        assert os.path.isdir(text_dir), f'Missing text templates for {plat}'
        code_dir = os.path.join(base, 'code', plat)
        assert os.path.isdir(code_dir), f'Missing code templates for {plat}'


def test_code_mode_new_shapes():
    from code_mode import draw_frame
    import numpy as np
    frame = draw_frame(400, 300, 0.5, 30, {"shape": "triangle", "radius": 60, "bg_color": (0,0,0)})
    assert frame.shape == (300, 400, 3)
    frame2 = draw_frame(400, 300, 0.5, 30, {"shape": "star", "radius": 60, "bg_color": (0,0,0)})
    assert frame2.shape == (300, 400, 3)
    frame3 = draw_frame(400, 300, 0.5, 30, {"shape": "particles", "radius": 50, "bg_color": (0,0,0)})
    assert frame3.shape == (300, 400, 3)
