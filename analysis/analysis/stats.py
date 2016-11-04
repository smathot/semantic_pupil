# coding=utf-8

"""
This file is part of P0005.1.

P0005.1 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

P0005.1 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with P0005.1.  If not, see <http://www.gnu.org/licenses/>.
"""

from analysis.constants import *
from analysis import pupil
from datamatrix.rbridge import lme4
from datamatrix import series
from matplotlib import pyplot as plt
from datamatrix import plot
from datamatrix.colors.tango import *
import numpy as np


def annotated_plot(dm):

	"""
	desc:
		Plots mean pupil size separately for dark and bright trials, and
		annotates the plot with significance markers.

	arguments:
		dm:
			type: DataMatrix
	"""

	plot.new(size=(8,6))
	lm = trace_lmer_simple(dm)
	plt.axvline(RT, color='black', linestyle=':')
	x = np.arange(3000)
	for color, a in [
			('black', 1.96), # p < .05
			('red', 2.57), # p < .01
			('orange', 2.81), # p < .005
			('yellow', 3.29) # p < .001
			]:
		threshold = series.threshold(lm.t,
			lambda t: abs(t) > a, min_length=1)
		print('Alpha %.5f (%.2f)' % (a, series.reduce_(threshold)[1]))
		plot.threshold(threshold[1], color=color, linewidth=1)
	dm_dark = dm.type == 'ctrl'
	plot.trace(dm_dark.pupil, color=grey[3],
		label='Neutral (N=%d)' % len(dm_dark))
	pupil.brightness_plot(dm, subplot=True)
	plt.xticks(range(0, 3001, 500), np.linspace(0,3,7))
	plt.xlabel('Time since word onset (s)')
	plt.ylabel('Pupil size (normalized to word onset)')
	plot.save('annotated_plot')


def trace_lmer_simple(dm, iv='type'):

	"""
	desc:
		Runs the main LME for each 10 ms window separately. Here the word type
		(bright or dark) is a fixed, pupil size is a dependent measure, and the
		model contains random by-participant slopes and intercepts.

	arguments:
		dm:
			type: DataMatrix

	keywords:
		iv:		The independent variable.

	returns:
		desc:	A DataMatrix with statistical results.
	"""

	dm = (dm.type == 'light') | (dm.type == 'dark')
	lm = lme4.lmer_series(dm,
		'pupil ~ (%(iv)s) + (1+%(iv)s|subject_nr)' \
		% {'iv' : iv}, winlen=WINLEN, cacheid='lmer_series_simple.%s' % iv)
	return lm


def trace_lmer_ratings(dm, dv='rating_brightness'):

	"""TODO"""

	dm = dm.type != 'animal'
	print(dm.type.unique, dv)
	lm = lme4.lmer_series(dm,
		'pupil ~ (%(dv)s) + (1+%(dv)s|subject_nr)' \
		% {'dv' : dv}, winlen=WINLEN, cacheid='lmer_series_ratings.%s' % dv)
	threshold = series.threshold(lm.p,
		lambda p: p > 0 and p<.05, min_length=200)
	print('Alpha .05 (%.2f)' % series.reduce_(threshold)[1])
	plt.plot(lm.t[1])
	plot.threshold(threshold[1], color=blue[1], linewidth=1)
	plt.show()
	return lm


def model_comparison(dm):

	"""TODO"""

	plot.new(size=(8,6))
	colors = brightcolors[:]
	for iv in ['rating_brightness', 'rating_valence', 'rating_intensity']:
		lm = trace_lmer_simple(dm, iv)
		plt.plot(np.abs(lm.t[1]), color=colors.pop(), label=iv)
	plt.legend()
	plt.xticks(range(0, 3001, 500), np.linspace(0,3,7))
	plt.xlabel('Time from word onset (s)')
	plt.ylabel('|t|')
	plot.save('model-comparison')
	
	
def brightness_intensity(dm):

	"""TODO"""

	lm = lme4.lmer_series((dm.type == 'light') | (dm.type == 'dark'),
		'pupil ~ type + rating_intensity + (1+type|subject_nr)',
		winlen=WINLEN, cacheid='lmer_series_type_intensity')
		
	threshold = series.threshold(lm.t, lambda t: abs(t) > 1.96, min_length=200)
	print('threshold', threshold > 0)
		
	plot.new(size=(8,6))
	plt.plot(threshold)
	plt.plot(lm.t[1], label='Type')
	plt.plot(lm.t[2], label='Intensity')
	plot.save('model-type-intensity')
	
	lm = lme4.lmer_series(dm.type != 'animal',
		'pupil ~ rating_brightness + rating_intensity + (1+rating_brightness|subject_nr)',
		winlen=WINLEN, cacheid='lmer_series_brightness_intensity')
	plot.new(size=(8,6))
	plt.plot(lm.t[1], label='Brightness')
	plt.plot(lm.t[2], label='Intensity')
	plot.save('model-brightness-intensity')
