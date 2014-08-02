coverage_analyzer
=================

A utility to help summarize reports from Cobertura XML files

A settings module is required, as you know where the locations of your coverage
reports live.

Here's a sample of the coverage settings dict:
```python
{
    "<NAME>" {
        "TYPE" "coverage_xml"
        "COVERAGE_XML" ["path/to/xml1" "path/to/xml2"
        "TARGETS" ["target1" "target/2"],
        "REPORT_PATH" "/path/to/report"
    }
}
```

Another sample of the cobertura settings dict:
```python
{
    "NAME" {
        "TYPE" "cobertura_json"
        "COBERTURA_URLS" "http://jenkins.domain/job/build/1/cobertura/api/json?depth=3",
        "TARGETS": <SAME_AS_ABOVE>",
        "REPORT_PATH": <SAME_AS_ABOVE>"
    }
}
```

You can mix and match as many of these objects as you like in your settings file:
```python
{
    <COVERAGE_SETTINGS_DICT_1>,
    ...
    <COVERAGE_SETTINGS_DICT_N>,
    <COBERTURA_SETTINGS_DICT_1>,
    ...
    <COBERTURA_SETTINGS_DICT_N>
}
```

Here's what each means:
- "NAME" - the application/project name you'd like to define for a config - this can be whatever you like
- TYPE - the format type aggregation against [coverage_xml OR cobertura_json]
- TARGETS - list of folder/file names that you want summarized. They should be relative paths based on the current working directory of the test suite
- REPORT_PATH - [optional] - path to write report file to
- COVERAGE_XML - path to coverage XML report(s)
- COBERTURA_URLS - URL endpoints to ping for coverage JSON stats


Usage
- Define your settings file
- python run.py --file <PATH_TO_SETTINGS_FILE>

Dependencies:
- python2.7
- https://pypi.python.org/pypi/tabulate
