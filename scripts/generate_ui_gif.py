from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright


ARTIFACTS_DIR = Path(__file__).resolve().parent.parent / "artifacts"
GIF_PATH = ARTIFACTS_DIR / "ui-demo.gif"
BASE_URL = "http://127.0.0.1:5173/"


def capture_frames(url: str = BASE_URL, count: int = 5) -> list[Path]:
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    frame_paths: list[Path] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        page.goto(url, wait_until="networkidle")
        page.evaluate("window.scrollTo(0, 0)")

        for i in range(count):
            page.evaluate(f"window.scrollTo(0, {i * 120})")
            frame_path = ARTIFACTS_DIR / f"frame_{i:02d}.png"
            page.screenshot(path=frame_path, full_page=False)
            frame_paths.append(frame_path)

        context.close()
        browser.close()

    return frame_paths


def build_gif(frame_paths: list[Path], output_path: GIF_PATH) -> None:
    frames = [Image.open(path).convert("P", palette=Image.ADAPTIVE) for path in frame_paths]
    frames[0].save(
        output_path,
        format="GIF",
        append_images=frames[1:],
        save_all=True,
        duration=500,
        loop=0,
    )


if __name__ == "__main__":
    frame_paths = capture_frames()
    build_gif(frame_paths, GIF_PATH)
    print(f"Saved UI demo GIF to {GIF_PATH}")
