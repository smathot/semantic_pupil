#!/usr/bin/env python3

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

from datamatrix.rbridge import lme4
from datamatrix import series
from matplotlib import pyplot as plt
from analysis import pupil
from datamatrix import plot
from datamatrix.colors.tango import *
import numpy as np


def annotated_plot(dm):

	plot.new(size=(8,6))
	lm = trace_lmer_simple(dm)
	plt.axvline(792, color='black', linestyle=':')
	x = np.arange(3000)
	for color, a in [('black', .05), ('orange', .01), ('red',.005)]:
		threshold = series.threshold(lm.p,
			lambda p: p > 0 and p<a, min_length=1)
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


def trace_lmer_simple(dm, dv='type'):

	dm = (dm.type == 'light') | (dm.type == 'dark')
	lm = lme4.lmer_series(dm,
		'pupil ~ (%(dv)s) + (1+%(dv)s|subject_nr) + (1+%(dv)s|word)' \
		% {'dv' : dv}, winlen=300, cacheid='lmer_series_simple.%s' % dv)
	return lm


def model_comparison(dm):

	plot.new()
	for dv in ['type', 'rating_brightness', 'rating_intensity',
		'rating_valence']:
		print(dv)
		lm = trace_lmer_simple(dm, dv=dv)
		plt.plot(lm.t[1], label=dv)
	plt.legend(frameon=False)
	plot.save('model_comparison')
