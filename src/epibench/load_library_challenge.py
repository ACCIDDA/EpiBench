"""Helpers for loading bundled challenge-library definitions."""

from __future__ import annotations

import json
from importlib import resources
from pathlib import Path

import click


def load_library_challenge(challenge_name: str) -> dict[str, object]:
    """Load one EpiBenchmark library challenge from the challenges-library directory."""
    challenges_dir = resources.files("epibench").joinpath("challenges-library")
    requested_name = Path(challenge_name).stem

    available_challenge_files = {
        challenge_path.stem: challenge_path
        for challenge_path in challenges_dir.iterdir()
        if challenge_path.is_file() and challenge_path.suffix.lower() == ".json"
    }

    challenge_path = available_challenge_files.get(requested_name)
    if challenge_path is None:
        available_challenge_names = ", ".join(sorted(available_challenge_files))
        raise click.ClickException(
            "that challenge is not in the EpiBenchmark challenge library. "
            f"Available challenges: {available_challenge_names}"
        )

    with challenge_path.open("r", encoding="utf-8") as challenges_file:
        return json.load(challenges_file)
