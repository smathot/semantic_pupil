# coding=utf-8

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

import sys
import os
import eyelinkparser
from analysis import helpers, pupil, stats, parse, constants
from datamatrix import io, dispatch, _cache, plot

if not os.path.exists('ratings.csv'):
	raise Exception('Please run analyze-ratings.py first')

if '--auditory' in sys.argv:
	constants.EXP = 'auditory'
	folder = 'data-pupil-asc/auditory'
	_cache.cachefolder = '.cache-auditory'
	plot.plotfolder = 'plot-auditory'
	pupil.OUTPUT_FOLDER = 'output-auditory'
elif '--visual' in sys.argv:
	constants.EXP = 'visual'
	folder = 'data-pupil-asc/visual'
	_cache.cachefolder = '.cache-visual'
	plot.plotfolder = 'plot-visual'
	pupil.OUTPUT_FOLDER = 'output-visual'
elif '--control' in sys.argv:
	constants.EXP == 'visual'
	folder = 'data-pupil-asc/control'
	_cache.cachefolder = '.cache-control'
	plot.plotfolder = 'plot-control'
	pupil.OUTPUT_FOLDER = 'output-control'	
elif '--dutch' in sys.argv:
	constants.EXP == 'dutch'
	folder = 'data-pupil-asc/dutch'
	_cache.cachefolder = '.cache-dutch'
	plot.plotfolder = 'plot-dutch'
	pupil.OUTPUT_FOLDER = 'output-dutch'	
else:
	raise Exception('Please specify --auditory, --visual, --control, or --dutch')
_cache.cache_initialized = False

dm = dispatch.waterfall(
		(eyelinkparser.parse, 'data', {
			'folder' : folder,
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
		'subject_summary',
		'word_summary',
		'annotated_plot'
		])
