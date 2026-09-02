# Configuration templates

Only `epibench create`, and `epibench score` (when not being used for a library challenge) require YAML configuration files. Please see templates below.

## `epibench create`

```yaml
---

hub_path: "" # either a path to a local hub repo, or a URL to a hub GitHub repo

challenge_name: "whatever-you-want-to-call-this"

target: "target-name" # one target per create run; match must be exact

dates: {
    start_date: YYYY-MM-DD, # dates are inclusive on both ends [,]
    end_date: YYYY-MM-DD,
    freq: "n weeks" # format must be "<num> week" or "<num> weeks"
} 
# or, just a list of dates
# e.g.,
# dates: [YYYY-MM-DD, YYYY-MM-DD, YYYY-MM-DD]
# date provided must align with the cadence for the provided hub's submission schedule in a given season

vintaging: TRUE # or FALSE
vintaging_method: "checkout" # or "as_of"; not required when vintaging is set to FALSE
# "as_of" pulls from a continuously updated ground truth file, matching an as_of to date of reference
# "checkout" actually goes back to the date of reference in the git history
vintaging_offset: -3 # if your hub has an offset between the date forecasts are created and the date they "begin"
# many hubs have a -3 offset

output_path: "/..." # path to where you want output to be saved
```

## `epibench score`

#### Note: if you are scoring your model for a challenge in our challenge library, you need not write a config. Simply provide your, `--model-data-path`, `--model-data`, and `--output-path` as flags when you run `epibench score <challenge-id>`.

```yaml
---

hub_path: "" # either a path to a local hub repo, or a URL to a hub GitHub repo

evaluation_start_date: "YYYY-MM-DD" 
evaluation_end_date: "YYYY-MM-DD" # dates are inclusive on both ends [,]

target: "wk inc flu hosp" # only scores one target at a time; match must be exact

models: {
    "name-of-model1": "/path/to/model1-data", # paths can point to a folder of CSVs
    "name-of-model2": "/path/to/model2-data", # or to a single CSV;
    "name-of-model3": "/path/to/model3-data" # data will be concatenated regardless
} 
# non-quantile output will be filtered out

baseline_model: "HubName-baseline" # name of the baseline model for your provided hub

include_models: ["Hub-model-X", "Hub-model-Y"]
# optional parameter that allows you to select submitting models you 
# would like to be scored alongside your model(s)

output_path: "/..." # path to where you want output to be saved
```
