# Clock test
This repository conatins task scripts for obtaining introspective reports based on a fast rotating clock as made popular by Libet, B., Gleason, C.A., Wright, E.W., & Pearl, D.K. (1983). Time of conscious intention to act in relation to onset of cerebral activity (readiness-potential). *Brain, 106(3)*, 623–642.

This version is written in PsychoPy (http://www.psychopy.org/). It was first used for the study:

> Vinding, M.C., Pedersen, M.N., & Overgaard, M. (2013). Unravelling intention: Distal intentions increase the subjective sense of agency. *Consciousness and Cognition, 22(3)*, 810–815. https://doi.org/10.1016/j.concog.2013.05.003

The script was written 2012-2014 in PsychoPy2. The current version is re-written 2018-2023 for PsychoPy3.

## Use
The task is found in the script `Clock test_2019.py`. 

**Important:** bBefore you use the script you should adjust the settings in the script to match how you want to run the script. E.g., adjust the screen setting to fit your hardware and experimental setup. Then set the number of trials and conditions.

The current version [2023-04-30] has instructions for the "W-time" and "M-time" conditions. To choose what to run change the argument `condition_keys`. Can be `['W-press','M-press']`

## Permissions
The scripts are free to use following the BSD 2-Clause License.

If you use the script or modified versions of the script in your research please cite the paper above in your methods section, e.g.:

> _"We used a modified open-source version of the Libet-clock task (Libet et al., 1983) originally used in Vinding et al. (2013) written in PsychoPy (Peirce et al. 2019)"_

If relevant, add a link to this GitHub repository in the Code Availability section of your paper.

## Disclaimer
I provide no guarantee or warranty.

The "letterMode" used in the paper listed above is not working in the current version [2019-02-21].

This task does not measure free will no matter what people claim.

## Contact
For questions and more information contact: mikkelcv@drcmr.dk
