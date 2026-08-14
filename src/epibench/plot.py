"""Run the `plot` pipeline and export a PDF of summary figures."""

from __future__ import annotations

import logging
from typing import Optional

import click
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from .build_plots import build_summary_figures, load_scores
from .load_library_challenge import load_library_challenge
from .path_utils import resolve_output_dir, resolve_path, establish_hub_path
from .prep_complete_models_for_plotting import prep_complete_models_for_plotting
from .scoring_bridge import ScoringBridge


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 

PLOTS_FILENAME = "EpiBenchmark_plots.pdf"

def _plot_from_score_file(score_file_path: str, output_path: str) -> None:
    """Run the direct score-file plotting workflow."""

    # load and validate score file
    resolved_score_file_path = resolve_path(score_file_path)
    if not resolved_score_file_path.exists():
        raise FileNotFoundError(f"Score file not found: {resolved_score_file_path}")
    if not resolved_score_file_path.is_file():
        raise ValueError(
            f"--score-file-path must be a file. Received: {resolved_score_file_path}"
        )
    output_dir = resolve_output_dir(output_path, files_to_save=[PLOTS_FILENAME])
    logger.info("Loading and validating scoring output...")
    score_df = load_scores(resolved_score_file_path)

    # build plots 
    logger.info("Building figures...")
    figures = build_summary_figures(score_df)
    logger.info("Success ✅")

    # save
    output_pdf = output_dir / PLOTS_FILENAME
    logger.info("Writing PDF to %s", output_pdf)
    with PdfPages(output_pdf) as pdf:
        for figure in figures:
            pdf.savefig(figure, bbox_inches="tight")
            plt.close(figure)
    logger.info("Success ✅")
    logger.info("File executed successfully to end 🎉")
    logger.info("Output file at %s", output_pdf)


def _plot_from_challenge_library(
    challenge_name: str,
    score_file_path: str,
    output_path: str,
    challenge_definition: dict[str, object],
) -> None:
    """Run challenge-library plotting workflow."""

    logger.info(
        "Initiating plotting for library challenge %s with score file at %s and output path %s.",
        challenge_name,
        score_file_path,
        output_path,
    )
    # load and validate user's score file
    resolved_score_file_path = resolve_path(score_file_path)
    if not resolved_score_file_path.exists():
        raise FileNotFoundError(f"Score file not found: {resolved_score_file_path}")
    if not resolved_score_file_path.is_file():
        raise ValueError(
            f"--score-file-path must be a file. Received: {resolved_score_file_path}"
        )
    output_dir = resolve_output_dir(output_path, files_to_save=[PLOTS_FILENAME])
    logger.info("Loading and validating scoring output...")
    baseline_model = challenge_definition["baseline_model"]
    users_scores = load_scores(resolved_score_file_path)
    # if multiple model names (aside from baseline) are found in data, fail
    non_baseline_models = set(users_scores[users_scores["model"] != baseline_model]["model"])
    if len(non_baseline_models) > 1:
        raise ValueError(
            f"Please only supply a single model's scores via `--score-file-path`. "
            f"Received: {non_baseline_models} (baseline model {baseline_model} does not count towards model total)."
        )
    else:
       users_model_name = list(non_baseline_models)[0] 

    # send challenge's complete models to scoring pre-processing
    logger.info("Retrieving external model data...")
    resolve_output_dir(output_path, files_to_save=[PLOTS_FILENAME])
    hub_path = establish_hub_path(hub_path_value=challenge_definition["hub_path"])
    complete_models = challenge_definition["complete_models"]
    # if the user's model is referenced by name in `complete_models`, drop from list
    if users_model_name.isin(complete_models):
        complete_models.remove(users_model_name)
    valid_locations = challenge_definition["locations"]
    valid_quantiles = challenge_definition["quantiles"]
    valid_horizons = challenge_definition["horizons"]
    valid_reference_dates = challenge_definition["reference_dates"]
    valid_target = challenge_definition["target"]
    complete_models_data = prep_complete_models_for_plotting(
        hub_path=hub_path,
        complete_models=complete_models,
        baseline_model=baseline_model,
        valid_locations=valid_locations,
        valid_quantiles=valid_quantiles,
        valid_horizons=valid_horizons,
        valid_reference_dates=valid_reference_dates,
        valid_target=valid_target
    )

    # score the external model data, filter out baseline (already exists in user's EpiBenchmark_scores.csv)
    scorer = ScoringBridge(baseline_model=baseline_model)
    scores = scorer.score_forecasts(complete_models_data)
    complete_models_scores = scores[scores["model"] != baseline_model]

    # concatenate complete models' scores with user-provided score file
    combined_scores_df = pd.concat([complete_models_scores, users_scores], ignore_index=True)

    # build plots
    logger.info("Building figures...")
    figures = build_summary_figures(combined_scores_df)
    logger.info("Success ✅")

    # save
    output_pdf = output_dir / PLOTS_FILENAME
    logger.info("Writing PDF to %s", output_pdf)
    with PdfPages(output_pdf) as pdf:
        for figure in figures:
            pdf.savefig(figure, bbox_inches="tight")
            plt.close(figure)
    logger.info("Success ✅")
    logger.info("File executed successfully to end 🎉")
    logger.info("Output file at %s", output_pdf)
    

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

    challenge_definition = load_library_challenge(challenge_name)
    _plot_from_challenge_library(
        challenge_name=challenge_name,
        score_file_path=score_file_path,
        output_path=output_path,
        challenge_definition=challenge_definition,
    )
