import json
import re
import subprocess
import tomllib
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
README_ZH_CN_PATH = ROOT / "README.zh-CN.md"
PI_REPOSITORY_URL = "https://github.com/earendil-works/pi"
DEMO_GIF_PLACEHOLDER = (
    "<!-- XODER_DEMO_GIF_PLACEHOLDER: insert docs/images/xoder-demo.gif here after capture. -->"
)
RELEASE_NOTES_SOURCE_PATH = (
    ROOT / "src" / "xoder_coding" / "data" / "release-notes" / "releases.json"
)
RELEASE_NOTES_WHEEL_PATH = "xoder_coding/data/release-notes/releases.json"
BUILTIN_RESOURCE_WHEEL_PATHS = {
    "xoder_coding/data/docs/README.md",
    "xoder_coding/data/docs/architecture.md",
    "xoder_coding/data/docs/cli.md",
    "xoder_coding/data/docs/extensions.md",
    "xoder_coding/data/docs/models.md",
    "xoder_coding/data/docs/skills.md",
    "xoder_coding/data/docs/tui.md",
    "xoder_coding/data/examples/extensions/hello_tool.py",
    "xoder_coding/data/skills/create-xoder-extension/SKILL.md",
    "xoder_coding/data/skills/xoder-model-catalog/SKILL.md",
}
EXPECTED_PROJECT_URLS = {
    "Homepage": "https://github.com/BANGHlxbackout/Xoder",
    "Repository": "https://github.com/BANGHlxbackout/Xoder",
    "Issues": "https://github.com/BANGHlxbackout/Xoder/issues",
}
EXPECTED_WHEEL_PACKAGES = ["src/xoder_ai", "src/xoder_agent", "src/xoder_coding"]
EXPECTED_SDIST_INCLUDES = [
    "/.github/workflows/ci.yml",
    "/.gitignore",
    "/.python-version",
    "/CONTRIBUTING.md",
    "/LICENSE",
    "/README.md",
    "/README.zh-CN.md",
    "/examples",
    "/pyproject.toml",
    "/src/xoder_ai",
    "/src/xoder_agent",
    "/src/xoder_coding",
    "/tests",
    "/uv.lock",
]
BUNDLED_PUBLIC_REFERENCE_FILES = (
    ROOT / "src" / "xoder_coding" / "data" / "docs" / "architecture.md",
    ROOT / "src" / "xoder_coding" / "data" / "docs" / "cli.md",
    ROOT / "src" / "xoder_coding" / "data" / "docs" / "extensions.md",
    ROOT / "src" / "xoder_coding" / "data" / "docs" / "models.md",
    ROOT / "src" / "xoder_coding" / "data" / "docs" / "skills.md",
    ROOT / "src" / "xoder_coding" / "data" / "docs" / "tui.md",
    ROOT / "src" / "xoder_coding" / "data" / "skills" / "create-xoder-extension" / "SKILL.md",
    ROOT / "src" / "xoder_coding" / "data" / "skills" / "xoder-model-catalog" / "SKILL.md",
)
STRICT_PUBLIC_FILES = (
    README_PATH,
    README_ZH_CN_PATH,
    ROOT / "CONTRIBUTING.md",
    ROOT / "pyproject.toml",
    ROOT / ".github" / "workflows" / "ci.yml",
    ROOT / ".github" / "workflows" / "pages.yml",
    ROOT / "examples" / "extensions" / "hello_tool.py",
    ROOT / "examples" / "extensions" / "permission_gate.py",
    ROOT / "website" / "index.html",
    ROOT / "website" / "script.js",
    ROOT / "website" / "styles.css",
    RELEASE_NOTES_SOURCE_PATH,
) + BUNDLED_PUBLIC_REFERENCE_FILES
TAU_BRAND_PATTERN = re.compile(r"(?i)(?<![a-z])tau(?![a-z])|τ")
FINAL_SNAPSHOT_FILES = (
    ".gitignore",
    ".python-version",
    ".github/workflows/ci.yml",
    ".github/workflows/pages.yml",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "README.zh-CN.md",
    "pyproject.toml",
    "uv.lock",
)
FINAL_SNAPSHOT_DIRS = (
    "examples",
    "src/xoder_ai",
    "src/xoder_agent",
    "src/xoder_coding",
    "tests",
    "website",
)
FINAL_SNAPSHOT_EXCLUDED_PREFIXES = (
    ".git",
    ".github/workflows/docs.yml",
    ".github/workflows/publish.yml",
    ".venv",
    "AGENTS.md",
    "Xoder简历.md",
    "dev-notes",
    "dist",
    "docs/assets/tau-header.svg",
    "landing.html",
    "phase2plan.md",
    "phase3plan.md",
    "progress.md",
    "src/tau_ai",
    "src/tau_agent",
    "src/tau_coding",
)


def _planned_snapshot_manifest() -> set[str]:
    manifest = set(FINAL_SNAPSHOT_FILES)
    for directory in FINAL_SNAPSHOT_DIRS:
        for path in (ROOT / directory).rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT)
            if (
                "__pycache__" in relative.parts
                or path.name == ".DS_Store"
                or path.suffix in {".pyc", ".pyo"}
            ):
                continue
            manifest.add(relative.as_posix())
    return manifest


def test_python_version_floor_matches_package_metadata() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert pyproject["project"]["requires-python"] == ">=3.12"
    assert pyproject["tool"]["ruff"]["target-version"] == "py312"
    assert pyproject["tool"]["mypy"]["python_version"] == "3.12"
    assert (ROOT / ".python-version").read_text(encoding="utf-8").strip() == "3.12"


