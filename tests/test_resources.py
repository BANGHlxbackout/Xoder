from pathlib import Path

import pytest

from xoder_coding import XoderPaths, XoderResourcePaths
from xoder_coding.resources import derive_description, parse_markdown_resource
from xoder_coding.self_docs import xoder_docs_path, xoder_examples_path


def test_resource_paths_use_xoder_subdirectories(tmp_path: Path) -> None:
    paths = XoderResourcePaths(root=tmp_path, agents_root=None)

    assert paths.skills_dir == tmp_path / "skills"
    assert paths.prompts_dir == tmp_path / "prompts"
    assert paths.skills_dirs[1:] == (tmp_path / "skills",)
    assert paths.skills_dirs[0].name == "skills"
    assert paths.skills_dirs[0].parent.name == "data"
    assert paths.prompts_dirs == (tmp_path / "prompts",)


def test_resource_paths_default_to_xoder_home(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home))

    assert XoderResourcePaths(agents_root=None).root == home / ".xoder"


def test_packaged_runtime_resources_use_xoder_names() -> None:
    data_root = xoder_docs_path().parent
    readme = xoder_docs_path() / "README.md"
    catalog = data_root / "catalog.toml"
    example = xoder_examples_path() / "extensions" / "hello_tool.py"

    assert "# Xoder documentation" in readme.read_text(encoding="utf-8")
    assert "# Xoder built-in provider catalog" in catalog.read_text(encoding="utf-8")
    assert "~/.xoder/catalog.toml" in catalog.read_text(encoding="utf-8")
    assert "def setup(xoder: ExtensionAPI)" in example.read_text(encoding="utf-8")


def test_resource_paths_include_agents_and_project_directories(tmp_path: Path) -> None:
    cwd = tmp_path / "project"
    xoder_home = tmp_path / "home" / ".xoder"
    agents_home = tmp_path / "home" / ".agents"
    paths = XoderResourcePaths(
        root=xoder_home,
        agents_root=agents_home,
        cwd=cwd,
        paths=XoderPaths(home=xoder_home, agents_home=agents_home),
    )

    assert paths.skills_dirs[1:] == (
        xoder_home / "skills",
        agents_home / "skills",
        cwd / ".xoder" / "skills",
        cwd / ".agents" / "skills",
    )
    assert paths.prompts_dirs == (
        xoder_home / "prompts",
        agents_home / "prompts",
        cwd / ".xoder" / "prompts",
        cwd / ".agents" / "prompts",
    )


def test_parse_frontmatter_description() -> None:
    metadata, body = parse_markdown_resource(
        "---\ndescription: Write tests\n---\n# Testing\nUse pytest."
    )

    assert metadata == {"description": "Write tests"}
    assert body == "# Testing\nUse pytest."


def test_parse_frontmatter_normalizes_crlf_line_endings() -> None:
    metadata, body = parse_markdown_resource(
        "---\r\ndescription: Write tests\r\n---\r\n# Testing\r\nUse pytest."
    )

    assert metadata == {"description": "Write tests"}
    assert body == "# Testing\nUse pytest."


def test_derive_description_uses_first_heading_or_paragraph() -> None:
    assert derive_description("\n# Title\nBody") == "Title"
    assert derive_description("\nFirst paragraph\nMore") == "First paragraph"
