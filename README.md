# Clock test
This repository conatins task scripts for obtaining introspective reports based on a fast rotating clock as made popular by Libet et al. (1983).

This version is written in PsychoPy (http://www.psychopy.org/). It was first used for the study:

> Vinding, M.C., Pedersen, M.N., & Overgaard, M. (2013). Unravelling intention: Distal intentions increase the subjective sense of agency. *Consciousness and Cognition, 22(3)*, 810–815. https://doi.org/10.1016/j.concog.2013.05.003

The script was written 2012-2014 for PsychoPy2. The current version is re-written 2018-2025 for PsychoPy3.

Download PsychoPy from https://psychopy.org/

## Use

### Quick Start
1. Open `Clock test_2025.py` in your PsychoPy environment
2. Configure the experimental parameters (see below)
3. Run the script

### Configuration
You can easily customize the adaptive timeout algorithm behavior by editing the config file without touching the main experimental script. The settings are properly documented with comments explaining their purpose and valid ranges.

**Important:** Adjust these settings before running the experiment:

#### Display Settings
- `monDistance`: Distance from subject's eyes to center of monitor (cm).
- `monWidth`: Physical width of monitor display (cm).
- `fullscr`: Set to `True` for fullscreen mode (recommended for experiments).
- `framerate`: Set the framerate of monitor (in Hz)

#### Experimental Design
- `condition_keys`: Choose which conditions to include (see table below).
- `blockRepetitions`: Number of repetitions of each condition block.
- `BlockTrials`: Number of trials per block.
- `trainingCondition_keys`: Conditions for practice trials.
- `trainingTrials`: Number of practice trials per condition.

#### Timing & Appearance
- `drawMode`: Visual style - `'dot'` or `'hand'`.
- `clockDirection`: `'clockwise'` or `'counterclockwise'`.

#### Output
- `triggerOutput`: Send trigger out for EEG during experiment (`True`/`False`).

### Data Output
Results are automatically saved as CSV files in the `data/` folder with the naming convention: `subject_[ID]_[condition][#].csv` (one file for each condition)

### OPTIONS FOR CONDITIONS:
this task can run several versions of task based on the Libet-clock method first described by Libet et al. (1983). Set which conditions to run in the experiments by specifying relevant keys in the `condition_keys` variable.

| Condition | Description | Original reference |
|-----------|-------------|-----------|
| `W-press` | Press. Report time of intention (W-time) | Libet et al. 1983 |
| `M-press` | Press. Report time of intention (M-time) | Libet et al. 1983 |
| `IB-press` | Press+tone. Indicate when a press is made. Part of the Intentional Binding paradigm | Haggard et al. 2002 |
| `IB-tone` | Press+tone. Indicate when a tone is heard. Part of the Intentional Binding paradigm | Haggard et al. 2002 |
| `IB-singleTone` | Tone. Indicate when a single tone is heard. Part of the Intentional Binding paradigm | Haggard et al. 2002 |
| `IB-singlePress` | Press. Indicate when a single press is made. Part of the Intentional Binding paradigm | Haggard et al. 2002 |
| `interruption` | Press. Random interruptions. Indicate when a single press is made. Libertus interuptus | Schurger et al. 2012 |


## Permissions
The scripts are free for any use following the BSD 2-Clause License.

If you use the script or modified versions of the script in your research please cite the paper above in your methods section, e.g.:

> _"We used a modified open-source version of the Libet-clock task (Libet et al., 1983) originally used in Vinding et al. (2013) written in PsychoPy (Peirce et al. 2019)"_

If relevant, add a link to this GitHub repository in the Code Availability section of your paper.

## Disclaimer

**Use at your own risk.** This software is provided "as is" without warranty of any kind, express or implied.

### Known Limitations
- **Experimental features**: *Intentional binding modes* and *letter mode* are not fully tested in the current version. Use with caution and validate results carefully.
- **Adaptive timeout**: Verify proper algorithm behavior.
- **Audio timing**: Sound output timing varies significantly across different hardware and operating systems. **Always test audio timing** on your specific setup before collecting data.
- **Platform compatibility**: While designed for cross-platform use, timing precision may vary between Windows, macOS, and Linux.

### Important Testing Requirements
1. **Validate timing precision** on your hardware before data collection
2. **Test audio latency** and synchronization with visual events
3. **Verify trigger timing** if using EEG/physiological recording
4. **Test adaptive timeout** algorithm behavior with pilot sessions for interruption condition
5. **Run pilot sessions** to ensure stable performance

### Theoretical Note
This task measures subjective timing reports and neural correlates of action preparation. It does not provide evidence for or against free will, regardless of claims in popular media or some academic interpretations.

## Contact
For questions and more information contact: mvi@psy.ku.dk

## References

### Papers using versions of this implementation:

Vinding, M.C., Pedersen, M.N., & Overgaard, M. (2013). Unravelling intention: Distal intentions increase the subjective sense of agency. *Consciousness and Cognition, 22(3)*, 810–815. https://doi.org/10.1016/j.concog.2013.05.003

Vinding, M.C., Jensen, M., & Overgaard, M. (2015). The time between intention and action affects the experience of action. *Frontiers in Human Neuroscience, 9*, 366. https://doi.org/10.3389/fnhum.2015.00366

Hall, S., van den Heever, D., Vinding, M.C., & Morris, L. (2020). Investigating motor preparatory processes and conscious volition using machine learning. *bioRxiv*. https://doi.org/10.1101/2020.09.07.286351


### Original clock method first described by:

Libet, B., Gleason, C.A., Wright, E.W., & Pearl, D.K. (1983). Time of conscious intention to act in relation to onset of cerebral activity (readiness-potential). *Brain, 106(3)*, 623–642. https://doi.org/10.1093/brain/106.3.623

### Intentional Binding paradigm:

Haggard, P., Clark, S., & Kalogeras, J. (2002). Voluntary action and conscious awareness. *Nature Neuroscience, 5(4)*, 382–385. https://doi.org/10.1038/nn827

### Libertus interruptus method:

Schurger, A., Sitt, J.D., & Dehaene, S. (2012). An accumulator model for spontaneous neural activity prior to self-initiated movement. *Proceedings of the National Academy of Sciences, 109(42)*, E2904–E2913. https://doi.org/10.1073/pnas.1210467109

### PsychoPy software:

Peirce, J., Gray, J.R., Simpson, S., MacAskill, M., Höchenberger, R., Sogo, H., Kastman, E., & Lindeløv, J.K. (2019). PsychoPy2: Experiments in behavior made easy. *Behavior Research Methods, 51(1)*, 195–203. https://doi.org/10.3758/s13428-018-01193-y
