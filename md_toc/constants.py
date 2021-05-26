#
# constants.py
#
# Copyright (C) 2017-2021 frnmst (Franco Masotti) <franco.masotti@live.com>
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

common_defaults = dict()

common_defaults = {
    'toc marker': '<!--TOC-->',
    'newline string': '\n',
}

parser = dict()
parser['cmark'] = dict()
parser['cmark']['list'] = dict()
parser['cmark']['link'] = dict()
parser['cmark']['header'] = dict()
parser['cmark']['code fence'] = dict()
parser['redcarpet'] = dict()
parser['redcarpet']['list'] = dict()

# github.
parser['cmark']['link'] = {
    'max chars label': 999,
}

parser['cmark']['list']['ordered'] = {
    'closing markers': ['.', ')'],
    'default marker number': 1,
    'min marker number': 0,
    'max marker number': 999999999,
    'default closing marker': '.',
}
parser['cmark']['list']['unordered'] = {
    'bullet markers': ['-', '+', '*'],
    'default marker': '-',
}

parser['cmark']['header'] = {
    'max space indentation': 3,
    'max levels': 6,
    'default keep levels': 3,
}

parser['cmark']['code fence'] = {
    'marker': {
        'backtick': '`',
        'tilde': '~',
    },
    'min marker characters': 3,
}

