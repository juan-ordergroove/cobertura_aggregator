coverage_analyzer
=================

A utility to help summarize reports from the coverage python library

A settings module is required, as you know where the locations of the coverage
reports live.

Here's an explanation of the settings configuration options:
- NAME - the application/project name you'd like to define for a config
- VENV_SOURCE - path to root level of your virtual environment
- REPORT_PATH - path to coverage report
- Targets - list of package/module names that you want summarized. They should be relative to the SOURCE path, NOT absolute paths.

Dependencies:
- coverage (in your projects virtual environment)
- python2.7
