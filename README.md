coverage_analyzer
=================

A utility to help summarize reports from Cobertura XML files

A settings module is required, as you know where the locations of your coverage
reports live.

Here's a sample of the settings dict:
{
    '<NAME>': {
        'COBERTURA_REPORTS': ['/path/to/xml1', '/path/to/xml2']
        'TARGETS': ['target1', 'target/2']
        'REPORT_PATH': '/path/to/report'
    }
}

Here's what each means:
- NAME - the application/project name you'd like to define for a config
- COBERTURA_REPORTS - path to coverage report(s)
- TARGETS - list of folder/file names that you want summarized. They should be relative paths based on the current working directory of the test suite
- REPORT_PATH - [optional] - path to write report file to

Usage
- Define your settings
- python cobertura_agg.py

Dependencies:
- python2.7
- https://pypi.python.org/pypi/tabulate
