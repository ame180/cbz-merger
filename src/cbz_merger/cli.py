from __future__ import annotations

import argparse
from collections.abc import Iterable
from pathlib import Path

from .merge import create_cbz_from_files, merge_cbz


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="cbz-merger",
        description=(
            "Merge multiple CBZ chapter archives into a single volume CBZ. "
            "All files are flattened to the top level and prefixed by their source archive name."
        ),
    )
    parser.add_argument("output", type=Path, help="Path to the resulting merged .cbz volume")
    parser.add_argument(
        "inputs",
        nargs="+",
        type=Path,
        help=(
            "Either: a single directory (default mode) containing .cbz chapter files to merge, "
            "or one or more paths to .cbz files to merge in the provided order."
        ),
    )
    parser.add_argument(
        "--mode",
        choices=["auto", "dir", "archives", "files"],
        default="auto",
        help=(
            "Operation mode: `auto` uses heuristics. `dir` forces directory mode."
            " `archives` treats inputs as CBZ archives, `files` treats inputs as image files."
        ),
    )
    args = parser.parse_args()

    inputs: Iterable[Path] = args.inputs

    mode = args.mode

    # Directory mode: treat inputs[0] as a directory and merge .cbz inside
    if mode == "dir" or (mode == "auto" and len(args.inputs) == 1 and args.inputs[0].is_dir()):
        dirp = args.inputs[0]
        # collect .cbz files (case-insensitive) and sort them
        cbz_files = sorted(p for p in dirp.iterdir() if p.is_file() and p.suffix.lower() == ".cbz")
        merge_cbz(cbz_files, args.output)
        return

    # Secondary mode: explicit list of files or archives
    # If inputs are plain image files instead of archives, use create_cbz_from_files
    # Heuristic: if any input has a .cbz suffix, treat inputs as archives to merge.
    # Otherwise treat the inputs as plain files to add to a new CBZ.
    if mode == "archives" or (mode == "auto" and any(p.suffix.lower() == ".cbz" for p in inputs)):
        merge_cbz(list(inputs), args.output)
    else:
        # files mode or auto-no-cbz -> create cbz from provided files
        create_cbz_from_files(list(inputs), args.output)


if __name__ == "__main__":
    main()
