#
# setup.py
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

from setuptools import setup, find_packages

setup(
    name='md_toc',
    version='2.0.0',
    packages=find_packages(),
    license='GPL',
    description='An utility that is able to generate a table of contents for a markdown file.',
    long_description=open('README.rst').read(),
    package_data={
        '': ['*.txt', '*.rst'],
    },
    author='Franco Masotti',
    author_email='franco.masotti@student.unife.it',
    keywords='markdown toc',
    url='https://github.com/frnmst/md-toc',
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'md_toc=md_toc.__main__:main',
        ],
    },
    test_suite='tests',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
    ],
    install_requires=['fpyutils==0.0.2'],
)

