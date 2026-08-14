"""Shared helpers for resolving local paths and hub paths."""

from __future__ import annotations

from pathlib import Path
import logging
import subprocess
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def resolve_path(path_value: str | Path, base_dir: str | Path | None = None) -> Path:
    """
    Resolve a path, optionally relative to a provided base directory.

    Relative paths are interpreted relative to `base_dir` when provided.
    Otherwise, they are resolved from the current working directory.
    """
    path = Path(path_value).expanduser()
    if not path.is_absolute() and base_dir is not None:
        path = Path(base_dir) / path
    return path.resolve()


def _validate_hub_directory(hub_path: Path, hub_path_value: str | Path) -> Path:
    """Validate that a resolved local hub path has the expected structure."""
    if not hub_path.is_dir():
        raise ValueError(
            f"`hub_path` ({hub_path_value}) either does not exist on this machine "
            "or does not point to a directory."
        )

    target_data_dir = hub_path / "target-data"
    if not target_data_dir.is_dir():
        raise ValueError("`hub_path` does not contain a required 'target-data/' directory.")

    return hub_path


def establish_hub_path(hub_path_value: str | Path, base_dir: str | Path | None = None) -> Path:
    """
    Resolve a hub input to a local directory and update it when possible.

    If `hub_path_value` is a GitHub URL, clone it into the project's `hubs/`
    directory when missing, otherwise pull the existing clone.

    If `hub_path_value` is a local path, resolve it and pull latest changes when
    it points to a git repository clone. Non-git local directories are still
    accepted as long as they have the expected hub structure.
    """
    hub_path_str = str(hub_path_value)
    if hub_path_str.startswith(("http://", "https://")) and "github.com" in hub_path_str:
        parsed_path = urlparse(hub_path_str).path
        repo_name = parsed_path.strip("/").split("/")[-1]
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

        project_root = Path(__file__).resolve().parents[2]
        hubs_dir = project_root / "hubs"
        hub_path = hubs_dir / repo_name

        if hub_path.exists() and hub_path.is_dir():
            logger.info(f"Updating existing hub repository: {repo_name}")
            subprocess.run(["git", "pull"], cwd=hub_path, check=True)
            logger.info("Hub updated successfully ✅")
        else:
            logger.info(f"Cloning hub repository into {hubs_dir}")
            hubs_dir.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "clone", hub_path_str], cwd=hubs_dir, check=True)
            logger.info("Hub cloned successfully ✅")

        return _validate_hub_directory(hub_path, hub_path_str)

    hub_path = resolve_path(hub_path_value, base_dir=base_dir)
    hub_path = _validate_hub_directory(hub_path, hub_path_value)

    git_dir = hub_path / ".git"
    if git_dir.exists():
        logger.info(f"Updating existing local hub repository: {hub_path}")
        subprocess.run(["git", "pull"], cwd=hub_path, check=True)
        logger.info("Hub updated successfully ✅")

    return hub_path


def resolve_output_dir(
    output_path: str | Path,
    base_dir: str | Path | None = None,
    files_to_save: list[str] | None = None,
) -> Path:
    """
    Resolve and validate an output directory path.

    Creates the directory if it does not already exist and optionally checks
    whether expected output filenames would conflict with existing files.
    """
    resolved_output_path = resolve_path(output_path, base_dir=base_dir)
    if resolved_output_path.exists() and not resolved_output_path.is_dir():
        raise NotADirectoryError(
            f"--output-path must be a directory. Received {resolved_output_path}"
        )
    resolved_output_path.mkdir(parents=True, exist_ok=True)

    if files_to_save is not None:
        conflicting_files = [
            str(resolved_output_path / filename)
            for filename in files_to_save
            if (resolved_output_path / filename).exists()
        ]
        if conflicting_files:
            raise FileExistsError(
                "The following output file(s) already exist and will not be overwritten: "
                + ", ".join(conflicting_files)
            )

    return resolved_output_path
