from PIL import Image
from pathlib import Path
import argparse
import os


def convert_image(input_path: Path, output_path: Path, target_format: str, quality: int = 95):
    with Image.open(input_path) as img:
        # 转换模式
        if img.mode in ("RGBA", "LA", "P"):
            rgb_img = img.convert("RGBA" if target_format.lower() in ("png",) else "RGB")
        else:
            rgb_img = img.convert("RGB")

        # 处理透明背景：如果目标格式是 JPG，必须转成 RGB
        if target_format.lower() == "jpg":
            rgb_img = rgb_img.convert("RGB")

        # 保存
        if target_format.lower() == "jpg":
            rgb_img.save(output_path, format="JPEG", quality=quality, optimize=True)
        elif target_format.lower() == "png":
            rgb_img.save(output_path, format="PNG", optimize=True)
        elif target_format.lower() == "webp":
            rgb_img.save(output_path, format="WEBP", quality=quality)
        elif target_format.lower() == "bmp":
            rgb_img.save(output_path, format="BMP")
        else:
            raise ValueError(f"Unsupported format: {target_format}")


def process_folder(input_dir: Path, output_dir: Path, target_format: str, quality: int = 95):
    input_dir = input_dir.resolve()
    output_dir = output_dir.resolve()

    supported_exts = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tif", ".tiff"}

    for file in input_dir.rglob("*"):
        if file.is_file() and file.suffix.lower() in supported_exts:
            rel_path = file.relative_to(input_dir)
            dest_path = output_dir / rel_path
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # 只保留扩展名，不重复加格式后缀
            new_name = dest_path.stem + "." + target_format.lower()
            dest_path = dest_path.with_name(new_name)

            convert_image(file, dest_path, target_format, quality=quality)
            print(f"Converted: {file} -> {dest_path}")


def main():
    parser = argparse.ArgumentParser(description="Batch convert image formats.")
    parser.add_argument("input_dir", help="Folder containing images")
    parser.add_argument("output_dir", help="Folder to save converted images")
    parser.add_argument("--format", choices=["jpg", "png", "webp", "bmp"], default="jpg", help="Target image format")
    parser.add_argument("--quality", type=int, default=95, help="Image quality for jpg/webp, 1-100")
    args = parser.parse_args()

    process_folder(Path(args.input_dir), Path(args.output_dir), args.format, args.quality)
    print("Done.")


if __name__ == "__main__":
    main()