"""Function to get model data for models with 'complete' challenge satisfaction, prepare for scoring."""

import datetime
import pandas as pd
import logging
from pathlib import Path
from hubdata import connect_hub

logger = logging.getLogger(__name__) 


def prep_complete_models_for_plotting(
        hub_path: Path,
        complete_models: list[str],
        baseline_model: str,
        valid_locations: list[str],
        valid_quantiles: list[str],
        valid_horizons: list[str],
        valid_reference_dates: list[str],
        valid_target: str,
) -> pd.DataFrame:
    """
    For complete models found in a challenge definition, fetch their
    model data from a Hubdata hub connection, appropriately filter to
    match the challenge, and put into scoringutils format.

    Args:
        - hub_path: Path to the corresponding hub
        - baseline_model: baseline model for the hub
        - complete_models: list of models for which challenge completion has been satisfied
        - + All forecast unit facets + quantiles defined in the challenge JSON (locations, horizons, reference_dates, output_type_ids, target)

    Returns:
        A pd.DataFrame ready to enter scoringutils
    """

    # connect to hub
    full_hub_df = connect_hub(hub_path=hub_path).to_table().to_pandas()

    # get data types the way we want them
    full_hub_df['location'] = full_hub_df['location'].astype('string')
    full_hub_df['output_type_id'] = full_hub_df['output_type_id'].astype('string')
    full_hub_df['horizon'] = full_hub_df['horizon'].astype('float') # process as floats for versatility across all hubs (rsv stores as "1", flu stores as "1.0")
    valid_horizons_float = [float(x) for x in valid_horizons]
    valid_reference_dates_obj = [datetime.date.fromisoformat(d) for d in valid_reference_dates]

    # add baseline to processing list
    complete_models.append(baseline_model)

    # filter each model to match challenge definition 
    filtered_model_data = {}
    for model in complete_models:
        filtered_model_data[model] = full_hub_df[
            (full_hub_df['model_id'] == model) &
            (full_hub_df['reference_date'].isin(valid_reference_dates_obj)) &
            (full_hub_df['horizon'].isin(valid_horizons_float)) &
            (full_hub_df['target'] == valid_target) &
            (full_hub_df['output_type'] == 'quantile') &
            (full_hub_df['output_type_id'].isin(valid_quantiles)) &
            (full_hub_df['location'].isin(valid_locations))
        ]

    # re-concatenate filtered model data, put columns in scoringutils format
    df = pd.concat(filtered_model_data.values(), ignore_index=True)
    df.rename(columns={"model_id": "model", "output_type_id": "quantile_level", "value": "predicted"})

    logger.info("Success ✅")
    return df