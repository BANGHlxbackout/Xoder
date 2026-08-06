from pathlib import Path

import pytest

from xoder_coding.catalog_loader import effective_catalog, user_catalog_path
from xoder_coding.credentials import FileCredentialStore
from xoder_coding.diagnostics import AgentCallDiagnosticLogger
from xoder_coding.paths import XoderPaths
from xoder_coding.provider_config import load_provider_settings, provider_settings_path
from xoder_coding.session_manager import SessionManager
from xoder_coding.shell_config import load_shell_settings, shell_settings_path
from xoder_coding.tui.config import load_tui_settings, tui_settings_path
from xoder_coding.update_check import (
    default_release_notes_state_path,
    default_update_check_cache_path,
)


def test_xoder_paths_user_locations(tmp_path: Path) -> None:
    paths = XoderPaths(home=tmp_path / ".xoder", agents_home=tmp_path / ".agents")

    assert paths.sessions_dir == tmp_path / ".xoder" / "sessions"
    assert paths.user_skills_dir == tmp_path / ".xoder" / "skills"
    assert paths.user_prompts_dir == tmp_path / ".xoder" / "prompts"
    assert paths.user_agents_skills_dir == tmp_path / ".agents" / "skills"
    assert paths.user_agents_prompts_dir == tmp_path / ".agents" / "prompts"


def test_xoder_paths_default_home_uses_xoder_namespace(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    monkeypatch.setenv("HOME", str(home))

    paths = XoderPaths()

    assert paths.home == home / ".xoder"
    assert paths.agents_home == home / ".agents"


def test_default_runtime_state_uses_xoder_and_ignores_legacy_tau_home(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    legacy_home = home / ".tau"
    legacy_home.mkdir(parents=True)
    (legacy_home / "credentials.json").write_text('{"openai": "legacy-key"}', encoding="utf-8")
    (legacy_home / "providers.json").write_text("not JSON", encoding="utf-8")
    (legacy_home / "catalog.toml").write_text("not valid TOML", encoding="utf-8")
    (legacy_home / "settings.json").write_text("not JSON", encoding="utf-8")
    (legacy_home / "tui.json").write_text("not JSON", encoding="utf-8")
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))

    paths = XoderPaths()
    credentials = FileCredentialStore()
    project = tmp_path / "project"
    project.mkdir()
    session = SessionManager().create_session(cwd=project, model="fake", session_id="new")

    assert paths.home == home / ".xoder"
    assert credentials.path == paths.home / "credentials.json"
    assert credentials.get("openai") is None
    credentials.set("openai", "new-key")
    assert provider_settings_path() == paths.home / "providers.json"
    assert load_provider_settings().default_provider == "openai"
    assert user_catalog_path() == paths.home / "catalog.toml"
    assert effective_catalog()
    assert shell_settings_path() == paths.home / "settings.json"
    assert load_shell_settings().shell_command_prefix is None
    assert tui_settings_path() == paths.home / "tui.json"
    assert load_tui_settings().keybindings.quit == "ctrl+d"
    assert default_update_check_cache_path() == paths.home / "cache" / "update-check.json"
    assert default_release_notes_state_path() == paths.home / "cache" / "release-notes-state.json"
    assert AgentCallDiagnosticLogger.from_paths().path == paths.home / "logs" / "agent-calls.jsonl"
    assert session.path.is_relative_to(paths.home / "sessions")
    assert (paths.home / "credentials.json").exists()


def test_xoder_paths_project_locations(tmp_path: Path) -> None:
    paths = XoderPaths(home=tmp_path / "home", agents_home=tmp_path / "agents")
    cwd = tmp_path / "project"

    assert paths.project_xoder_dir(cwd) == cwd / ".xoder"
    assert paths.project_agents_dir(cwd) == cwd / ".agents"
    assert paths.project_skills_dir(cwd) == cwd / ".xoder" / "skills"
    assert paths.project_prompts_dir(cwd) == cwd / ".xoder" / "prompts"
    assert paths.project_agents_skills_dir(cwd) == cwd / ".agents" / "skills"
    assert paths.project_agents_prompts_dir(cwd) == cwd / ".agents" / "prompts"


def test_default_session_path_uses_home_sessions_and_readable_project_path(
    tmp_path: Path,
) -> None:
    paths = XoderPaths(home=tmp_path / "home", agents_home=tmp_path / "agents")
    cwd = tmp_path / "repos" / "exploration" / "xoder"
    cwd.mkdir(parents=True)

    session_path = paths.default_session_path(cwd)

    assert session_path.name == "default.jsonl"
    assert session_path.parent.parent == tmp_path / "home" / "sessions"
    assert "repos-exploration-xoder-" in session_path.parent.name
    assert len(session_path.parent.name.rsplit("-", maxsplit=1)[-1]) == 6
    assert session_path.parent.exists()
