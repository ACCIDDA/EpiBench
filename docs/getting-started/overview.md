# EpiBenchmark Overview

Once completing the installation instructions, you will have all EpiBenchmark commands available to you (see: `epibench --help`). EpiBenchmark allows users to interact with its benchmarking framework in two distinct ways: either through a challenge defined in our library, or through a challenge that they have defined themselves. The challenges in our [challenge library](../challenge-information/challenges.md) are comprised of a set combination of pathogen, dates, locations, horizons, and quantiles. In order to score your model data against a library challenge, your model data must have forecasts for all of the facets defined in the challenge. Alternatively, and more flexibly, you may define challenges/fetch ground truth for personal use, or score + plot model data unrelated to a challenge.

## Using a library challenge

- `epibench list`: Lists the challenges available in the bundled **challenge library**. [Learn more and browse the challenge catalog](../challenge-information/challenges.md).
- `epibench fetch <challenge-id> --output-path`: Downloads a challenge's data files from Zenodo
    - A challenge's data files include all the data you need to run your model for a challenge, including instruction files for an agent
- `epibench score <challenge-id> --model-data-path --model-name --output-path`: A command that scores model forecast data with a weighted interval score (WIS) and compiles all information into two CSVs:
    - `EpiBenchmark_scorecard.csv`: a scorecard, with one value for each metric defined in the challenge metrics
    - `EpiBenchmark_scores.csv`: a scores file, with all scores for all unique forecast units included in your model data
    - Note that your model data must contain every forecast unit combination defined in a challenge in order to be scored against it
- `epibench plot --config-path`: Using a `--config-path` argument, generate a set of plots for the visual analysis of your model performance in a library challenge

When scoring model data for a library challenge, you may only submit one model's data at a time

## Building your own challenge

- `epibench create --config-path`: A command that fetches and organizes ground truth data (of a specificed vintage) from a forecasting hub. In running this command with your specifications, you will have the vintaged (i.e., un-backfilled) ground truth data necessary to execute model runs from any date(s) of reference. The challenges you create with `epibench create` differ from the challenges in our library – our library challenges are static, and meant to represent specific forecasting requirements.
-  `epibench score --config-path` to score any model output
- `epibench plot --config-path` to visualize your scores


When using `epibench create`, `epibench plot`, (or `epibench score` outside of a library challenge), pass a single required `--config-path` flag – the path to a YAML configuration file with the parameters of each run. The configuration file for each command is slightly different; visit the [Configuration templates](configuration-templates.md) page to get copy/pasteable templates, or visit 'Workflows' for thorough explanation of configuration keys.


While each command is written to build off the others, all of the EpiBenchmark workflows can be run independently (i.e., `epibench create` is not a pre-requesite for `epibench score`, etc.).