def test_xoder_project_metadata() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert pyproject["project"]["name"] == "xoder-ai"
    assert pyproject["project"]["scripts"] == {"xoder": "xoder_coding.cli:app"}
    assert pyproject["project"]["urls"] == EXPECTED_PROJECT_URLS
    assert pyproject["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"] == (
        EXPECTED_WHEEL_PACKAGES
    )
    assert pyproject["tool"]["hatch"]["build"]["targets"]["sdist"]["include"] == (
        EXPECTED_SDIST_INCLUDES
    )
    assert pyproject["tool"]["mypy"]["packages"] == [
        "xoder_ai",
        "xoder_agent",
        "xoder_coding",
    ]


def test_current_version_has_only_xoder_release_notes() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert RELEASE_NOTES_SOURCE_PATH.is_file(), (
        f"release notes not found at {RELEASE_NOTES_SOURCE_PATH}"
    )
    release_notes = json.loads(RELEASE_NOTES_SOURCE_PATH.read_text(encoding="utf-8"))

    assert len(release_notes) == 1
    assert release_notes[0]["version"] == pyproject["project"]["version"]
    assert release_notes[0]["date"] is None
    assert release_notes[0]["sections"]
    serialized_notes = json.dumps(release_notes, ensure_ascii=False)
    assert TAU_BRAND_PATTERN.search(serialized_notes) is None
    assert "Xoder" in serialized_notes


def test_public_release_scope_is_xoder_only() -> None:
    for path in STRICT_PUBLIC_FILES:
        content = path.read_text(encoding="utf-8")
        assert TAU_BRAND_PATTERN.search(content) is None, f"Tau branding remains in {path}"
        assert "github.com/huggingface/tau" not in content
        assert "twotimespi.dev" not in content
        assert "dev-notes/" not in content

    readme = README_PATH.read_text(encoding="utf-8")
    readme_zh_cn = README_ZH_CN_PATH.read_text(encoding="utf-8")
    assert readme.count("# Xoder Agent Harness\n") == 1
    assert readme_zh_cn.count("# Xoder Agent Harness\n") == 1
    assert "website/Xoder_logo.png" in readme
    assert "website/Xoder_logo.png" in readme_zh_cn
    assert "docs/assets/tau-header.svg" not in readme
    assert "not yet published to PyPI" not in readme
    assert "还没有发布到 PyPI" not in readme_zh_cn
    assert "pypi.org/project/xoder-ai" not in readme
    for content in (readme, readme_zh_cn):
        assert "xoder-ai==0.0.0" in content
        assert "uv tool install xoder-ai==0.0.0" in content
        assert "uv add xoder-ai==0.0.0" in content
        assert "python -m pip install xoder-ai==0.0.0" in content
        assert "Python 3.12" in content
        assert "FakeProvider" in content
    assert 'href="README.zh-CN.md"' in readme
    assert 'href="README.md"' in readme_zh_cn
    assert PI_REPOSITORY_URL in readme
    assert PI_REPOSITORY_URL in readme_zh_cn
    assert DEMO_GIF_PLACEHOLDER in readme
    assert DEMO_GIF_PLACEHOLDER in readme_zh_cn
    assert "## Inspiration" not in readme
    assert "## 灵感来源" not in readme_zh_cn
    assert readme.index("# Xoder Agent Harness") < readme.index(PI_REPOSITORY_URL)
    assert readme.index(PI_REPOSITORY_URL) < readme.index("## Why Xoder?")
    assert readme_zh_cn.index("# Xoder Agent Harness") < readme_zh_cn.index(PI_REPOSITORY_URL)
    assert readme_zh_cn.index(PI_REPOSITORY_URL) < readme_zh_cn.index("## 为什么选择 Xoder？")

    ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "working-directory: website" not in ci
    assert "Build documentation" not in ci
    assert re.search(r"HOME:\s*\$\{\{ runner\.temp \}\}/xoder-test-home", ci)
    assert re.search(r"USERPROFILE:\s*\$\{\{ runner\.temp \}\}/xoder-test-home", ci)


def test_planned_public_snapshot_manifest_matches_phase_three_boundary() -> None:
    manifest = _planned_snapshot_manifest()

    assert set(FINAL_SNAPSHOT_FILES) <= manifest
    assert all((ROOT / path).is_file() for path in manifest)
    assert {path for path in manifest if path.startswith(".github/workflows/")} == {
        ".github/workflows/ci.yml",
        ".github/workflows/pages.yml",
    }
    assert all(Path(path).name != ".DS_Store" for path in manifest)
    for excluded in FINAL_SNAPSHOT_EXCLUDED_PREFIXES:
        assert excluded not in manifest
        assert not any(path.startswith(f"{excluded}/") for path in manifest)


def test_wheel_includes_release_notes_package_data(tmp_path: Path) -> None:
    """Regression: releases.json must be included in installed wheels."""
    wheel_dir = tmp_path / "wheel"
    wheel_dir.mkdir()
    result = subprocess.run(
        ["uv", "build", "--wheel", "--out-dir", str(wheel_dir)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    wheels = sorted(wheel_dir.glob("*.whl"))
    assert len(wheels) == 1, result.stdout + result.stderr
    with ZipFile(wheels[0]) as wheel:
        wheel_files = set(wheel.namelist())

    assert RELEASE_NOTES_WHEEL_PATH in wheel_files
    assert wheel_files >= BUILTIN_RESOURCE_WHEEL_PATHS
