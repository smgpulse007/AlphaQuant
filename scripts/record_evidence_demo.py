"""Render actual demo command output as a terminal GIF; requires Pillow."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]


def font(size):
    for name in ["DejaVuSansMono.ttf", "C:/Windows/Fonts/consola.ttf"]:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def main():
    result = subprocess.run([sys.executable, "-m", "scripts.evidence_demo"], cwd=ROOT,
                            capture_output=True, text=True, encoding="utf-8", timeout=30)
    if result.returncode:
        raise RuntimeError("Demo failed; no success recording created.")
    output = result.stdout
    lines = output.splitlines()
    frames, durations = [], []
    for count in range(1, len(lines) + 1):
        canvas = Image.new("RGB", (1120, 620), "#0b1422")
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle((18, 18, 1102, 602), radius=16, fill="#122238", outline="#31506b", width=2)
        draw.text((42, 36), "AlphaQuant / inspect the evidence", font=font(25), fill="#edf5fa")
        draw.text((42, 82), "$ python -m scripts.evidence_demo", font=font(20), fill="#7dd3fc")
        for index, line in enumerate(lines[:count][-17:]):
            color = "#fda4af" if ": FAIL" in line else "#a7f3d0" if ": PASS" in line else "#e1e9f5"
            draw.text((42, 128 + 24 * index), line, font=font(18), fill=color)
        draw.text((42, 572), "Actual command output / synthetic fixtures / no network calls", font=font(16), fill="#9bb3c9")
        frames.append(canvas)
        durations.append(4000 if count == len(lines) else 500)
    target = ROOT / "artifacts/evidence-demo.gif"
    frames[0].save(target, save_all=True, append_images=frames[1:], duration=durations, loop=0, optimize=True)
    sources = ["src/orchestrator/verifier.py", "scripts/evidence_demo.py"]
    metadata = {"recorded_utc": datetime.now(timezone.utc).isoformat(),
                "method": "Animation rendered from actual command output",
                "command": "python -m scripts.evidence_demo", "exit_code": result.returncode, "output": output,
                "source_hash_format": "UTF-8 bytes with CRLF normalized to LF, matching Git blobs",
                "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes().replace(b"\r\n", b"\n")).hexdigest() for name in sources},
                "gif_sha256": hashlib.sha256(target.read_bytes()).hexdigest()}
    (ROOT / "artifacts/evidence-demo.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Recorded {target.name}: {target.stat().st_size} bytes from actual execution.")


if __name__ == "__main__":
    main()
