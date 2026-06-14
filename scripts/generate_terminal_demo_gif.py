from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ARTIFACTS_DIR = Path(__file__).resolve().parent.parent / "artifacts"
OUTPUT_PATH = ARTIFACTS_DIR / "terminal-demo.gif"


def build_terminal_demo_gif(output_path: Path = OUTPUT_PATH, frame_count: int = 10) -> None:
    ARTIFACTS_DIR.mkdir(exist_ok=True)

    width, height = 1200, 700
    bg = (15, 23, 42)
    panel = (17, 24, 39)
    accent = (56, 189, 248)
    text = (226, 232, 240)
    muted = (148, 163, 184)

    font_path = Path("C:/Windows/Fonts/consola.ttf")
    font = ImageFont.truetype(str(font_path), 24)
    small_font = ImageFont.truetype(str(font_path), 18)

    frames = []
    for step in range(frame_count):
        image = Image.new("RGB", (width, height), bg)
        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle((18, 18, width - 18, height - 18), radius=26, fill=panel, outline=(30, 41, 59), width=2)
        draw.rounded_rectangle((34, 34, width - 34, height - 34), radius=18, fill=(15, 23, 42), outline=(30, 41, 59), width=1)

        draw.rectangle((56, 56, 140, 86), fill=(248, 113, 113))
        draw.rectangle((152, 56, 236, 86), fill=(251, 191, 36))
        draw.rectangle((248, 56, 332, 86), fill=(74, 222, 128))

        y = 120
        lines = [
            "PS C:\\Users\\shail\\source\\AlphaQuant> python --version",
            "Python 3.11.8",
            "PS C:\\Users\\shail\\source\\AlphaQuant> npm --version",
            "10.9.8",
            "PS C:\\Users\\shail\\source\\AlphaQuant> docker compose version",
            "Docker Compose version v2.31.0-desktop.2",
            "",
            "AlphaQuant local setup demo",
            "VHS tape source: artifacts/quick-setup.tape",
            "GitHub-friendly terminal preview for the README.",
        ]

        for index, line in enumerate(lines):
            color = text if index % 2 == 0 else muted
            draw.text((72, y + index * 42), line, fill=color, font=font)

        cursor_phase = step % 3
        cursor_x = 72 + len("PS C:\\Users\\shail\\source\\AlphaQuant> ") * 11
        cursor_y = 120 + (cursor_phase * 2) * 42
        if cursor_phase == 0:
            draw.text((cursor_x, cursor_y), "_", fill=accent, font=font)

        draw.text((72, height - 110), "Rendered from a terminal-style GIF for GitHub README previews.", fill=muted, font=small_font)

        frames.append(image.copy())

    frames[0].save(
        output_path,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=160,
        loop=0,
        optimize=True,
        disposal=2,
    )


if __name__ == "__main__":
    build_terminal_demo_gif()
    print(f"Saved terminal demo GIF to {OUTPUT_PATH}")
