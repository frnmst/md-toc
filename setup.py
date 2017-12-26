from setuptools import setup, find_packages

setup(
    name='md_toc',
    version='0.0.1',
    packages=find_packages(),
    license='MIT',
    long_description=open('README.rst').read(),
    package_data={
        '': ['*.txt', '*.rst'],
    },
    author='Franco Masotti',
    author_email='franco.masotti@student.unife.it',
    keywords='markdown toc',
    url='https://github.com/frnmst/md-toc',
    python_requires='>=3',
    # This part was inspired by:
    # https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-script$
    entry_points={
        'console_scripts': [
            'md_toc=md_toc.__main__:main',
        ],
    },
    test_suite='tests',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
#        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=['fpyutils', 'python-slugify'],
)

