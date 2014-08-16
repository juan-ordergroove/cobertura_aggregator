cobertura_aggregator
=================

A utility to help summarize reports from Jenkins Cobertura REST API calls or Cobertura XML files

A config file is required, as you know where the locations of your Cobertura reports live.

Here's a sample of the aggregator settings dict:
```python
{
    "NAME_1": {
        "TYPE": "cobertura_api",
        "USERNAME": "username",
        "API_TOKEN": "api_token",
        "DOMAIN": "http://jenkins.domain.com",
        "BUILDS": [
            "build1",
            "build2"
        ],
        "TARGETS": [
            "target1",
            "target2"
        ]
    },
    "NAME_2": {
        "TYPE": "cobertura_xml",
        "REPORTS": [
            "path/to/xml1",
            "path/to/xml2"
        ],
        "TARGETS": [
            "target1",
            "target_2"
        ],
        "REPORT_PATH": "/path/to/report"
    }
}
```

You can mix and match as many of these objects as you like in your settings file:
```python
{
    <API_SETTINGS_DICT_1>,
    ...
    <API_SETTINGS_DICT_N>,
    <XML_SETTINGS_DICT_1>,
    ...
    <XML_SETTINGS_DICT_N>
}
```

Common settings:
- "NAME" - the application/project name you'd like to define for a config - this can be whatever you like
- TYPE - the format type aggregation against [cobertura_xml OR cobertura_api]
- TARGETS - list of folder/file names that you want summarized. They should be relative paths based on the current working directory of the test suite
- REPORT_PATH - [optional] - path to write report file to

For *cobertura_xml* TYPE you need to define:
- REPORTS - list of paths to Cobertura XML reports

For *cobertura_api* TYPE you need to define:
- USERNAME - your Jenkins username
- API_TOKEN - the API token/key Jenkins generates for your user
- DOMAIN - where is the location of the Jenkins' builds
- BUILDS - list of builds to aggregate

Usage
- Define your config file
- python run.py --file /path/to/config_file

Dependencies:
- python2.7
- https://pypi.python.org/pypi/tabulate
