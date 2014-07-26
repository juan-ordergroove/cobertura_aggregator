coverage_analyzer
=================

A utility to help summarize reports from the coverage python library

A settings module is required, as you know where the locations of the packages you'd 
like coverage summaries generated for. The code doesn't support this yet, but I'd like for 
this package to iterate over the applications you'd like summarized and a single report 
is generated. For now, running coverage against a Django project is all this currently 
supports, as it is a need of my own I'm currently trying to satisfy.

Here's an explanation of the settings configuration options:
- Name of Configuration - the application/project name you'd like to define for a config
- VENV_SOURCE - path to root level of your virtual environment
- SOURCE - coverage CLI option needed for running coverage against Django projects - use the project folder path
- MANAGE_PATH - path to Django's manage.py
- OMIT - coverage omissions
- FOLDERS - list of folder names that you want summarized. They should be relative to
the SOURCE path, NOT absolute paths.
- APPS (optional) - what apps to target running tests for. This should line up intelligently
with FOLDERS if you choose to use this parameter.

CLI options:
- --regenerate - regenerate the coverage report by running the test suite before analyzing the coverage report

Dependencies:
- Django
- coverage
