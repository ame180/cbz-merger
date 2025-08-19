# ruff: noqa: S101
from __future__ import annotations

import zipfile
from pathlib import Path

from cbz_merger.merge import merge_cbz


def _make_cbz(archive: Path, files: dict[str, bytes]) -> None:
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name, data in files.items():
            zf.writestr(name, data)


def test_merge_cbz_flattens_and_prefixes(tmp_path: Path) -> None:
    chapter1 = tmp_path / "Archive1.cbz"
    chapter2 = tmp_path / "Archive 2.cbz"
    _make_cbz(
        chapter1,
        {
            "Img1.jpg": b"jpg1",
            "sub/Img2.jpg": b"jpg2",
        },
    )
    _make_cbz(
        chapter2,
        {
            "001.png": b"p1",
        },
    )

    out = tmp_path / "merged.cbz"
    result = merge_cbz([chapter1, chapter2], out)

    assert result == out
    assert out.exists()
    with zipfile.ZipFile(out) as zf:
        names = zf.namelist()
        # Order should follow input archives, inner order of each archive preserved
        assert names == [
            "Archive1_Img1.jpg",
            "Archive1_Img2.jpg",
            "Archive_2_001.png",
        ]
