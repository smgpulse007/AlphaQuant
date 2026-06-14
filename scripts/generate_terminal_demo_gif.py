from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ARTIFACTS_DIR = Path(__file__).resolve().parent.parent / "artifacts"
OUTPUT_PATH = ARTIFACTS_DIR / "terminal-demo.gif"
PROMPT = "PS C:\\Users\\shail\\source\\AlphaQuant> "
COMMANDS = [
    ("python --version", ["Python 3.11.8"]),
    ("npm --version", ["10.9.8"]),
    ("docker compose version", ["Docker Compose version v2.31.0-desktop.2"]),
]


def _load_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/consola.ttf"),
        Path("C:/Windows/Fonts/CascadiaMono.ttf"),
        Path("C:/Windows/Fonts/consolab.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def _render_frame(typed_prefix: str, output_lines: list[str], cursor_on: bool, width: int = 1200, height: int = 700) -> Image.Image:
    image = Image.new("RGB", (width, height), (10, 14, 24))
    draw = ImageDraw.Draw(image)
    panel = (17, 24, 39)
    accent = (56, 189, 248)
    text = (226, 232, 240)
    muted = (148, 163, 184)

    draw.rounded_rectangle((18, 18, width - 18, height - 18), radius=26, fill=panel, outline=(30, 41, 59), width=2)
    draw.rounded_rectangle((34, 34, width - 34, height - 34), radius=18, fill=(10, 14, 24), outline=(30, 41, 59), width=1)

    draw.rectangle((56, 56, 140, 86), fill=(248, 113, 113))
    draw.rectangle((152, 56, 236, 86), fill=(251, 191, 36))
    draw.rectangle((248, 56, 332, 86), fill=(74, 222, 128))

    font = _load_font(22)
    small_font = _load_font(18)

    draw.text((72, 96), "AlphaQuant local setup", fill=text, font=font)
    draw.text((72, 126), "Command sequence preview", fill=muted, font=small_font)

    y = 180
    draw.text((72, y), PROMPT + typed_prefix, fill=text, font=font)
    if cursor_on:
        cursor_x = 72 + font.getbbox(PROMPT + typed_prefix)[2]
        draw.text((cursor_x, y), "_", fill=accent, font=font)

    y += 42
    for line in output_lines:
        draw.text((92, y), line, fill=(167, 243, 208), font=font)
        y += 42

    draw.text((72, height - 92), "Real command flow shown in sequence for the README preview.", fill=muted, font=small_font)
    return image


def build_terminal_demo_gif(output_path: Path = OUTPUT_PATH, frame_delay_ms: int = 140) -> None:
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    width, height = 1200, 700

    frames = []
    for command, outputs in COMMANDS:
        for step in range(1, len(command) + 1):
            typed_prefix = command[:step]
            frames.append(_render_frame(typed_prefix, [], step % 2 == 0, width, height))

        for _ in range(4):
            frames.append(_render_frame(command, outputs, True, width, height))

    frames[0].save(
        output_path,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=frame_delay_ms,
        loop=0,
        optimize=True,
        disposal=2,
    )


if __name__ == "__main__":
    build_terminal_demo_gif()
    print(f"Saved terminal demo GIF to {OUTPUT_PATH}")
