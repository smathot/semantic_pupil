#!/usr/bin/env python3

"""
This file is part of P0005.1.

P0005.1 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
(at your option) any later version.

P0005.1 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with P0005.1.  If not, see <http://www.gnu.org/licenses/>.
"""

import eyelinkparser
from analysis import helpers, pupil, stats, parse
from datamatrix import io, dispatch

dm = dispatch.waterfall(
		(eyelinkparser.parse, 'data', {
			'folder' : 'data-pupil-asc',
			'parser' : parse.CustomParser
			}),
		(helpers.filter_, 'data-filtered', {}),
		(pupil.preprocess, 'data-preprocessed', {}),
	)
dispatch.dispatch(dm,
	modules=[
		helpers,
		pupil,
		stats
		],
	full=[
		'brightness_plot',
		'subject_diff_traces',
		'subject_summary',
		'word_summary',
		'annotated_plot'
		])
