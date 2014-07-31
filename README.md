coverage_analyzer
=================

A utility to help summarize reports from Cobertura XML files

A settings module is required, as you know where the locations of your coverage
reports live.

Here's an explanation of the settings configuration options:
- NAME - the application/project name you'd like to define for a config
- REPORT_PATH - path to coverage report
- TARGETS - list of folder/file names that you want summarized. They should be relative paths based on the current working directory of the test suite

Usage
- Define your settings
- python cobertura_agg.py

Dependencies:
- python2.7
- https://pypi.python.org/pypi/tabulate
