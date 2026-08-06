from pathlib import Path

from xoder_coding.context import discover_project_context
from xoder_coding.paths import XoderPaths
from xoder_coding.resources import XoderResourcePaths


def test_discovers_user_project_and_agents_context_files(tmp_path: Path) -> None:
    xoder_home = tmp_path / "home" / ".xoder"
    agents_home = tmp_path / "home" / ".agents"
    project = tmp_path / "project"
    nested = project / "pkg"
    nested.mkdir(parents=True)
    (project / "pyproject.toml").write_text("[project]\nname = 'demo'\n", encoding="utf-8")
    (xoder_home).mkdir(parents=True)
    (agents_home).mkdir(parents=True)
    (project / ".xoder").mkdir()
    (project / ".agents").mkdir()

    (xoder_home / "AGENTS.md").write_text("User Xoder instructions", encoding="utf-8")
    (agents_home / "AGENTS.md").write_text("User agents instructions", encoding="utf-8")
    (project / "AGENTS.md").write_text("Project instructions", encoding="utf-8")
    (nested / "AGENTS.md").write_text("Nested instructions", encoding="utf-8")
    (nested / ".xoder").mkdir()
    (nested / ".agents").mkdir()
    (nested / ".xoder" / "AGENTS.md").write_text("Project Xoder instructions", encoding="utf-8")
    (nested / ".agents" / "AGENTS.md").write_text("Project agents instructions", encoding="utf-8")

    context_files = discover_project_context(
        XoderResourcePaths(
            root=xoder_home,
            agents_root=agents_home,
            cwd=nested,
            paths=XoderPaths(home=xoder_home, agents_home=agents_home),
        )
    )

    assert [Path(context_file.path) for context_file in context_files] == [
        xoder_home / "AGENTS.md",
        agents_home / "AGENTS.md",
        project / "AGENTS.md",
        nested / "AGENTS.md",
        nested / ".xoder" / "AGENTS.md",
        nested / ".agents" / "AGENTS.md",
    ]
    assert [context_file.content for context_file in context_files] == [
        "User Xoder instructions",
        "User agents instructions",
        "Project instructions",
        "Nested instructions",
        "Project Xoder instructions",
        "Project agents instructions",
    ]
