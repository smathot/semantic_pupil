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
from datamatrix.colors.tango import *
from datamatrix import cached, DataMatrix, io, operations, series, FloatColumn
from datamatrix import plot
from matplotlib import pyplot as plt
import numpy as np


def preprocess(dm):

	"""
	desc:
		Performs pupil preprocessing, and removes trials where pupil size was
		unrealistic.
	"""

	dm.pupil = series.blinkreconstruct(dm.ptrace_target)
	dm.pupil.depth = 3000
	dm.pupil = series.smooth(dm.pupil, winlen=51)
	dm.pupil = series.baseline(dm.pupil, dm.pupil, 0, 1, method='divisive')
	# Remove all trials where pupil size has unrealistic values
	dm.pupilmax = FloatColumn
	dm.pupilmin = FloatColumn
	for row in dm:
		row.pupilmin = np.nanmin(row.pupil)
		row.pupilmax = np.nanmax(row.pupil)
		print(row.pupilmin, row.pupilmax)
	plot.new()
	# plot.histogram(dm.pupilmin, bins=100, range=(0, 5), color=red[1], alpha=.5)
	# plot.histogram(dm.pupilmax, bins=100, range=(0, 5), color=green[1], alpha=.5)
	plt.hist(dm.pupilmin, bins=100, range=(0, 5), color=red[1], alpha=.5)
	plt.hist(dm.pupilmax, bins=100, range=(0, 5), color=green[1], alpha=.5)
	l0 = len(dm)
	dm = (dm.pupilmin > PUPILRANGE[0]) & (dm.pupilmax < PUPILRANGE[1])
	l1 = len(dm)
	s = '%d of %d unrealistic values' % (l0-l1, l0)
	plt.title(s)
	plot.save('pupil-peaks')
	print(s)
	return dm


def size(dm, start=0, end=None):

	"""
	desc:
		Gets the mean pupil size during a time window.

	arguments:
		dm:
			type: DataMatrix

	keywords:
		start:	The start time.
		end:	The end time, or None for trace end.

	returns:
		type:
			ndarrray
	"""

	return series.reduce_(series.window(dm.pupil, start=start, end=end)).mean


def size_se(dm, start=0, end=None):

	"""
	desc:
		Gets the pupil-size standard error during a time window.

	arguments:
		dm:
			type: DataMatrix

	keywords:
		start:	The start time.
		end:	The end time, or None for trace end.

	returns:
		type:
			ndarrray
	"""

	s = series.reduce_(series.window(dm.pupil, start=start, end=end))
	return s.mean, s.std / len(s)**.5


def effect(dm, start=0, end=None):

	"""
	desc:
		Gets the difference in pupil size between dark and bright trials
		during a time window.

	arguments:
		dm:
			type: DataMatrix

	keywords:
		start:	The start time.
		end:	The end time, or None for trace end.

	returns:
		type:
			ndarrray
	"""

	dm_bright = dm.type == 'light'
	dm_dark = dm.type == 'dark'
	bright = series.reduce_(series.window(dm_bright.pupil, start=start, end=end))
	dark = series.reduce_(series.window(dm_dark.pupil, start=start, end=end))
	return dark.mean - bright.mean


def effect_se(dm, start=0, end=None):

	"""
	desc:
		Gets the standard error of the differencein pupil size between dark and
		bright trials during a time window.

	arguments:
		dm:
			type: DataMatrix

	keywords:
		start:	The start time.
		end:	The end time, or None for trace end.

	returns:
		type:
			ndarrray
	"""

	if EXP == 'control':
		dm_bright = dm.category == 'positive'
		dm_dark = dm.category == 'negative'
	else:
		dm_bright = dm.type == 'light'
		dm_dark = dm.type == 'dark'
	bright = series.reduce_(series.window(dm_bright.pupil, start=start, end=end))
	dark = series.reduce_(series.window(dm_dark.pupil, start=start, end=end))
	diff = dark.mean - bright.mean
	se = ( (bright.std**2 / len(bright)) + (dark.std**2 / len(dark)) )**.5
	return diff, se


