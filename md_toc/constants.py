#
# constants.py
#
# Copyright (C) 2017-2024 Franco Masotti (see /README.md)
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

import copy
import html
import os
import typing

# License C applies to the cmark entities part.
# See docs/copyright_license.rst
_entities5 = html.entities.html5
# remove keys without semicolons.  For some reason the list
# has duplicates of a few things, like auml, one with and one
# without a semicolon.
_ents = sorted([(k[:-1], _entities5[k].encode('utf-8'))
                for k in _entities5.keys() if k[-1] == ';'])

# Use a list instead of a class for simplicity.
# For this reason the cmark/entities.inc file is missing.
_entities: list = list()
for (ent, bs) in _ents:
    _entities.append({
        'entity': ent,
        'bytes': (' '.join(map(str, bs)) + ' 0').split(' ')
    })
    # Transform each entity into a list of integers from a list of strings.
    _entities[-1]['bytes'] = [int(n) for n in _entities[-1]['bytes']]

# Regular expressions related to scanners functions.
# See scanners.re and scanners.c files.
__cmark_spacechar = '([ \t\v\f\r\n])'
__cmark_tagname = '([A-Za-z][A-Za-z0-9-]*)'
__cmark_attributename = '([a-zA-Z_:][a-zA-Z0-9:._-]*)'
__cmark_unquotedvalue = "([^ \t\r\n\v\f\"'=<>`\x00]+)"
__cmark_singlequotedvalue = "(['][^'\x00]*['])"
__cmark_doublequotedvalue = '(["][^"\x00]*["])'
__cmark_attributevalue = '(' + __cmark_unquotedvalue + '|' + __cmark_singlequotedvalue + '|' + __cmark_doublequotedvalue + ')'
__cmark_attributevaluespec = __cmark_spacechar + '*[=]' + __cmark_spacechar + '*' + __cmark_attributevalue
__cmark_attribute = '(' + __cmark_spacechar + '+' + __cmark_attributename + __cmark_attributevaluespec + '?)'
__cmark_opentag = __cmark_tagname + __cmark_attribute + '*' + __cmark_spacechar + '*[/]?[>]'
__cmark_closetag = '[/]' + __cmark_tagname + __cmark_spacechar + '*[>]'

common_defaults: dict = {
    'toc_marker': '<!--TOC-->',
    'newline_string': os.linesep,
}

parser: dict = {
    'cmark': {
        'list': {
            'ordered': {
                'closing_markers': ['.', ')'],
                'default_marker_number': 1,
                'min_marker_number': 0,
                'max_marker_number': 999999999,
                'default_closing_marker': '.',
            },
            'unordered': {
                'bullet_markers': ['-', '+', '*'],
                'default_marker': '-',
            },
        },
        'link': {
            'max_chars_label': 999,
        },
        'header': {
            'max_space_indentation': 3,
            'max_levels': 6,
            'default_keep_levels': 6,
        },
        'code_fence': {
            'marker': {
                'backtick': '`',
                'tilde': '~',
            },
            'min_marker_characters': 3,
        },
        # Regular expressions related to entities functions.
        # See make_entities_inc.py and entities.inc files.
        're': {
            'ENTITIES': {
                'CMARK_ENTITY_MIN_LENGTH': 2,
                'CMARK_ENTITY_MAX_LENGTH': 32,
                'CMARK_NUM_ENTITIES': len(_entities),
                'entities': _entities,
            },
            # [0.30] only.
            'SPACETAB': '[\u0009\u0020]',
            # Line ending.
            'LE': '(\u000a|\u000d|\u000d\u000a)',

            # See https://spec.commonmark.org/0.28/#raw-html
            # 1. Open tag and 2. close tag.
            'DQAV': __cmark_doublequotedvalue,
            'SQAV': __cmark_singlequotedvalue,
            'UAV': __cmark_unquotedvalue,

            # 2.
            'AN': __cmark_attributename,
            'TN': __cmark_tagname,

            # 3. HTML comment.
            'COS': '<!--',
            'COT': '((?!>|->)(?:(?!--).))+(?!-).?',
            'COE': '-->',

            # 4. Processing instructions.
            'PIS': r'<\?',
            'PIB': r'(?:(?!\?>).)*',
            'PIE': r'\?>',

            # 5. Declarations.
            'DES': '<!',
            'DEN': '[A-Z]+',
            'DEB': '(?:(?!>).)+',
            'DEE': '>',

            # 6. CDATA
            # Section.
            'CDS': r'<!\[CDATA\[',
            # Body.
            'CDB': r'(?:(?!\]\]>).)+',
            # End.
            'CDE': r'\]\]>',

            # Attribute value.
            'AV': __cmark_attributevalue,

            # Attribute value specification.
            'AVS': __cmark_attributevaluespec,
        },
        '_scanners.re': {
            # FIXME
            # Some of these expressions are a duplicate of parser['cmark']['re'] dicts.
            'spacechar': __cmark_spacechar,
            'escaped_char': '([\\][!"#$%&\'()*+,./:;<=>?@[\\\\]^_`{|}~-])',
            'cdata': r'CDATA\[([^\]\x00]+|\][^\]\x00]|\]\][^>\x00])*',
            'htmltag': '(' + __cmark_opentag + '|' + __cmark_closetag + ')',
            'htmlcomment': '(--->|(-([-]?[^\x00>-])([-]?[^\x00-])*-->))',
            'declaration': '[A-Z]+' + __cmark_spacechar + '+' + '[^>\x00]*',
            'processinginstruction': '([^?>\x00]+|[?][^>\x00]|[>])+',
        },
    },
    'redcarpet': {
        'list': {
            'ordered': {
                # FIXME
                'min_marker_number': 0,
                'closing_markers': ['.'],
                'default_closing_marker': '.',
            },
            'unordered': {
                'bullet_markers': ['-', '+', '*'],
                'default_marker': '-',
            },
        },
        'header': {
            'max_space_indentation': 0,
            'max_levels': 6,
            'default_keep_levels': 6,
        },
    },
}

