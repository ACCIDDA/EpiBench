# `epibench plot`

Running `epibench plot --config-path ".../..."` via the command line will generate a set of graphics to help visualize your model(s) scores. The graphics will be saved in PDF format.

## Config file

The configuration file for an `epibench plot` run only takes in two keys: 

* `score_file_path`: a path to an `EpiBenchmark_scores.csv` file
* `output_path`: path where you would like the PDF output to be saved

## Output 

Currently, `epibench plot` produces 3 plots for visualizing the output of `epibench score`:

* plot 1: **Total WIS components by model**
    * a horizontal stacked bar chart that sums each model's WIS across all scored forecast units and decomposes it into underprediction, dispersion, and overprediction.
* plot 2: **Mean relative WIS by model and horizon**
    * a heatmap of relative WIS for each model-horizon pair; demonstrating how each model performs relative to the baseline at each forecast horizone (rWIS < 1 is better than th baseline, rWIS > 1 is worse).
* plot 3: **Mean WIS by reference date**
    * a time-series line plot of each model's mean WIS over date of reference; useful for understanding model performance over time. 

#### Hint: when scoring, it can be useful to list relevant submitting models via the `include_models` key. Doing so will allow you to compare your model data to other models in the hub.

The PDF output will be named `EpiBenchmark_plots.pdf`.

## example usage:

```bash
epibench plot --config-path "configs/plotting-config.yml"
```
where `--config-path` is the path to your YAML configuration file.
