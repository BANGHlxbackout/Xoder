"""Locations of Xoder's packaged self-documentation and examples."""

from __future__ import annotations

from pathlib import Path

_PACKAGE_ROOT = Path(__file__).resolve().parent
_DATA_ROOT = _PACKAGE_ROOT / "data"


def xoder_readme_path() -> Path:
    """Return the installed overview document for Xoder-aware tasks."""
    return _DATA_ROOT / "docs" / "README.md"


def xoder_docs_path() -> Path:
    """Return the installed Xoder self-documentation directory."""
    return _DATA_ROOT / "docs"


def xoder_examples_path() -> Path:
    """Return the installed Xoder example directory."""
    return _DATA_ROOT / "examples"


def xoder_builtin_skills_path() -> Path:
    """Return the directory containing first-party Xoder skills."""
    return _DATA_ROOT / "skills"
