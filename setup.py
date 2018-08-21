# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='orage',
    version='0.1.0',
    description='Scraper for the french government calendars',
    long_description=readme,
    author='Alexandre PEREZ',
    author_email='',
    url='https://github.com/AlexandrePerez/orage',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)