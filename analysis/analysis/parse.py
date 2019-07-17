#-*- coding:utf-8 -*-

"""
This file is part of SWM_PUPIL.

SWM_PUPIL is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SWM_PUPIL is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SWM_PUPIL.  If not, see <http://www.gnu.org/licenses/>.
"""

import warnings
import gc
from eyelinkparser import EyeLinkParser, sample

class CustomParser(EyeLinkParser):

	def parse_phase(self, l):

		if self.current_phase in ('target', 'fixation') or \
			'target' in l or 'fixation' in l:
			EyeLinkParser.parse_phase(self, l)

	def end_phase(self, l):

		if len(self.ptrace) > 4000:
			warnings.warn('Very long trace, truncating to 4000: %s (%d)' \
				% (self.current_phase, len(self.ptrace)))
			self.ptrace = self.ptrace[:4000]
			self.ttrace = self.ttrace[:4000]
			self.xtrace = self.xtrace[:4000]
			self.ytrace = self.ytrace[:4000]
		EyeLinkParser.end_phase(self, l)
		gc.collect()
