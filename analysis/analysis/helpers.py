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

@cached
def filter_(dm):

	# Keep only relevant columns to speed up processing
	ops.keep_only(dm, ['trialid', 'word', 'type', 'ptrace_target',
		'ptrace_fixation', 'subject_nr', 'response_time', 'correct'])
	# Remove practice trials, and the misspelled word
	print('Filtering')
	dm = dm.trialid >= 10
	dm = dm.word != 'trbrant'
	# First show error information, and then remove error trials
	errors = len(dm.correct == 0)
	error_percent = 100. * errors / len(dm)
	print('Errors(Total) = %d (%.2f %%) of %d' \
		% (errors, error_percent, len(dm)))
	for type_ in ('light', 'dark', 'ctrl', 'animal'):
		total = len(dm.type == type_)
		errors = len((dm.type == type_) & (dm.correct == 0))
		error_percent = 100. * errors / total
		print('Errors(%s) = %d (%.2f %%) of %d' \
			% (type_, errors, error_percent, total))
	dm = dm.correct == 1
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
		rating = ratings.ascii_word == row.word
		assert(len(rating) == 1)
		row.rating_brightness = rating.rating_brightness[0]
		row.rating_valence = rating.rating_valence[0]
		row.rating_intensity = rating.rating_intensity[0]
	return dm


def descriptives(dm):

	pm = collapse(dm.response_time_keyboard_response,
		by=[dm.type, dm.subject_nr])
	print(pm)
