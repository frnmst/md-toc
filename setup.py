#
# setup.py
#
# Copyright (C) 2017-2021 Franco Masotti (franco \D\o\T masotti {-A-T-} tutanota \D\o\T com)
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
r"""setup.py."""

from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='md_toc',
    version='8.1.4',
    packages=find_packages(exclude=['*tests*']),
    license='GPLv3+',
    description='A utility that is able to generate a table of contents for a markdown file.',
    long_description=readme,
    long_description_content_type='text/markdown',
    package_data={
        '': ['*.txt', '*.rst'],
    },
    author='Franco Masotti',
    author_email='franco.masotti@tutanota.com',
    keywords='markdown toc',
    url='https://blog.franco.net.eu.org/software/#md-toc',
    python_requires='>=3.5, <4',
    entry_points={
        'console_scripts': [
            'md_toc=md_toc.__main__:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'fpyutils>=2.2,<3'
    ],
)
