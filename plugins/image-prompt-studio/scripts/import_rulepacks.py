# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Import selected upstream rulepacks locally without overwriting or executing them."""

from __future__ import annotations

import argparse
import io
import stat
import tempfile
import urllib.error
import urllib.request
import zipfile
from collections.abc import Callable
from pathlib import Path, PurePosixPath

PACKS = {
    "M2": {
        "repo": "Moeblack/moss-image-prompt-skill",
        "ref": "f89adb2d6b9ff356d8a8f7aaf2768b437a775e9e",
        "directory": "moss-community",
    },
    "K2": {
        "repo": "AI-KSK/krea2-prompt-suite",
        "ref": "2b4a9da6d9a77d83f44ecd7a5a65a5e2ed7ffddf",
        "directory": "krea2-prompt-suite",
    },
    "A1": {
        "repo": "AI-KSK/anima-prompt-crafter-skill",
        "ref": "4487133518e2864f633da5541f7207a9f1a12671",
        "directory": "anima-prompt-crafter",
    },
}
MAX_DOWNLOAD = 16 * 1024 * 1024
MAX_EXPANDED = 64 * 1024 * 1024


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "image-prompt-studio/0.2.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read(MAX_DOWNLOAD + 1)
    if len(data) > MAX_DOWNLOAD:
        raise ValueError("Upstream archive exceeds the download limit")
    return data


def extract_archive(data: bytes, destination: Path) -> Path:
    """Validate every archive member before extracting anything."""
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        members = archive.infolist()
        if not members or sum(member.file_size for member in members) > MAX_EXPANDED:
            raise ValueError("Archive is empty or exceeds the expanded-size limit")
        roots: set[str] = set()
        for member in members:
            path = PurePosixPath(member.filename)
            if (
                not path.parts
                or path.is_absolute()
                or ".." in path.parts
                or "\\" in member.filename
                or ":" in member.filename
                or stat.S_ISLNK(member.external_attr >> 16)
            ):
                raise ValueError(f"Unsafe archive member: {member.filename}")
            roots.add(path.parts[0])
            resolved = (destination / Path(*path.parts)).resolve()
            if not resolved.is_relative_to(destination.resolve()):
                raise ValueError("Archive member escapes extraction directory")
        if len(roots) != 1:
            raise ValueError("Expected a single repository root")
        archive.extractall(destination)
    source = destination / next(iter(roots))
    skill = source / "SKILL.md"
    if not skill.is_file() or not skill.read_text(encoding="utf-8").startswith("---"):
        raise ValueError("Upstream archive has no root skill with frontmatter")
    return source


def import_pack(
    code: str,
    plugin_root: Path,
    fetch: Callable[[str], bytes] = download,
) -> bool:
    """Return True for a new import and False for an unchanged existing import."""
    pack = PACKS[code]
    rulepacks = plugin_root.resolve() / "rulepacks"
    rulepacks.mkdir(parents=True, exist_ok=True)
    if rulepacks.is_symlink():
        raise ValueError("The rulepacks directory must not be a symbolic link")
    destination = rulepacks / pack["directory"]
    if destination.exists() or destination.is_symlink():
        if (
            destination.is_symlink()
            or not destination.is_dir()
            or not (destination / "SKILL.md").is_file()
        ):
            raise ValueError(f"Existing destination is not a valid rulepack: {destination}")
        return False
    url = f"https://codeload.github.com/{pack['repo']}/zip/{pack['ref']}"
    data = fetch(url)
    with tempfile.TemporaryDirectory(prefix=".import-", dir=rulepacks) as temporary:
        source = extract_archive(data, Path(temporary))
        if destination.exists() or destination.is_symlink():
            raise ValueError("Destination appeared during import; refusing to overwrite")
        source.rename(destination)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profiles", nargs="*", metavar="PROFILE", help="M2, K2 or A1")
    parser.add_argument("--list", action="store_true", help="Show local availability")
    args = parser.parse_args()
    unknown = [code for code in args.profiles if code not in PACKS]
    if unknown:
        parser.error("Unknown profiles: " + ", ".join(unknown))
    plugin_root = Path(__file__).resolve().parents[1]
    if args.list:
        for code, pack in PACKS.items():
            exists = (plugin_root / "rulepacks" / pack["directory"] / "SKILL.md").is_file()
            state = "available locally" if exists else "optional; not imported"
            print(f"{code}: {state} | https://github.com/{pack['repo']}")
    if not args.profiles:
        if not args.list:
            parser.print_help()
        return 0
    try:
        for code in dict.fromkeys(args.profiles):
            imported = import_pack(code, plugin_root)
            print(f"{code}: " + ("imported from pinned upstream snapshot" if imported else "already present; preserved"))
    except (OSError, ValueError, zipfile.BadZipFile, urllib.error.URLError) as error:
        parser.exit(1, f"Import failed: {error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
