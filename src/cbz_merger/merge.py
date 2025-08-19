from __future__ import annotations

import re
import zipfile
from collections.abc import Iterable
from pathlib import Path


def _sanitize_prefix(name: str) -> str:
    """Sanitize an archive base name to be a safe filename prefix.

    - Use the stem (without extension)
    - Keep alphanumeric characters, replace others with underscores
    - Collapse consecutive underscores
    - Strip leading/trailing underscores
    """
    stem = Path(name).stem
    # Replace non-alphanumeric with underscore
    sanitized = re.sub(r"[^A-Za-z0-9]+", "_", stem)
    sanitized = re.sub(r"_+", "_", sanitized).strip("_")
    return sanitized or "archive"


def _iter_zip_files(zip_path: Path) -> Iterable[zipfile.ZipInfo]:
    with zipfile.ZipFile(zip_path, "r") as zin:
        # Preserve original order of entries within the archive
        for info in zin.infolist():
            # Skip directories
            if info.is_dir():
                continue
            yield info


def merge_cbz(input_paths: list[str | Path], output_path: str | Path) -> Path:
    """Merge multiple CBZ archives into a single CBZ.

    All files from input archives are flattened to the top level and prefixed
    by their source archive's base name, e.g. `Archive1_Img1.jpg`.

    Inputs are processed in the order provided.
    """
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zout:
        for p in input_paths:
            src = Path(p)
            if not src.exists():
                continue
            prefix = _sanitize_prefix(src.name)
            with zipfile.ZipFile(src, "r") as zin:
                for info in zin.infolist():
                    if info.is_dir():
                        continue
                    # Flatten: take only the basename of the file
                    inner_name = Path(info.filename).name
                    arcname = f"{prefix}_{inner_name}"
                    # Read and write the file into the output zip
                    with zin.open(info, "r") as src_file:
                        data = src_file.read()
                    zout.writestr(arcname, data, compress_type=zipfile.ZIP_DEFLATED)

    return out


def create_cbz_from_files(input_files: list[str | Path], output_path: str | Path) -> Path:
    """Create a CBZ archive from a list of image files.

    Files are written to the top-level of the archive preserving the order
    in the provided list. Missing files are skipped.
    """
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in input_files:
            path = Path(p)
            if not path.exists() or not path.is_file():
                # Skip non-existing or non-file entries
                continue
            zf.write(path, arcname=path.name)
    return out
