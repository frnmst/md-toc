#
# constants.py
#
# Copyright (C) 2017-2018 frnmst (Franco Masotti) <franco.masotti@live.com>
#                                            <franco.masotti@student.unife.it>
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

common_defaults = {'toc_marker': '[](TOC)'}

parser = dict()
parser['github'] = dict()
parser['github']['list'] = dict()
parser['github']['link'] = dict()
parser['redcarpet'] = dict()
parser['redcarpet']['list'] = dict()

parser['github']['link'] = {
    'max_chars_label': 999,
}

parser['github']['list']['ordered'] = {
    'closing_markers': ['.', ')'],
    'max_marker_number': 999999999,
    'default_closing_marker': '.'
}
parser['github']['list']['unordered'] = {
    'bullet_markers': ['-', '+', '*'],
    'default_marker': '-'
}

parser['github']['header'] = {
    'max_space_indentation': 3,
    'max_levels': 6,
    'default_keep_levels': 3
}

parser['cmark'] = parser['github']

parser['redcarpet']['list']['unordered'] = {
    'bullet_markers': ['-', '+', '*'],
}

parser['redcarpet']['list']['ordered'] = {
    'closing_markers': ['.'],
    'default_closing_marker': '.'
}
parser['redcarpet']['list']['unordered'] = {
    'bullet_markers': ['-', '+', '*'],
    'default_marker': '-'
}

parser['redcarpet']['header'] = {
    'max_space_indentation': 0,
    'max_levels': 6,
    'default_keep_levels': 3
}

parser['gitlab'] = parser['redcarpet']

if __name__ == '__main__':
    pass
