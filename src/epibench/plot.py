"""Run the `plot` pipeline and export a PDF of summary figures."""

from __future__ import annotations

import logging
from typing import Optional

import click
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from .build_plots import build_summary_figures, load_scores
from .path_utils import resolve_output_dir, resolve_path


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _plot_from_score_file(score_file_path: str, output_path: str) -> None:
    """Run the direct score-file plotting workflow."""
    resolved_score_file_path = resolve_path(score_file_path)
    if not resolved_score_file_path.exists():
        raise FileNotFoundError(f"Score file not found: {resolved_score_file_path}")
    if not resolved_score_file_path.is_file():
        raise ValueError(
            f"--score-file-path must be a file. Received: {resolved_score_file_path}"
        )
    output_dir = resolve_output_dir(output_path)

    logger.info("Loading and validating scoring output...")
    score_df = load_scores(resolved_score_file_path)

    logger.info("Building figures...")
    figures = build_summary_figures(score_df)

    output_pdf = output_dir / "EpiBenchmark_plots.pdf"
    logger.info("Writing PDF to %s", output_pdf)
    with PdfPages(output_pdf) as pdf:
        for figure in figures:
            pdf.savefig(figure, bbox_inches="tight")
            plt.close(figure)

    logger.info("File executed successfully to end.")
    logger.info("Output file at %s", output_pdf)


def _plot_from_challenge_library(
    challenge_name: str,
    score_file_path: str,
    output_path: str,
) -> None:
    """Run challenge-library plotting workflow."""
    logger.info(
        "Library challenge plotting requested for %s with score file at %s and output path %s.",
        challenge_name,
        score_file_path,
        output_path,
    )
    # PUT NEW PLOT LOGIC HERE
    raise NotImplementedError(
        "Library challenge plotting is not implemented yet."
    )


def plot(
    challenge_name: Optional[str] = None,
    score_file_path: Optional[str] = None,
    output_path: Optional[str] = None,
) -> None:
    """
    Main execution function for the `epibench plot` pipeline.
    """
    if challenge_name is None and score_file_path is None:
        raise click.UsageError(
            "Provide either --score-file-path with --output-path or <challenge-name> with --score-file-path."
        )
    if score_file_path is None:
        raise click.UsageError(
            "--score-file-path is required when running epibench plot."
        )
    if output_path is None:
        raise click.UsageError(
            "--output-path is required when running epibench plot."
        )

    if challenge_name is None:
        _plot_from_score_file(
            score_file_path=score_file_path,
            output_path=output_path,
        )
        return

    _plot_from_challenge_library(
        challenge_name=challenge_name,
        score_file_path=score_file_path,
        output_path=output_path,
    )
