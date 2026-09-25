# Clock Test Data Import Script

## Overview

This folder contains example analysis scripts for the clock test data. Use these as examples on how to get started, and adapt them to your own experimental setup as needed.

The R script `import.R` imports and processes raw data files from clock test experiments. The script handles multiple subjects and experimental conditions, performs data cleaning, angle recalculations, and creates a consolidated dataset for analysis.

The R script `IB_examples.R` provides example calculations for intentional binding based on the imported clock test data.

## Purpose

The clock test is used to measure participants' mental timing, in Libet-style experiments or in the context of intentional binding - the subjective compression of time between voluntary actions and their sensory consequences.

The import script will read files from the main experiment assumed to be in the folder `data`:

```
clock_test/
├── analysis/
│   ├── import.R          # Main data import script
│   ├── IB_examples.R     # Example intentional binding calculations
│   └── README.md         # This documentation
├── raw_data/             # Raw CSV data files from experiment (default location)
├── data/                 # Processed and consolidated data files (default location)
└── ...
```

## Initial configuration

Before running the script, you should change the `datapath` and `subjects` variables in the import script to match the location on your machine and the id codes of your research participants:

```r
# Data directory path
datapath <- c('C:\\Users\\ncb623\\clock_test')

# Subject IDs to import
subjects <- c('666')  # Add your subject IDs here

# Experimental conditions. For example, if your experiment includes conditions like "IB-press" and "IB-tone", list them here:
conditions <- c("IB-press","IB-tone","IB-singlePress","IB-singleTone")

# Wildcard keys (if used in condition names). For example, if your conditions include "Self" or "Other" conditions (must be named in the filenames), you can specify the wildcard keys here. E.g.:
wildcard_keys <- c('Self', 'Other')

```

## Input Data Requirements

### File Naming Convention

Data files should be CSV format follow a naming pattern that includes:

- Subject ID (from the `subjects` list)
- Condition name (from the `conditions` list)
- Optional trailing numbers (e.g., `1`, `2` for different sessions/blocks)

**Example filenames:**

- `subject_666_IB-press1.csv`
- `subject_666_IB-tone2.csv`
- `subject_666_IB-singlePress.csv`

### Required Columns

Input CSV files must contain these columns:

- `ansAngle`: Participant's response angle on the clock
- `pressAngle`: Actual button press angle
- `userError`: Boolean flag for user errors
- `id`: Subject identifier

### Optional Columns

- Additional columns are preserved in the output

## Output

The script creates a consolidated dataset (`clock.data`) containing:

### Key Variables

| Variable | Type | Description |
|----------|------|-------------|
| `id` | factor | Participant identifier |
| `condition` | factor | Original condition name with block numbers |
| `no` | numeric | Trial number within block |
| `dotDelay` | numeric | Duration of dot display after last event (in frames) |
| `toneOnset` | numeric | Time of tone onset since trial start |
| `toneAngle` | numeric | Angle of dot when tone occurred |
| `pressOnset` | numeric | Time of button press since trial start |
| `pressAngle` | numeric | Angle of dot when button was pressed (potentially recalculated) |
| `ansAngle` | numeric | Participant's response angle on clock (potentially recalculated) |
| `ansTime` | numeric | Response time for angle selection |
| `userError` | logical | Boolean flag for user-identified errors |
| `response` | numeric | Response trigger code |
| `recalc` | logical | Boolean indicating if angle recalculation was performed for boundary crossings |
| `shiftAngle` | numeric | Angular difference (ansAngle - toneAngle OR pressAngle) |
| `shiftTime` | numeric | Temporal shift in milliseconds (shiftAngle converted to miliseconds by clock speed) |
| `condition1` | factor | Condition name (e.g., "IB-press") |
| `condition2` | factor | Wildcard modifier if present (factor levels>NA) |

## Usage

### Basic Usage

1. Place your CSV data files in the `data/` directory
2. Update the configuration section with your subject IDs and conditions
3. Run the script in R:

```r
source("analysis/import.R")
```

## Additional Scripts

### IB_examples.R

Example analysis script that calculates intentional binding (IB) effects from processed data:

- Checks for complete data across required conditions
- Computes mean error times and statistics per subject/condition
- Calculates IB effects: IB_press and IB_tone per subject

Run after `import.R`:

```r
source("analysis/import.R")
source("analysis/IB_examples.R")
```

* **Error flagging**: Uses `userError` column to identify problematic trials
* **File matching**: Only processes files that match subject and condition criteria

## Troubleshooting

### Common Issues

**No files found:**

- Check that `datapath` is correct
- Verify file naming matches subject/condition patterns
- Ensure files are CSV format with semicolon separators

**Empty files warning:**

- Some data files may be empty or corrupted
- The script will skip these automatically and continue processing

**Angle calculation errors:**

- Verify that `ansAngle` and `pressAngle` columns exist
- Check that angle values are in degrees (0-360)

### Error Messages

**"Warning: File is empty, skipping: [filename]"**

- The file exists but contains no data rows
- Check the original data file for corruption

**File reading errors:**

- Verify CSV format and semicolon separator
- Check for special characters in file names or data

## Technical Details

### Angle Recalculation Logic

The script handles cases where responses cross the 360°/0° boundary:

- **Case 1**: Response < 100° AND press > 270° → Add 360° to response
- **Case 2**: Response > 260° AND press < 100° → Add 360° to press

This ensures accurate calculation of the shortest angular distance.

## Dependencies

- Base R (no additional packages required)
- CSV files with semicolon separators
- Properly formatted input data

## Version Information

- **Created**: For clock test / intentional binding experiments
- **Clock Speed**: Default 2650ms (configurable)
- **Compatible**: R 3.0+ (base R functions only)

## Contact

For questions about this script or the clock test methodology, refer to the original experiment documentation or contact the research team: mvi@psy.ku.dk

https://github.com/mcvinding/clock_test