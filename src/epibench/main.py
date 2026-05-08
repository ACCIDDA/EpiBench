"""Main execution script for scoring quantile forecasts with scoringutils WIS"""

import argparse
import logging

from validate_config import validate_config
from extract_model_data_details import extract_model_data_details
from ground_truth import GroundTruth


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """
    Main execution function
    """
    parser = argparse.ArgumentParser(description = 'Score models over specified time frame using a config.')
    parser.add_argument("--config-path",
                        type=str,
                        required=False,
                        help="Absolute path to your YAML configuration file.")
    args = parser.parse_args()

    logger.info("Validating configuration file...")
    hub_path, evaluation_start_date, evaluation_end_date, model_info, output_path = validate_config(args.config_path)

    logger.info("Validating model data...")
    model_data_details, target, locations_list = extract_model_data_details( # presently only handles one target
        model_info=model_info, 
        eval_start_date=evaluation_start_date, 
        eval_end_date=evaluation_end_date
    )

    logger.info("Retrieving and formatting ground truth data...")
    gto = GroundTruth(
        hub_path=hub_path, 
        target=target, 
        locations=locations_list, 
        eval_start_date=evaluation_start_date, 
        eval_end_date=evaluation_end_date
    ) # access the actual DataFrame with gto.gt

    output_dict = {}
    for model in model_info:
        logger.info(f"Scoring model {model}...")
        # validate csv at path
        # score from start, end
        # add output table to dict 
        pass
    
    for modelname, output_table in output_dict:
        # save to output_path, fail if overwrite will occur
        pass

    # end 
    print("File executed successfully to end.\n\n\n")


if __name__ == "__main__":
    main()


