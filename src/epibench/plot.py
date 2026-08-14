"""Run the `plot` pipeline and export a PDF of summary figures."""

from __future__ import annotations

import logging
from typing import Optional

import click
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from .build_plots import build_summary_figures, load_scores
from .config import Config


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _plot_from_config(config_path: str) -> None:
    """Run the config-driven plotting workflow."""
    logger.info("Validating config...")
    config_object = Config(config_path=config_path, pipeline="plot")

    logger.info("Loading and validating scoring output...")
    score_df = load_scores(config_object.score_file_path)

    logger.info("Building figures...")
    figures = build_summary_figures(score_df)

    output_pdf = config_object.plot_output_dir / "EpiBenchmark_plots.pdf"
    logger.info("Writing PDF to %s", output_pdf)
    with PdfPages(output_pdf) as pdf:
        for figure in figures:
            pdf.savefig(figure, bbox_inches="tight")
            plt.close(figure)

    logger.info("File executed successfully to end.")
    logger.info("Output file at %s", output_pdf)


def _plot_from_challenge_library(
    challenge_name: str,
    model_data_path: str,
    output_path: str,
) -> None:
    """Run challenge-library plotting workflow."""
    logger.info(
        "Library challenge plotting requested for %s with model data at %s and output path %s.",
        challenge_name,
        model_data_path,
        output_path,
    )
    raise NotImplementedError(
        "Library challenge plotting is not implemented yet."
    )


def plot(
    challenge_name: Optional[str] = None,
    model_data_path: Optional[str] = None,
    output_path: Optional[str] = None,
    config_path: Optional[str] = None,
) -> None:
    """
    Main execution function for the `epibench plot` pipeline.
    """
    using_library_challenge = challenge_name is not None or model_data_path is not None
    using_config = config_path is not None

    if using_library_challenge and using_config:
        raise click.UsageError(
            "Use either a library challenge with --score-file-path or --config-path, not both."
        )

    if using_config:
        if (
            challenge_name is not None
            or model_data_path is not None
            or output_path is not None
        ):
            raise click.UsageError(
                "When using --config-path, do not provide challenge-name, "
                "--score-file-path, or --output-path."
            )
        _plot_from_config(config_path=config_path)
        return

    if challenge_name is None and model_data_path is None:
        raise click.UsageError(
            "Provide either <challenge-name> with --score-file-path or --config-path."
        )
    if challenge_name is None:
        raise click.UsageError(
            "A library challenge name is required when using --score-file-path."
        )
    if model_data_path is None:
        raise click.UsageError(
            "--score-file-path is required when using a library challenge."
        )
    if output_path is None:
        raise click.UsageError(
            "--output-path is required when using a library challenge."
        )

    _plot_from_challenge_library(
        challenge_name=challenge_name,
        model_data_path=model_data_path,
        output_path=output_path,
    )