def brightness_plot(dm, subplot=False):

	"""
	desc:
		Plots mean pupil size separately for dark and bright trials over time.

	arguments:
		dm:
			type: DataMatrix

	keywords:
		subplot:	Indicates whether a new plot should be created, or not.
	"""

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
		plot.save('brightness_plot')


def valence_plot(dm, subplot=False):

	"""
	desc:
		Plots mean pupil size separately for positive and negative trials over
		time.

	arguments:
		dm:
			type: DataMatrix

	keywords:
		subplot:	Indicates whether a new plot should be created, or not.
	"""

	if not subplot:
		plot.new()
	dm_pos = dm.category == 'positive'
	dm_neg = dm.category == 'negative'
	plot.trace(dm_pos.pupil, color=green[1],
		label='Positive (N=%d)' % len(dm_pos))
	plot.trace(dm_neg.pupil, color=red[1],
		label='Negative (N=%d)' % len(dm_neg))
	plt.legend(frameon=False)
	if not subplot:
		plot.save('valence_plot')


def intensity_plot(dm, subplot=False):

	if not subplot:
		plot.new()
	dm = dm.type != 'animal'
	dm.intensity = np.abs(dm.valence - 3)
	dm_lo, dm_med, dm_hi = operations.bin_split(dm.intensity, 3)
	plot.trace(dm_lo.pupil, color=blue[1],
		label='Low intensity (N=%d)' % len(dm_lo))
	plot.trace(dm_med.pupil, color=yellow[-1],
		label='Medium intensity (N=%d)' % len(dm_med))
	plot.trace(dm_hi.pupil, color=red[1],
		label='High intensity (N=%d)' % len(dm_hi))
	plt.xticks([0,1000,2000,3000], [0,1,2,3])
	plt.xlabel('Time since word onset(s)')
	plt.ylabel('Proportional pupil-size change')
	plt.legend(frameon=False)
	if not subplot:
		plot.save('intensity_plot')


def subject_diff_traces(dm):

	"""
	desc:
		Plots the difference in pupil size for dark and bright trials over time,
		separately for each participant.

	arguments:
		dm:
			type: DataMatrix
	"""

	plot.new()
	x = np.arange(dm.pupil.depth)
	for i, s in enumerate(dm.subject_nr.unique):
		print(s)
		_dm = dm.subject_nr == s
		plt.subplot(6,5,i+1)
		plt.title('Subject %d' % i)
		brightness_plot(_dm, subplot=True)
	plot.save('subject_diff_trace')


def subject_summary(dm, save=True):

	"""
	desc:
		Plots the mean difference in pupil size between dark and bright trials
		for each participant as a bar plot. The time window is indicated by the
		PEAKWIN constant. This data is also written to a .csv file.

	arguments:
		dm:
			type: DataMatrix
	"""

	x = np.arange(len(dm.subject_nr.unique))
	sm = DataMatrix(length=len(dm.subject_nr.unique))
	sm.subject_nr = 0
	sm.effect_win = FloatColumn
	sm.effect_win_se = FloatColumn
	sm.effect_full = FloatColumn
	sm.effect_full_se = FloatColumn
	for i, s in enumerate(dm.subject_nr.unique):
		_dm = dm.subject_nr == s
		sm.subject_nr[i] = s
		sm.effect_win[i], sm.effect_win_se[i] = effect_se(_dm,
			PEAKWIN[0], PEAKWIN[1])
		sm.effect_full[i], sm.effect_full_se[i] = effect_se(_dm)
	sm = operations.sort(sm, by=sm.effect_win)
	if save:
		plot.new(size=(4,3))
	plt.axhline(0, color='black')
	plt.plot(sm.effect_win, 'o-', color=green[-1])
	plt.errorbar(x, sm.effect_win, yerr=sm.effect_win_se, linestyle='',
		color=green[-1], capsize=0)
	plt.xlim(-1, 30)
	plt.ylabel('Pupil-size difference (normalized)')
	plt.xlabel('Participant')
	plt.xticks([])
	if save:
		plot.save('subject_summary')
		io.writetxt(sm, '%s/subject_summary.csv' % OUTPUT_FOLDER)


