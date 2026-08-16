# Rdataanalysis

Data analysis utilities.

## Reason category analysis

`scripts/reason_category_analysis.py` performs a full inventory of the
`Reason` column in `rw_analysis_final.xlsx`. Rows may contain multiple
semicolon-separated reason codes (optionally prefixed with `+`); the script
splits, cleans, and counts each distinct reason, then reports:

- the number of unique reason categories,
- the average number of reasons per record,
- a frequency table (count + percentage of records) for every reason.

The frequency table is printed to the console and saved as a CSV.

### Usage

```bash
pip install -r requirements.txt
python scripts/reason_category_analysis.py \
    --input path/to/rw_analysis_final.xlsx \
    --output output/reason_categories.csv
```

Both `--input` and `--output` are optional (see the script for defaults).