parser['cmark']['re'].update({
    # Attribute.
    # [0.30]
    #   An attribute consists of spaces, tabs, and up to one line ending,
    #   an attribute name, and an optional attribute value specification.
    # A newline is needed if spaces are not present in the first part.
    'AT':
    ('(' + parser['cmark']['re']['SPACETAB'] + '+' + '|' +
     parser['cmark']['re']['LE'] + '{1,1}' + ')' +
     parser['cmark']['re']['AN'] + '(' + parser['cmark']['re']['AVS'] + ')?'),
})

parser['cmark']['re'].update({
    # 1. Open tag.
    'OT':
    ('<' + parser['cmark']['re']['TN'] + '(' + parser['cmark']['re']['AT'] +
     ')*' + '(' + parser['cmark']['re']['SPACETAB'] + '*' + '|' +
     parser['cmark']['re']['LE'] + '?' + ')' + '(/)?' + '>'),
    # 2. Close tag.
    'CT': ('</' + parser['cmark']['re']['TN'] + '(' +
           parser['cmark']['re']['SPACETAB'] + '*' + '|' +
           parser['cmark']['re']['LE'] + '?' + ')' + '>'),

    # 3. HTML comment.
    'CO':
    parser['cmark']['re']['COS'] + parser['cmark']['re']['COT'] +
    parser['cmark']['re']['COE'],

    # 4. Processing instructions.
    'PI':
    parser['cmark']['re']['PIS'] + parser['cmark']['re']['PIB'] +
    parser['cmark']['re']['PIE'],

    # 5. Declarations.
    'DE':
    parser['cmark']['re']['DES'] + parser['cmark']['re']['DEN'] +
    parser['cmark']['re']['DEB'] + parser['cmark']['re']['DEE'],

    # 6. CDATA.
    'CD':
    parser['cmark']['re']['CDS'] + parser['cmark']['re']['CDB'] +
    parser['cmark']['re']['CDE'],
})

parser['github'] = copy.deepcopy(parser['cmark'])

# FIXME
# The following overrides must be removed once GFM is on par with cmark 0.30.
# FIXME
# Regular expressions.
# These refer to inline HTML.
parser['github']['re'].update({
    'UAV':
    "[^\u0020\"'=<>`]+",
    'WS':
    '(\u0020|\u0009|\u000a|\u000b|\u000c|\u000d)',
})

parser['github']['re'].update({
    'AV': ('(' + parser['github']['re']['UAV'] + '|' +
           parser['github']['re']['SQAV'] + '|' +
           parser['github']['re']['DQAV'] + ')'),
    'AVS': (parser['github']['re']['WS'] + '*' + '=' +
            parser['github']['re']['WS'] + '*' + parser['github']['re']['AV']),

    # Attribute.
    'AT': (parser['github']['re']['WS'] + '+' + parser['github']['re']['AN'] +
           '(' + parser['github']['re']['AVS'] + ')?'),

    # Remember: https://developmentality.wordpress.com/2011/09/22/python-gotcha-word-boundaries-in-regular-expressions/
    # Github Flavored Markdown Disallowed Raw HTML (specific to GFM and not to cmark')
    # See
    # https://github.github.com/gfm/#disallowed-raw-html-extension-
    # This RE are specific to GFM.
    'GDRH':
    r'''(\b[tT][iI][tT][lL][eE]\b|\b[tT][eE][xX][tT][aA][rR][eE][aA]\b|\b[sS][tT][yY][lL][eE]\b|\b[xX][mM][pP]\b|\b[iI][fF][rR][aA][mM][eE]\b|\b[nN][oO][eE][mM][bB][eE][dD]\b|\b[nN][oO][fF][rR][aA][mM][eE][sS]\b|\b[sS][cC][rR][iI][pP][tT]\b|\b[pP][lL][aA][iI][nN][tT][eE][xX][tT]\b)''',
    'DEW':
    parser['github']['re']['WS'] + '+',
})

parser['github']['re'].update({
    'TN': ('(?!' + parser['github']['re']['GDRH'] + ')' +
           parser['github']['re']['TN']),
})

parser['github']['re'].update({
    # 1. Open tag.
    'OT':
    ('<' + parser['github']['re']['TN'] + '(' + parser['github']['re']['AT'] +
     ')*' + '(' + parser['github']['re']['WS'] + ')*' + '(/)?' + '>'),
    # 2. Close tag.
    'CT': ('</' + parser['github']['re']['TN'] + parser['github']['re']['WS'] +
           '?' + '>'),
    # 5. Declarations.
    'DE': (parser['github']['re']['DES'] + parser['github']['re']['DEN'] +
           parser['github']['re']['DEW'] + parser['github']['re']['DEB'] +
           parser['github']['re']['DEE']),
})

del parser['github']['re']['SPACETAB']
del parser['github']['re']['LE']

##########################################

# Do not move these.
parser['gitlab'] = copy.deepcopy(parser['cmark'])
parser['goldmark'] = copy.deepcopy(parser['cmark'])
parser['commonmarker'] = copy.deepcopy(parser['github'])

if __name__ == '__main__':
    pass
