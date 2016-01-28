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

from datamatrix import cached, DataMatrix, io, operations, series
from datamatrix.colors.tango import *
from datamatrix import plot
from matplotlib import pyplot as plt
from scipy.stats import nanmedian
import numpy as np

@cached
def preprocess(dm):

	dm.pupil = series.blinkreconstruct(dm.ptrace_target)
	dm.pupil.depth = 3000
	dm.pupil = series.smooth(dm.pupil, winlen=51)
	dm.pupil = series.baseline(dm.pupil, dm.pupil, 0, 1)
	return dm


def size(dm, start=0, end=None):

	return series.reduce_(series.window(dm.pupil, start=start, end=end)).mean


def effect(dm, start=0, end=None):

	dm_bright = dm.type == 'light'
	dm_dark = dm.type == 'dark'
	bright = series.reduce_(series.window(dm_bright.pupil, start=start, end=end))
	dark = series.reduce_(series.window(dm_dark.pupil, start=start, end=end))
	return dark.mean - bright.mean


def brightness_plot(dm, subplot=False):

	if not subplot:
		plot.new()
	dm_bright = dm.type == 'light'
	dm_dark = dm.type == 'dark'
	plot.trace(dm_bright.pupil, color=orange[1],
		label='Bright (N=%d)' % len(dm_bright))
	plot.trace(dm_dark.pupil, color=blue[1],
		label='Dark (N=%d)' % len(dm_dark))
	plt.legend(frameon=False)
	if not subplot:
		plot.save('brighness_plot')


def subject_diff_traces(dm):

	plot.new()
	x = np.arange(dm.pupil.depth)
	for i, s in enumerate(dm.subject_nr.unique):
		_dm = dm.subject_nr == s
		plt.subplot(5,6,i+1)
		plt.title('Subject %d' % i)
		brightness_plot(_dm, subplot=True)
	plot.save('subject_diff_trace')


def subject_diff_summary(dm):

	plot.new()
	x = np.arange(dm.pupil.depth)
	sm = DataMatrix(length=len(dm.subject_nr.unique))
	sm.subject_nr = 0
	sm.effect_win = 0
	sm.effect_full = 0
	for i, s in enumerate(dm.subject_nr.unique):
		_dm = dm.subject_nr == s
		sm.subject_nr[i] = s
		sm.effect_win[i] = effect(_dm, 1500, 2000)
		sm.effect_full[i] = effect(_dm)
	sm = operations.sort(sm, by=sm.effect_win)
	plt.axhline(0, color='black')
	plt.plot(sm.effect_win, 'o-', color=blue[1])
	plt.plot(sm.effect_full, 'o-', color=green[1])
	plot.save('subject_diff_summary')
	io.writetxt(sm, 'output/subject_diff_summary.csv')


def word_summary(dm):

	dm = (dm.type == 'light') | (dm.type == 'dark')
	x = np.arange(dm.pupil.depth)
	sm = DataMatrix(length=len(dm.word.unique))
	sm.word = 0
	sm.type = 0
	sm.pupil_win = 0
	sm.pupil_full = 0
	for i, w in enumerate(dm.word.unique):
		_dm = dm.word == w
		sm.word[i] = w
		sm.type[i] = (dm.word == w).type[0]
		sm.pupil_win[i] = size(_dm, 1500, 2000)
		sm.pupil_full[i] = size(_dm)
	sm = operations.sort(sm, sm.pupil_win)
	plot.new()
	plt.axhline(0, color='black')
	for i, row in enumerate(sm):
		x = i-.4
		if row.type == 'light':
			color = orange[1]
		else:
			color = blue[1]
		plt.bar(x, row.pupil_win, color=color)
		plt.plot(x, row.pupil_full, '.', color='black')
		print(row.type, row.pupil_win)
	plt.xticks(range(len(sm)), sm.word, rotation=90)
	plt.ylim(.8, 1.1)
	plt.xlim(-1, len(sm))
	plot.save('word_summary')
	io.writetxt(sm, 'output/word_summary.csv')