# A structure containing some generic pseudo-regex expressions used in some algorithms.
parser['cmark']['pseudo-re'] = {
    # See https://www.fileformat.info/info/unicode/category/Zs/list.htm
    # for the Zs characters.
    # Unicode Whitespace Character.
    'UWC': ['\u0020', '\u00A0', '\u1680', '\u2000', '\u2001', '\u2002', '\u2003', '\u2004', '\u2005', '\u2006', '\u2007', '\u2008', '\u2009', '\u200A', '\u202F', '\u205F', '\u3000', '\u0009', '\u000D', '\u000A', '\u000D'],

    # ASCII punctuation characters.
    'APC': ['\u0021', '\u0022', '\u0023', '\u0024', '\u0025', '\u0026', '\u0027', '\u0028', '\u0029', '\u002A', '\u002B', '\u002C', '\u002D', '\u002E', '\u002F3', '\u003A', '\u003B', '\u003C', '\u003D', '\u003E', '\u003F', '\u0040', '\u005B', '\u005E', '\u005F', '\u0060', '\u007B', '\u007C', '\u007D', '\u007E'],

    # Punctuation General Unicode Categories.
    'PGUCPC': ['\u005F', '\u203F', '\u2040', '\u2054', '\uFE33', '\uFE33', '\uFE4D', '\uFE4E', '\uFE4F', '\uFF3F'],
    'PGUCPD': ['\u002D', '\u058A', '\u05BE', '\u1400', '\u1806', '\u2010', '\u2011', '\u2012', '\u2013', '\u2014', '\u2015', '\u2E17', '\u2E1A', '\u2E3A', '\u2E3B', '\u2E40', '\u301C', '\u3030', '\u30A0', '\uFE31', '\uFE32', '\uFE58', '\uFE63', '\uFF0D', '\u10EAD'],
    'PGUCPF': ['\u00BB', '\u2019', '\u201D', '\u203A', '\u2E03', '\u2E05', '\u2E0A', '\u2E0D', '\u2E1D', '\u2E21'],
    'PGUCPI': ['\u00AB', '\u2018', '\u201B', '\u201C', '\u201F', '\u2039', '\u2E02', '\u2E04', '\u2E09', '\u2E0C', '\u2E1C', '\u2E20'],
    'PGUCPO': ['\u0021', '\u0022', '\u0023', '\u0025', '\u0026', '\u0027', '\u002A', '\u002C', '\u002E', '\u002F', '\u003A', '\u003B', '\u003F', '\u0040', '\u005C', '\u00A1', '\u00A7', '\u00B6', '\u00B7', '\u00BF', '\u037E', '\u0387', '\u055A', '\u055B', '\u055C', '\u055D', '\u055E', '\u055F', '\u0589', '\u05C0', '\u05C3', '\u05C6', '\u05F3', '\u05F4', '\u0609', '\u060A', '\u060C', '\u060D', '\u061B', '\u061E', '\u061F', '\u066A', '\u066B', '\u066C', '\u066D', '\u06D4', '\u0700', '\u0701', '\u0702', '\u0703', '\u0704', '\u0705', '\u0706', '\u0707', '\u0708', '\u0709', '\u070A', '\u070B', '\u070C', '\u070D', '\u07F7', '\u07F8', '\u07F9', '\u0830', '\u0831', '\u0832', '\u0833', '\u0834', '\u0835', '\u0836', '\u0837', '\u0838', '\u0839', '\u083A', '\u083B', '\u083C', '\u083D', '\u083E', '\u085E', '\u0964', '\u0965', '\u0970', '\u09FD', '\u0A76', '\u0AF0', '\u0C77', '\u0C84', '\u0DF4', '\u0E4F', '\u0E5A', '\u0E5B', '\u0F04', '\u0F05', '\u0F06', '\u0F07', '\u0F08', '\u0F09', '\u0F0A', '\u0F0B', '\u0F0C', '\u0F0D', '\u0F0E', '\u0F0F', '\u0F10', '\u0F11', '\u0F12', '\u0F14', '\u0F85', '\u0FD0', '\u0FD1', '\u0FD2', '\u0FD3', '\u0FD4', '\u0FD9', '\u0FDA', '\u104A', '\u104B', '\u104C', '\u104D', '\u104E', '\u104F', '\u10FB', '\u1360', '\u1361', '\u1362', '\u1363', '\u1364', '\u1365', '\u1366', '\u1367', '\u1368', '\u166E', '\u16EB', '\u16EC', '\u16ED', '\u1735', '\u1736', '\u17D4', '\u17D5', '\u17D6', '\u17D8', '\u17D9', '\u17DA', '\u1800', '\u1801', '\u1802', '\u1803', '\u1804', '\u1805', '\u1807', '\u1808', '\u1809', '\u180A', '\u1944', '\u1945', '\u1A1E', '\u1A1F', '\u1AA0', '\u1AA1', '\u1AA2', '\u1AA3', '\u1AA4', '\u1AA5', '\u1AA6', '\u1AA8', '\u1AA9', '\u1AAA', '\u1AAB', '\u1AAC', '\u1AAD', '\u1B5A', '\u1B5B', '\u1B5C', '\u1B5D', '\u1B5E', '\u1B5F', '\u1B60', '\u1BFC', '\u1BFD', '\u1BFE', '\u1BFF', '\u1C3B', '\u1C3C', '\u1C3D', '\u1C3E', '\u1C3F', '\u1C7E', '\u1C7F', '\u1CC0', '\u1CC1', '\u1CC2', '\u1CC3', '\u1CC4', '\u1CC5', '\u1CC6', '\u1CC7', '\u1CD3', '\u2016', '\u2017', '\u2020', '\u2021', '\u2022', '\u2023', '\u2024', '\u2025', '\u2026', '\u2027', '\u2030', '\u2031', '\u2032', '\u2033', '\u2034', '\u2035', '\u2036', '\u2037', '\u2038', '\u203B', '\u203C', '\u203D', '\u203E', '\u2041', '\u2042', '\u2043', '\u2047', '\u2048', '\u2049', '\u204A', '\u204B', '\u204C', '\u204D', '\u204E', '\u204F', '\u2050', '\u2051', '\u2053', '\u2055', '\u2056', '\u2057', '\u2058', '\u2059', '\u205A', '\u205B', '\u205C', '\u205D', '\u205E', '\u2CF9', '\u2CFA', '\u2CFB', '\u2CFC', '\u2CFE', '\u2CFF', '\u2D70', '\u2E00', '\u2E01', '\u2E06', '\u2E07', '\u2E08', '\u2E0B', '\u2E0E', '\u2E0F', '\u2E10', '\u2E11', '\u2E12', '\u2E13', '\u2E14', '\u2E15', '\u2E16', '\u2E18', '\u2E19', '\u2E1B', '\u2E1E', '\u2E1F', '\u2E2A', '\u2E2B', '\u2E2C', '\u2E2D', '\u2E2E', '\u2E30', '\u2E31', '\u2E32', '\u2E33', '\u2E34', '\u2E35', '\u2E36', '\u2E37', '\u2E38', '\u2E39', '\u2E3C', '\u2E3D', '\u2E3E', '\u2E3F', '\u2E41', '\u2E43', '\u2E44', '\u2E45', '\u2E46', '\u2E47', '\u2E48', '\u2E49', '\u2E4A', '\u2E4B', '\u2E4C', '\u2E4D', '\u2E4E', '\u2E4F', '\u2E52', '\u3001', '\u3002', '\u3003', '\u303D', '\u30FB', '\uA4FE', '\uA4FF', '\uA60D', '\uA60E', '\uA60F', '\uA673', '\uA67E', '\uA6F2', '\uA6F3', '\uA6F4', '\uA6F5', '\uA6F6', '\uA6F7', '\uA874', '\uA875', '\uA876', '\uA877', '\uA8CE', '\uA8CF', '\uA8F8', '\uA8F9', '\uA8FA', '\uA8FC', '\uA92E', '\uA92F', '\uA95F', '\uA9C1', '\uA9C2', '\uA9C3', '\uA9C4', '\uA9C5', '\uA9C6', '\uA9C7', '\uA9C8', '\uA9C9', '\uA9CA', '\uA9CB', '\uA9CC', '\uA9CD', '\uA9DE', '\uA9DF', '\uAA5C', '\uAA5D', '\uAA5E', '\uAA5F', '\uAADE', '\uAADF', '\uAAF0', '\uAAF1', '\uABEB', '\uFE10', '\uFE11', '\uFE12', '\uFE13', '\uFE14', '\uFE15', '\uFE16', '\uFE19', '\uFE30', '\uFE45', '\uFE46', '\uFE49', '\uFE4A', '\uFE4B', '\uFE4C', '\uFE50', '\uFE51', '\uFE52', '\uFE54', '\uFE55', '\uFE56', '\uFE57', '\uFE5F', '\uFE60', '\uFE61', '\uFE68', '\uFE6A', '\uFE6B', '\uFF01', '\uFF02', '\uFF03', '\uFF05', '\uFF06', '\uFF07', '\uFF0A', '\uFF0C', '\uFF0E', '\uFF0F', '\uFF1A', '\uFF1B', '\uFF1F', '\uFF20', '\uFF3C', '\uFF61', '\uFF64', '\uFF65', '\u10100', '\u10101', '\u10102', '\u1039F', '\u103D0', '\u1056F', '\u10857', '\u1091F', '\u1093F', '\u10A50', '\u10A51', '\u10A52', '\u10A53', '\u10A54', '\u10A55', '\u10A56', '\u10A57', '\u10A58', '\u10A7F', '\u10AF0', '\u10AF1', '\u10AF2', '\u10AF3', '\u10AF4', '\u10AF5', '\u10AF6', '\u10B39', '\u10B3A', '\u10B3B', '\u10B3C', '\u10B3D', '\u10B3E', '\u10B3F', '\u10B99', '\u10B9A', '\u10B9B', '\u10B9C', '\u10F55', '\u10F56', '\u10F57', '\u10F58', '\u10F59', '\u11047', '\u11048', '\u11049', '\u1104A', '\u1104B', '\u1104C', '\u1104D', '\u110BB', '\u110BC', '\u110BE', '\u110BF', '\u110C0', '\u110C1', '\u11140', '\u11141', '\u11142', '\u11143', '\u11174', '\u11175', '\u111C5', '\u111C6', '\u111C7', '\u111C8', '\u111CD', '\u111DB', '\u111DD', '\u111DE', '\u111DF', '\u11238', '\u11239', '\u1123A', '\u1123B', '\u1123C', '\u1123D', '\u112A9', '\u1144B', '\u1144C', '\u1144D', '\u1144E', '\u1144F', '\u1145A', '\u1145B', '\u1145D', '\u114C6', '\u115C1', '\u115C2', '\u115C3', '\u115C4', '\u115C5', '\u115C6', '\u115C7', '\u115C8', '\u115C9', '\u115CA', '\u115CB', '\u115CC', '\u115CD', '\u115CE', '\u115CF', '\u115D0', '\u115D1', '\u115D2', '\u115D3', '\u115D4', '\u115D5', '\u115D6', '\u115D7', '\u11641', '\u11642', '\u11643', '\u11660', '\u11661', '\u11662', '\u11663', '\u11664', '\u11665', '\u11666', '\u11667', '\u11668', '\u11669', '\u1166A', '\u1166B', '\u1166C', '\u1173C', '\u1173D', '\u1173E', '\u1183B', '\u11944', '\u11945', '\u11946', '\u119E2', '\u11A3F', '\u11A40', '\u11A41', '\u11A42', '\u11A43', '\u11A44', '\u11A45', '\u11A46', '\u11A9A', '\u11A9B', '\u11A9C', '\u11A9E', '\u11A9F', '\u11AA0', '\u11AA1', '\u11AA2', '\u11C41', '\u11C42', '\u11C43', '\u11C44', '\u11C45', '\u11C70', '\u11C71', '\u11EF7', '\u11EF8', '\u11FFF', '\u12470', '\u12471', '\u12472', '\u12473', '\u12474', '\u16A6E', '\u16A6F', '\u16AF5', '\u16B37', '\u16B38', '\u16B39', '\u16B3A', '\u16B3B', '\u16B44', '\u16E97', '\u16E98', '\u16E99', '\u16E9A', '\u16FE2', '\u1BC9F', '\u1DA87', '\u1DA88', '\u1DA89', '\u1DA8A', '\u1DA8B', '\u1E95E', '\u1E95F'],
    'PGUCPS': ['\u0028', '\u005B', '\u007B', '\u0F3A', '\u0F3C', '\u169B', '\u201A', '\u201E', '\u2045', '\u207D', '\u208D', '\u2308', '\u230A', '\u2329', '\u2768', '\u276A', '\u276C', '\u276E', '\u2770', '\u2772', '\u2774', '\u27C5', '\u27E6', '\u27E8', '\u27EA', '\u27EC', '\u27EE', '\u2983', '\u2985', '\u2987', '\u2989', '\u298B', '\u298D', '\u298F', '\u2991', '\u2993', '\u2995', '\u2997', '\u29D8', '\u29DA', '\u29FC', '\u2E22', '\u2E24', '\u2E26', '\u2E28', '\u2E42', '\u3008', '\u300A', '\u300C', '\u300E', '\u3010', '\u3014', '\u3016', '\u3018', '\u301A', '\u301D', '\uFD3F', '\uFE17', '\uFE35', '\uFE37', '\uFE39', '\uFE3B', '\uFE3D', '\uFE3F', '\uFE41', '\uFE43', '\uFE47', '\uFE59', '\uFE5B', '\uFE5D', '\uFF08', '\uFF3B', '\uFF5B', '\uFF5F', '\uFF62'],

}
# Punctuation character.
parser['cmark']['pseudo-re']['PC'] = parser['cmark']['pseudo-re']['APC'] + parser['cmark']['pseudo-re']['PGUCPC'] + parser['cmark']['pseudo-re']['PGUCPD'] + parser['cmark']['pseudo-re']['PGUCPF'] + parser['cmark']['pseudo-re']['PGUCPI'] + parser['cmark']['pseudo-re']['PGUCPO'] + parser['cmark']['pseudo-re']['PGUCPS']

