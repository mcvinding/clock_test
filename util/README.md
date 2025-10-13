# Clock Test Data Import Script

## Overview

This R script (`import.R`) imports and processes raw data files from clock test experiments. The script handles multiple subjects and experimental conditions, performs data cleaning, angle recalculations, and creates a consolidated dataset for analysis.

## Purpose

The clock test is used to measure participants' mental timing, in Libet-style experiments or in the context of intentional binding - the subjective compression of time between voluntary actions and their sensory consequences.

The import script will read files from the main experiment assumed to be in the folder `data`:

```
clock_test/
├── util/
│   ├── import.R          # Main import script
│   ├── README.md         # This documentation
│   └── ...
└── data/                 # Raw CSV data files
```

## Configurati
Before running the script, you should change the `datapath` and `subjects` variables in the import script to match the locatin on your machine and the id codes of your research participants:
```r
# Data directory path
datapath <- c('C:\\Users\\ncb623\\clock_test\\data')

# Subject IDs to import
subjects <- c('666')  # Add your subject IDs here

# Experimental conditions
conditions <- c("IB-press","IB-tone","IB-singlePress","IB-singleTone")

```

## Input Data Requirements

### File Naming Convention
Data files should be CSV format with semicolon separators (`;`) and follow a naming pattern that includes:
- Subject ID (from the `subjects` list)
- Condition name (from the `conditions` list)
- Optional trailing numbers (e.g., `_1`, `_2` for different sessions/blocks)

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
- Columns 11-15 are automatically removed (modify script if needed) - these are currently not used for anything.
- Additional columns are preserved in the output

## Output

The script creates a consolidated dataset (`clock.data`) containing:

### Key Variables

| Variable | Type | Description |
|----------|------|-------------|
| `id` | factor | Participant identifier |
| `condition` | factor | Original condition name |
| `condition_clean` | factor | Standardized condition name without numbers |
| `ansAngle` | numeric | Response angle (potentially recalculated) |
| `pressAngle` | numeric | Actual press angle (potentially recalculated) |
| `errAngle` | numeric | Angular error in degrees |
| `errTime` | numeric | Temporal error in milliseconds |
| `recalc` | logical | Boolean indicating if angle recalculation was performed |
| `userError` | logical | Boolean flag for user-identified errors |

## Usage

### Basic Usage
1. Place your CSV data files in the `data/` directory
2. Update the configuration section with your subject IDs and conditions
3. Run the script in R:

```r
source("util/import.R")
```

## Data Quality Checks

The script includes several built-in quality checks:

1. **Empty file detection**: Warns and skips files with no data
2. **Boundary crossing detection**: Identifies and handles 360°/0° crossings
3. **Error flagging**: Uses `userError` column to identify problematic trials
4. **File matching**: Only processes files that match subject and condition criteria

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