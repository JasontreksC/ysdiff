"""images/ 안의 이미지를 EXIF 방향 고정 후, 가장 작은 이미지 크기에 맞춰 리사이즈한다."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp"}


def collect_images(input_dir: Path) -> list[Path]:
    return sorted(
        p
        for p in input_dir.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )


def oriented_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img)
        return img.size


def find_smallest_size(paths: list[Path]) -> tuple[int, int]:
    sizes = [oriented_size(p) for p in paths]
    min_w = min(w for w, _ in sizes)
    min_h = min(h for _, h in sizes)
    return min_w, min_h


def process_image(src: Path, dst: Path, size: tuple[int, int]) -> None:
    with Image.open(src) as img:
        img = ImageOps.exif_transpose(img)
        img = img.convert("RGB")
        if img.size != size:
            img = img.resize(size, Image.Resampling.LANCZOS)
        dst.parent.mkdir(parents=True, exist_ok=True)
        img.save(dst, format="PNG", optimize=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fix EXIF orientation and resize all images to the smallest size."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=Path("t_images"),
        help="입력 폴더 (기본: t_images)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("t_images/processed"),
        help="출력 폴더 (기본: t_images/processed)",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=None,
        help="출력 가로 크기 (생략 시 가장 작은 이미지의 가로에 맞춤, 세로는 비율 유지)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    images = collect_images(args.input)
    if not images:
        print(f"이미지가 없습니다: {args.input}")
        return

    min_w, min_h = find_smallest_size(images)
    if args.width is not None:
        height = round(args.width * min_h / min_w)
        size = (args.width, height)
    else:
        size = (min_w, min_h)

    print(f"대상 {len(images)}장 → {size[0]}x{size[1]} (가장 작은 기준: {min_w}x{min_h})")
    print(f"출력: {args.output}/")

    for src in images:
        dst = args.output / f"{src.stem}.png"
        process_image(src, dst, size)
        print(f"  {src.name} → {dst}")

    print("완료")


if __name__ == "__main__":
    main()
