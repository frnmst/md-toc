#
# constants.py
#
# Copyright (C) 2017-2020 frnmst (Franco Masotti) <franco.masotti@live.com>
#
# This file is part of md-toc.
#
# md-toc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# md-toc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with md-toc.  If not, see <http://www.gnu.org/licenses/>.
#
"""A file that contains all the global constants."""

common_defaults = dict()

common_defaults = {'toc marker': '<!--TOC-->'}

parser = dict()
parser['github'] = dict()
parser['github']['list'] = dict()
parser['github']['link'] = dict()
parser['github']['header'] = dict()
parser['github']['code fence'] = dict()
parser['redcarpet'] = dict()
parser['redcarpet']['list'] = dict()

# github.
parser['github']['link'] = {
    'max chars label': 999,
}

parser['github']['list']['ordered'] = {
    'closing markers': ['.', ')'],
    'default marker number': 1,
    'min marker number': 0,
    'max marker number': 999999999,
    'default closing marker': '.'
}
parser['github']['list']['unordered'] = {
    'bullet markers': ['-', '+', '*'],
    'default marker': '-'
}

parser['github']['header'] = {
    'max space indentation': 3,
    'max levels': 6,
    'default keep levels': 3
}

parser['github']['code fence'] = {
    'marker': ['`', '~'],
    'min marker characters': 3
}

parser['cmark'] = parser['github']
parser['gitlab'] = parser['github']
parser['commonmarker'] = parser['github']

# redcarpet.
parser['redcarpet']['list']['ordered'] = {
    # FIXME
    'min marker number': 0,
    'closing markers': ['.'],
    'default closing marker': '.'
}
parser['redcarpet']['list']['unordered'] = {
    'bullet markers': ['-', '+', '*'],
    'default marker': '-'
}

parser['redcarpet']['header'] = {
    'max space indentation': 0,
    'max levels': 6,
    'default keep levels': 3
}

if __name__ == '__main__':
    pass