# Regular expressions.
parser['cmark']['re'] = {
    # See https://spec.commonmark.org/0.28/#raw-html
    # 1. Open tag and 2. close tag.
    'DQAV': '"[^"]*"',
    'SQAV': "'[^']*'",
    'UAV': "[^\u0020\"'=<>`]+",
    'WS': '(\u0020|\u0009|\u000a|\u000b|\u000c|\u000d)',
    'AN': r'([A-Za-z]|_|:)([A-Za-z]|[0-9]|_|\.|:|-)*',
    'TN prime': '[A-Za-z]([A-Za-z]|[0-9]|-)*',

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
    'CDS': r'<!\[CDATA\[',
    'CDB': r'(?:(?!\]\]>).)+',
    'CDE': r'\]\]>',
}
parser['cmark']['re']['AV'] = '(' + parser['cmark']['re']['UAV'] + '|' + parser['cmark']['re']['SQAV'] + '|' + parser['cmark']['re']['DQAV'] + ')'
parser['cmark']['re']['AVS'] = parser['cmark']['re']['WS'] + '*' + '=' + parser['cmark']['re']['WS'] + '*' + parser['cmark']['re']['AV']
parser['cmark']['re']['AT'] = parser['cmark']['re']['WS'] + '+' + parser['cmark']['re']['AN'] + '(' + parser['cmark']['re']['AVS'] + ')?'

