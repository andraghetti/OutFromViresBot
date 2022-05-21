"""
Install the package using `pip install .`
"""

import os

from setuptools import find_namespace_packages, setup

CONSOLE_SCRIPTS = {}

REQUIREMENTS = [
    'bs4',
    'requests',
    'coloredlogs'
]

setup(
    name='out_from_vires_bot',
    packages=find_namespace_packages(),
    version='0.0.2',
    author='Lorenzo Andraghetti',
    author_email='andraghetti.l@gmail.com',
    maintainer_email='andraghetti.l@gmail.com',
    url='https://github.com/andraghetti/OutFromViresBot',
    download_url='https://github.com/andraghetti/OutFromViresBot',
    platforms=['any'],
    python_requires='>=3.7',
    install_requires=REQUIREMENTS,
    entry_points={'console_scripts': CONSOLE_SCRIPTS},
)
