import shutil
import sys
from pathlib import Path
from typing import Generator

from generate import generate_page


_PUBLIC_DIR = Path(__file__).parent.parent / "docs"
_STATIC_DIR = Path(__file__).parent.parent / "static"
_CONTENT_DIR = Path(__file__).parent.parent / "content"
_TEMPLATE_PATH = Path(__file__).parent.parent / "template.html"


def _purge_public():
    print(f'Purging public directory at {_PUBLIC_DIR!s}')
    if _PUBLIC_DIR.exists():
        shutil.rmtree(_PUBLIC_DIR)
    _PUBLIC_DIR.mkdir()


def _recursive_walk(path: Path) -> Generator[Path, None, None]:
    if path.is_file():
        yield path
    if path.is_dir():
        for p in path.iterdir():
            yield from _recursive_walk(p)


def _copy_static_to_public():
    for static_fp in _recursive_walk(_STATIC_DIR):
        public_fp = _PUBLIC_DIR / static_fp.relative_to(_STATIC_DIR)
        print(f"Copying {static_fp!s} to {public_fp!s}")
        public_fp.parent.mkdir(exist_ok=True)
        shutil.copy(static_fp, public_fp)


def _generate_pages(base_path: str = "/"):
    for src_path in _recursive_walk(_CONTENT_DIR):
        if src_path.suffix == ".md":
            dest_path = (_PUBLIC_DIR / src_path.relative_to(_CONTENT_DIR)).with_suffix(".html")
            generate_page(src_path, _TEMPLATE_PATH, dest_path, base_path)


def main():
    _purge_public()
    _copy_static_to_public()
    base_path = sys.argv[1] if len(sys.argv) == 2 else "/"
    _generate_pages(base_path)


if __name__ == "__main__":
    main()
