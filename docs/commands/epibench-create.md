# `epibench create`

Running `epibench create --config-path "../.."` will fetch and orgnize vintaged ground truth data from a forecasting hub based on the specifications you have written in your config. That is, if you wanted to run your model on the ground truth influenza data that was available on date `YYYY-MM-DD`, `epibench create` will visit the correct hub, retrieve the ground truth file from that day in the past, and return it to you in a nested format.

## Config file 

The configuration file for an `epibench create` run takes in the following keys:

* `hub_path`: a path to a local hub repo clone, or to a hub GitHub repo URL 
* `challenge_name`: whatever name you would like to give the "challenge" you are defining
* `target`: the single target whose ground truth you would like to fetch; it must exactly match the source data when that data contains a `target` column
* `ground_truth_file`: a relative path, from the hub root, to the CSV or Parquet ground truth file
* `observed_column_name`: the source column containing observed values
* `location_column_name`: the source column containing locations
* `date_column_name`: the source column containing target end dates
* `dates`: which dates of reference you want to fetch ground truth data for (`YYYY-MM-DD`)
    * this can be passes as a list of individually-specified dates, 
    * or as a dictionary with three keys: `start_date`, `end_date`, `freq`
        * `freq` format must be `"<n> weeks"` or `"<n> week"`
    * **important: your dates must match the submission cadence of the hub you have provided for a given season.** If your `epibench create` run spans more than a season, the process will exit and ask that you limit to one season at a time.
* `vintaging`: TRUE/FALSE; TRUE if you would like ground gruth data to be vintaged, FALSE if you just want to fetch the most recently available data across your date range
* `vintagin_method`: if vintaging, choose `"as_of"` or `"checkout"`
    * when set to `"as_of"`, data will be pulled from a continuously updated ground truth data file (where reference date matches the reported `as_of` date)
    * when set to `"checkout"`, data will be pulled from the commit that happened on the reference date via `git checkout`
* `vintaging_offset`: if vintaging, elect an integer vintaging offset
    * many hubs take forecasting submission a few days before the reported reference date (e.g., forecasts are made on Wednesday, but the reference date is the following Saturday, creating an offset of `-3` days). For maximum realism, you can inform `epibench create` of this and it will ensure you do not get any ground truth data that would have been filled in (e.g.) between the Wednesday and the Saturday.
    * if you would like no offset, pass `0`
    * when possible, `epibench create` will match you `vintaging_offset` value with the submisison cadence of the hub and give warning if your value does not match the hub

See our [configuration templates](../getting-started/configuration-templates.md) for a copy-pasteable template of the `epibench create` config.

## Output

Upon a successful `epibench create` run, you can expect a single folder to appear at your `--output-path`. The folder will be named by whatever string you set as `challenge_name` in the configuration file, followed by a ten-character hash that is both unique to your specifications and reproducible. Within the folder, you would find the following nested structure: 

```
output_path/
└── my-covid-challenge_b7bb9fbf7c/
    ├── task_list.csv
    └── gt/ 
        ├── 2026-01-01/
        │   └── 20260101_gt.csv
        ├── 2026-01-08/
        │   └── 20260108_gt.csv
        ├── 2026-01-15/
        │   └── 20260115_gt.csv
        ├── 2026-01-22/
        │   └── 20260122_gt.csv
        └── 2026-01-29/
            └── 20260129_gt.csv
```

Where each requested date of reference has its own folder and file within the `gt/` directory, and the `task_list.csv` file give relative paths to ground truth data files for each date of reference.

Each generated ground truth file uses the standardized columns `target_end_date`, `location`, and `observed`.

## example usage

An example config could look like this:
```bash
epibench create --config-path "path/to/create-config.yml"
```
where `--config-path` is the path to your YAML configuration file.
