# Clock Test - Libet Clock Task

A user-friendly implementation of the classic Libet clock task for studying the timing of conscious intention. This repository contains task scripts that present participants with a fast-rotating clock and collect introspective reports about when they experienced the intention to act.

## What is the Libet Clock Task?

The Libet clock task is a psychological experiment that investigates the relationship between conscious intention and brain activity. Participants watch a dot rotate around a clock face and report when they first experienced the intention to perform an action (like pressing a button).

This implementation is based on the classic study by Libet, B., Gleason, C.A., Wright, E.W., & Pearl, D.K. (1983) and was originally developed for:

> Vinding, M.C., Pedersen, M.N., & Overgaard, M. (2013). Unravelling intention: Distal intentions increase the subjective sense of agency. *Consciousness and Cognition, 22(3)*, 810–815. https://doi.org/10.1016/j.concog.2013.05.003

## Prerequisites

Before running the experiment, you'll need:

- **Python 3.x** with the following packages:
  - PsychoPy (version 3.x recommended)
  - NumPy
  - Standard Python libraries (math, random, os, csv)
- **A computer monitor** (settings will need to be configured for your display)
- **Input device** (keyboard for participant responses)

## Quick Start

### 1. Installation
```bash
# Install PsychoPy (if not already installed)
pip install psychopy
```

### 2. Basic Configuration

Open the file `Clock test_2019.py` and adjust these key settings near the top of the file:

**Display Settings** (lines ~36-42):
```python
monDistance = 70        # Distance from participant to monitor (in cm)
monWidth = 30          # Width of your monitor (in cm)
circleRadius = 2       # Size of the clock circle (adjust if too big/small)
```

**Experiment Settings** (lines ~23-29):
```python
condition_keys = ['W-press','M-press']    # Which conditions to run
blockRepetitions = 2                      # How many times to repeat each condition
BlockTrials = 5                          # Number of trials per block
```

**Window Settings** (line ~118):
```python
fullscr=False    # Change to True for fullscreen mode
```

### 3. Running the Experiment

```bash
python "Clock test_2019.py"
```

The experiment includes:
- **Training trials** to help participants understand the task
- **Two main conditions**:
  - **W-press**: Report when you first *intended* to press
  - **M-press**: Report when you actually *pressed* the button

## Understanding the Conditions

- **W-press (Intention condition)**: Participants report the clock position when they first experienced the intention to press a button
- **M-press (Movement condition)**: Participants report the clock position when they actually pressed the button

These conditions help researchers study the timing difference between conscious intention and actual movement.

## Data Output

The experiment automatically saves data to CSV files in the same directory:
- Filename format: `subject_[ID]_[condition].csv`
- Contains trial-by-trial data including response times and clock positions
- Use the included R script in `util/import.R` for data analysis

## Troubleshooting

**Common Issues:**

- **"Module not found" errors**: Make sure PsychoPy and NumPy are installed
- **Window doesn't appear**: Check your `fullscr` and monitor settings
- **Clock appears too small/large**: Adjust `circleRadius` in the configuration
- **Audio issues on Windows**: The script may show timing warnings for `winsound` - this is expected

**Need Help?**
- Check that your Python version is compatible with PsychoPy 3.x
- Ensure your monitor settings match your actual hardware
- For research use, test thoroughly with your specific setup

## License and Usage
This software is free to use under the **BSD 2-Clause License**.

### Citation

If you use this software in your research, please cite the original paper in your methods section:

> *"We used a modified open-source version of the Libet-clock task (Libet et al., 1983) originally used in Vinding et al. (2013) written in PsychoPy (Peirce et al. 2019)"*

Consider adding a link to this GitHub repository in the Code Availability section of your paper.

## Important Notes

- This software comes with **no warranty or guarantee**
- The "letterMode" feature from the original 2013 paper is not available in the current version
- Test thoroughly with your specific experimental setup before collecting research data
- This task measures timing judgments of intention and action, not "free will" per se

## Version History

- **2012-2014**: Original version written in PsychoPy2
- **2018-2023**: Rewritten and updated for PsychoPy3 compatibility
- **Current**: Stable version with W-press and M-press conditions

## Contact

For questions, bug reports, or suggestions:
**Email**: mikkelcv@drcmr.dk

---

*Happy experimenting! 🧠⏰*
