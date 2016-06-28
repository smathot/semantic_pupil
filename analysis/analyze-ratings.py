#!/usr/bin/env python3
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

import os
from datamatrix import io, DataMatrix, FloatColumn, plot
import numpy as np

# First merge all ratings into a single DataMatrix
dm = None
for path in os.listdir('data-ratings'):
	if not path.endswith('.csv'):
		continue
	print('Reading %s' % path)
	if dm is None:
		dm = io.readtxt('data-ratings/%s' % path)
	else:
		dm <<= io.readtxt('data-ratings/%s' % path)

# This word was misspelled
dm = dm.word != 'térébrant'
# There are 30 participants who provided 2 ratings for 122 words
assert(len(dm) == 30*2*102)

rm = DataMatrix(length=101)
rm.word = ''
rm._type = ''
rm.rating_brightness = FloatColumn
rm.rating_valence = FloatColumn
rm.rating_intensity = FloatColumn
for row, word in zip(rm, dm.word.unique):
	dm_ = dm.word == word
	dme = dm_.rating_type == 'emotion'
	dmb = dm_.rating_type == 'brightness'
	# Pénombre was accidentally rated twice.
	assert(len(dmb)==30 or word == 'pénombre')
	assert(len(dme)==30 or word == 'pénombre')
	row.word = word
	row._type = dme.type[0]
	row.rating_brightness = dmb.rating.mean
	row.rating_valence = dme.rating.mean
	# The intensity is just the deviation from the middle score (2). In the
	# initial analysis, the deviation from the mean valence was taken. But
	# taking the per-trial deviation from the middle score, and then averaging
	# that seems to make more sense.
	row.rating_intensity = np.abs(dme.rating-2).mean()
io.writetxt(rm, 'ratings.csv')

# Determine the correlations
print(plot.regress(rm.rating_brightness, rm.rating_valence))
plot.save('regress.brightness.valence')
print(plot.regress(rm.rating_brightness, rm.rating_intensity))
plot.save('regress.brightness.intensity')