# Remember: https://developmentality.wordpress.com/2011/09/22/python-gotcha-word-boundaries-in-regular-expressions/
# Github Flavored Markdown Disallowed Raw HTML
# See https://github.github.com/gfm/#disallowed-raw-html-extension-
parser['cmark']['re']['GDRH'] = r'''(\b[tT][iI][tT][lL][eE]\b|\b[tT][eE][xX][tT][aA][rR][eE][aA]\b|\b[sS][tT][yY][lL][eE]\b|\b[xX][mM][pP]\b|\b[iI][fF][rR][aA][mM][eE]\b|\b[nN][oO][eE][mM][bB][eE][dD]\b|\b[nN][oO][fF][rR][aA][mM][eE][sS]\b|\b[sS][cC][rR][iI][pP][tT]\b|\b[pP][lL][aA][iI][nN][tT][eE][xX][tT]\b)'''
parser['cmark']['re']['TN'] = parser['cmark']['re']['TN prime']
parser['cmark']['re']['DEW'] = parser['cmark']['re']['WS'] + '+'

# 1. Open tag.
parser['cmark']['re']['OT'] = '<' + parser['cmark']['re']['TN'] + '(' + parser['cmark']['re']['AT'] + ')*' + '(' + parser['cmark']['re']['WS'] + ')*' + '(/)?' + '>'
# 2. Close tag.
parser['cmark']['re']['CT'] = '</' + parser['cmark']['re']['TN'] + parser['cmark']['re']['WS'] + '?' + '>'
# 3. HTML comment.
parser['cmark']['re']['CO'] = parser['cmark']['re']['COS'] + parser['cmark']['re']['COT'] + parser['cmark']['re']['COE']
# 4. Processing instructions.
parser['cmark']['re']['PI'] = parser['cmark']['re']['PIS'] + parser['cmark']['re']['PIB'] + parser['cmark']['re']['PIE']
# 5. Declarations.
parser['cmark']['re']['DE'] = parser['cmark']['re']['DES'] + parser['cmark']['re']['DEN'] + parser['cmark']['re']['DEW'] + parser['cmark']['re']['DEB'] + parser['cmark']['re']['DEE']
# 6. CDATA.
parser['cmark']['re']['CD'] = parser['cmark']['re']['CDS'] + parser['cmark']['re']['CDB'] + parser['cmark']['re']['CDE']

# Do not move these after the github override re expressions.
parser['github'] = copy.deepcopy(parser['cmark'])
parser['gitlab'] = copy.deepcopy(parser['cmark'])
parser['commonmarker'] = copy.deepcopy(parser['cmark'])
parser['goldmark'] = copy.deepcopy(parser['cmark'])

# Override for github only
parser['github']['re']['TN'] = '(?!' + parser['github']['re']['GDRH'] + ')' + parser['github']['re']['TN prime']
parser['github']['re']['OT'] = '<' + parser['github']['re']['TN'] + '(' + parser['github']['re']['AT'] + ')*' + '(' + parser['github']['re']['WS'] + ')*' + '(/)?' + '>'
parser['github']['re']['CT'] = '</' + parser['github']['re']['TN'] + parser['github']['re']['WS'] + '?' + '>'

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
