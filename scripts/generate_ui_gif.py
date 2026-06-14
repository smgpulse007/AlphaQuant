from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright


ARTIFACTS_DIR = Path(__file__).resolve().parent.parent / "artifacts"
GIF_PATH = ARTIFACTS_DIR / "ui-demo.gif"
BASE_URL = "http://127.0.0.1:5173/"
FRAME_COUNT = 18
FRAME_DELAY_MS = 75


def capture_frames(url: str = BASE_URL, count: int = FRAME_COUNT) -> list[Path]:
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    frame_paths: list[Path] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        page.goto(url, wait_until="networkidle")
        max_scroll = page.evaluate("document.body.scrollHeight - window.innerHeight")

        for i in range(count):
            scroll_position = int(max_scroll * i / max(count - 1, 1))
            page.evaluate(f"window.scrollTo(0, {scroll_position})")
            page.wait_for_timeout(80)
            frame_path = ARTIFACTS_DIR / f"frame_{i:02d}.png"
            page.screenshot(path=frame_path, full_page=False)
            frame_paths.append(frame_path)

        context.close()
        browser.close()

    return frame_paths


def build_gif(frame_paths: list[Path], output_path: Path) -> None:
    frames = [Image.open(path).convert("P", palette=Image.ADAPTIVE) for path in frame_paths]
    frames = [frame.copy().convert("P", palette=Image.ADAPTIVE) for frame in frames]
    frames[0].save(
        output_path,
        format="GIF",
        append_images=frames[1:],
        save_all=True,
        duration=FRAME_DELAY_MS,
        loop=0,
        optimize=True,
    )


if __name__ == "__main__":
    frame_paths = capture_frames()
    build_gif(frame_paths, GIF_PATH)
    print(f"Saved UI demo GIF to {GIF_PATH}")
