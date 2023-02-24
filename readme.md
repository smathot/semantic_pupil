# Experimental resources for the study "Semantic Pupil"

Copyright 2015-2023 Sebastiaan Mathôt, Kristof Strijkers, Jonathan Grainger

- <s.mathot@cogsci.nl>
- <http://www.cogsci.nl/smathot>

# Table of contents

- About this repository
- Running the experiments
- Participant data
- Running the analysis
- License


# About this repository

This repository contains materials to accompany the following manuscript:

Mathôt, S., Strijkers, K., & Grainger, J. (2017). Pupillary responses to words that convey a sense of brightness or darkness. *Psychological Science*. <https://doi.org/10.1177/0956797617702699>


# Running the experiments

The experiments are placed in the `experiments` subfoler.

All experiments were conducted with [OpenSesame](http://osdoc.cogsci.nl/), but not all with the same version.

- visual experiment: 2.9.6 (with EyeLink plugins, which need to be installed separately)
- ratings experiment: 3.0.0
- auditory experiment: 3.1.0
- valence-control experiment: 3.1.3


# Participant data

## Eye-tracking data

The eye-tracking data for each experiment is located in `analysis/edf/[experiment name]`. This in `.edf` format, which is the format used by the EyeLink eye tracker.

To run the analysis as described below, the `.edf` files need to be converted to `.asc` files using the `edf2asc` utility that can be downloaded for free from the SR Research forum (registration required)

The `.asc` files then need to be placed in a folder called `analysis/data-pupil-asc/[experiment name]`. This folder needs to be created.

## Ratings data

The ratings data is located in `analysis/data-ratings`. This in standard comma-separated values (`.csv`) format.


# Running the analysis

Before analyzing the data, the eye-tracking data needs to be converted as described above.

Analysis scripts and participant data are placed in the `analysis` subfolder.

## IPython notebook

For a quick example of how the analysis works, see this IPython notebook:

- [analysis/basic-analysis.ipynb](analysis/basic-analysis.ipynb)

## Full analysis pathway

The analysis requires the standard numpy/ scipy stack, and [DataMatrix](https://github.com/smathot/python-datamatrix) and [EyelinkParser](https://github.com/smathot/python-eyelinkparser).

First, parse the ratings data by running:

	python3 analyze-ratings.py

This will create a file called `ratings.csv`, which is used for the main analyses.

Next, run the full analysis for the visual experiment:

	python3 analyze-pupil.py --auditory @full

And for the auditory experiment:

	python3 analyze-pupil.py --visual @full
	
And for the control experiment:

	python3 analyze-pupil.py --control @annotated_valence_plot
	
Various other analyses can be performed as well. The logic is that you can execute a function in one of the analysis modules by passing `@[function name]` as argument.

During the analysis, cache files are created. To start from scratch, pass the `--clear-cache` argument.

Notes:

- *térébrant* was misspelled and therefore removed from the analysis.
- *pénombre* occurred twice in the stimulus list of the pupillometry experiment.


# License

- Analysis and experimental code are released under a [GNU General Public License 3](https://www.gnu.org/copyleft/gpl.html).
- Data and text are released under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
