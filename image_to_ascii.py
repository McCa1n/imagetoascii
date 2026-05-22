from pathlib import Path
import sys

from PIL import Image
from PIL import ImageEnhance


ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"}
RESET_COLOR = "\033[0m"


def find_image_files() -> list[Path]:
    script_dir = Path(__file__).resolve().parent
    image_files = sorted(
        path
        for path in script_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    if not image_files:
        raise FileNotFoundError("No image files were found in this folder.")
    return image_files


def resize_image(image: Image.Image, width: int) -> Image.Image:
    aspect_ratio = image.height / image.width
    # Terminal characters are taller than they are wide, so shrink height a bit.
    height = max(1, int(width * aspect_ratio * 0.55))
    return image.resize((width, height))


def enhance_image(image: Image.Image) -> Image.Image:
    image = ImageEnhance.Contrast(image).enhance(1.8)
    image = ImageEnhance.Sharpness(image).enhance(1.4)
    image = ImageEnhance.Brightness(image).enhance(1.05)
    return image


def pixel_to_char(pixel: int) -> str:
    return ASCII_CHARS[pixel * (len(ASCII_CHARS) - 1) // 255]


def rgb_to_ansi(red: int, green: int, blue: int) -> str:
    return f"\033[38;2;{red};{green};{blue}m"


def image_to_ascii(image_path: Path, width: int) -> tuple[str, str]:
    with Image.open(image_path) as image:
        color_image = resize_image(image.convert("RGB"), width)
        grayscale = resize_image(enhance_image(image.convert("L")), width)

    color_pixels = list(color_image.getdata())
    gray_pixels = list(grayscale.getdata())
    plain_lines = []
    colored_lines = []

    for row_start in range(0, len(gray_pixels), grayscale.width):
        gray_row = gray_pixels[row_start : row_start + grayscale.width]
        color_row = color_pixels[row_start : row_start + color_image.width]

        plain_chars = []
        colored_chars = []
        for gray_pixel, (red, green, blue) in zip(gray_row, color_row):
            char = pixel_to_char(gray_pixel)
            plain_chars.append(char)
            colored_chars.append(f"{rgb_to_ansi(red, green, blue)}{char}{RESET_COLOR}")

        plain_lines.append("".join(plain_chars))
        colored_lines.append("".join(colored_chars))

    return "\n".join(plain_lines), "\n".join(colored_lines)


def save_ascii_file(image_path: Path, ascii_art: str) -> Path:
    output_path = image_path.with_name(f"{image_path.stem}_ascii.txt")
    output_path.write_text(ascii_art, encoding="utf-8")
    return output_path


def main():
    width = 120
    if len(sys.argv) > 1:
        width = int(sys.argv[1])

    image_files = find_image_files()

    for image_path in image_files:
        plain_ascii_art, colored_ascii_art = image_to_ascii(image_path, width)
        output_path = save_ascii_file(image_path, plain_ascii_art)

        print(f"Image: {image_path.name}")
        print(f"Saved: {output_path.name}")
        print(colored_ascii_art)
        print("\n" + "=" * width + "\n")


if __name__ == "__main__":
    main()
