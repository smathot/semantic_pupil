# Experimental resources for the study "Semantic Pupil"

Copyright 2015-2017 Sebastiaan Mathôt, Kristof Strijkers, Jonathan Grainger

- <s.mathot@cogsci.nl>
- <http://www.cogsci.nl/smathot>

# About this repository

This repository contains materials to accompany the following manuscript:

Mathôt, S., Strijkers, K., & Grainger, J. (in press). Pupillary responses to words that convey a sense of brightness or darkness, *Psychological Science*.


## Running the experiments

The experiments are placed in the `experiments` subfoler.

All experiments were conducted with [OpenSesame](http://osdoc.cogsci.nl/), but not all with the same version.

- visual experiment: 2.9.6 (with EyeLink plugins, which need to be installed separately)
- ratings experiment: 3.0.0
- auditory experiment: 3.1.0
- valence-control experiment: 3.1.3


# Running the analysis

Analysis scripts and participant data are placed in the `analysis` subfolder.

## IPython notebook

For a quick example of how the analysis words, see this IPython notebook:

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
