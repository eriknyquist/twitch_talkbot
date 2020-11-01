import unittest
import os
from setuptools import setup, find_packages
from distutils.core import Command

from twitch_talkbot import __version__

HERE = os.path.abspath(os.path.dirname(__file__))
README = os.path.join(HERE, "README.rst")

with open(README, 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as fh:
    requirements = [x.strip() for x in fh.readlines()]

setup(
    name='twitch_talkbot',
    version=__version__,
    description=('A twitch bot for streamers who can\'t / don\'t want to talk'),
    long_description=long_description,
    url='http://github.com/eriknyquist/twitch_talkbot',
    author='Erik Nyquist',
    author_email='eknyquist@gmail.com',
    license='Apache 2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False
)
