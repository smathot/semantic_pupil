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

import sys

if '--auditory' in sys.argv:
	EXP = 'auditory'
	RT = 1067
elif '--visual' in sys.argv:
	EXP = 'visual'
	RT = 790
else:
	raise Exception('Please specify --auditory or --visual')

# Epoch-of-interest for the subject and word summaries.
PEAKWIN = 1000, 2000
# Determined based on visual inspection of histograms of minimum and maximum
# pupil sizes. Trials where pupil size exceeds these values are discarded.
PUPILRANGE = .5, 2.5
# Window length for statistical analyses
WINLEN = 10
DOWNSAMPLE = 10
