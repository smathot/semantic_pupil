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

from datamatrix import io, IntColumn, FloatColumn, cached
from datamatrix import operations as ops
from datamatrix import series
import numpy as np
from analysis import constants


@cached
def filter_(dm):

	"""
	desc:
		Applies basic filtering to the parsed data, by removing unnecessary
		columns, filtering out practice trials, etc. This function does not do
		pupil-size preprocessing; this is handled by pupil.preprocess()

	arguments:
		dm:
			type: DataMatrix

	returns:
		type:	DataMatrix
	"""

	# Keep only relevant columns to speed up processing
	ops.keep_only(dm, ['trialid', 'word', 'type', 'ptrace_target', 'category',
		'ptrace_fixation', 'subject_nr', 'response_time_keyboard_response',
		'correct_keyboard_response', 'practice', 'valence'])
	dm.rename('response_time_keyboard_response', 'rt')
	dm.rename('correct_keyboard_response', 'correct')
	# Remove practice trials, and the misspelled word
	print('Filtering')
	if constants.EXP in ('control', 'dutch'):
		dm = dm.practice == 'no'
	else:
		dm = dm.trialid >= 10
		dm = dm.word != 'trbrant'
	# Show all words and trialcounts
	for word in dm.word.unique:
		print('%s\t%d' % (word, len(dm.word == word)))
	# First show error information, and then remove error trials
	errors = len(dm.correct == 0)
	error_percent = 100. * errors / len(dm)
	n_word = len(dm.word.unique)
	print('N(word) = %d Errors(Total) = %d (%.2f %%) of %d' \
		% (n_word, errors, error_percent, len(dm)))
	if constants.EXP == 'control':
		categories = ('positive', 'negative', 'animal')
	elif constants.EXP == 'dutch':
		# Remap the slightly different coding for the Dutch experiment
		categories = 'light', 'dark', 'ctrl', 'animal'		
		dm.type = ''
		for row in dm:
			if row.category == 'control':
				row.type = 'ctrl'
			else:
				row.type = row.category
	elif constants.EXP in ('visual', 'auditory'):
		categories = 'light', 'dark', 'ctrl', 'animal'
	else:
		assert(False)
	for type_ in categories:
		if constants.EXP == 'control':
			dm_ = dm.category == type_
		else:
			dm_ = dm.type == type_
		total = len(dm_)
		errors = len((dm_) & (dm.correct == 0))
		error_percent = 100. * errors / total
		n_word = len(dm_.word.unique)
		print('N(word, %s) = %d, Errors(%s) = %d (%.2f %%) of %d' \
			% (type_, n_word, type_, errors, error_percent, total))
	dm = dm.correct == 1
	if constants.EXP in ('control', 'dutch'):
		return dm
	# Add new columns
	print('Adding columns')
	dm.rating_brightness = FloatColumn
	dm.rating_valence = FloatColumn
	dm.rating_intensity = FloatColumn
	dm.word_len = IntColumn
	dm.word_len = [len(word) for word in dm.word]
	# Integrate the normative ratings and French lexicon project into the data
	print('Integrating normative ratings')
	ratings = io.readtxt('ratings.csv')
	ratings.ascii_word = [word.encode('ascii', errors='ignore') \
		for word in ratings.word]
	for row in dm:
		# The animal names haven't been rated
		if row.type == 'animal':
			continue
		# The special characters have been stripped in the EDF file, but not from
		# the ratings data. We assert that we have exactly one match between the
		# ascii-fied and original word to make sure that we map things correctly.
		# In addition, in the auditory experiment the special characters were
		# converted to html hex notation. So we strip those characters.
		word = ''.join([l for l in row.word if l.isalpha()])
		rating = ratings.ascii_word == word
		assert(len(rating) == 1)
		row.rating_brightness = rating.rating_brightness[0]
		row.rating_valence = rating.rating_valence[0]
		row.rating_intensity = rating.rating_intensity[0]
	return dm


def descriptives(dm):

	"""
	desc:
		Provides basic descriptives of response times. These are printed
		directly to the stdout.

	arguments:
		dm:
			type: DataMatrix
	"""
	
	if constants.EXP == 'control':
		ops.keep_only(dm, cols=['category', 'rt'])
		gm = ops.group(dm, by=[dm.category])
	else:
		ops.keep_only(dm, cols=['type', 'rt'])
		gm = ops.group(dm, by=[dm.type])
	gm.mean_rt = series.reduce_(gm.rt)
	gm.se_rt = series.reduce_(gm.rt, lambda x: np.nanstd(x)/np.sqrt(len(x)))
	gm.n = series.reduce_(gm.rt, lambda x: np.sum(~np.isnan(x)))
	del gm.rt
	print(gm)