def word_summary(dm, save=True):

	"""
	desc:
		Plots the mean pupil size for dark and bright words as a bar plot. The
		time window is indicated by the PEAKWIN constant. This data is also
		written to a .csv file.

	arguments:
		dm:
			type: DataMatrix
	"""

	if EXP == 'control':
		dm = (dm.category == 'positive') | (dm.category == 'negative')
	else:
		dm = (dm.type == 'light') | (dm.type == 'dark')
	x = np.arange(dm.pupil.depth)
	sm = DataMatrix(length=len(dm.word.unique))
	sm.word = 0
	sm.type = 0
	sm.pupil_win = FloatColumn
	sm.pupil_win_se = FloatColumn
	sm.pupil_full = FloatColumn
	sm.pupil_full_se = FloatColumn
	for i, w in enumerate(dm.word.unique):
		_dm = dm.word == w
		sm.word[i] = w
		if EXP == 'control':
			sm.type[i] = (dm.word == w).category[0]
		else:
			sm.type[i] = (dm.word == w).type[0]
		sm.pupil_win[i], sm.pupil_win_se[i] = size_se(_dm,
			PEAKWIN[0], PEAKWIN[1])
		sm.pupil_full[i], sm.pupil_full_se[i] = size_se(_dm)
	sm = operations.sort(sm, sm.pupil_win)
	if save:
		io.writetxt(sm, '%s/word_summary.csv' % OUTPUT_FOLDER)
		plot.new(size=(4,3))
	dx = 0
	for color, type_ in ((orange[1], 'light'), (blue[1],'dark')):
		if EXP == 'control':
			type_ = 'positive'  if type_ == 'light' else 'negative'
		sm_ = sm.type == type_
		x = np.arange(len(sm_))
		plt.plot(sm_.pupil_win, 'o-', color=color)
		if type_ == 'dark':
			yerr = (np.zeros(len(sm_)), sm_.pupil_win_se)
		else:
			yerr = (sm_.pupil_win_se, np.zeros(len(sm_)))
		plt.errorbar(x, sm_.pupil_win, yerr=yerr, linestyle='', color=color,
			capsize=0)
	plt.xlim(-1, 33)
	plt.ylabel('Pupil size (normalized)')
	plt.xlabel('Word')
	plt.xticks([])
	if save:
		plot.save('word_summary')


def valence_summary(dm):

	"""
	desc:
		Plots pupil size by word valence or intensity.

	arguments:
		dm:
			type: DataMatrix
	"""


	assert(EXP == 'control')
	dm = dm.category != 'animal'
	sm = DataMatrix(length=len(dm.word.unique))
	sm.word = 0
	sm.valence = 0
	sm.pupil_win = FloatColumn
	sm.pupil_win_se = FloatColumn
	sm.pupil_full = FloatColumn
	sm.pupil_full_se = FloatColumn
	for i, w in enumerate(dm.word.unique):
		_dm = dm.word == w
		sm.word[i] = w
		sm.valence[i] = _dm[0].valence
		sm.pupil_win[i], sm.pupil_win_se[i] = size_se(_dm, 1500, 3000)
		sm.pupil_full[i], sm.pupil_full_se[i] = size_se(_dm)
	sm.intensity = np.abs(sm.valence-3)
	sm = operations.sort(sm, by=sm.intensity)
	print(sm)
	plt.plot(sm.valence, sm.pupil_full, 'o')
	plt.show()
