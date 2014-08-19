cobertura_aggregator
=================

A utility to help summarize reports from Jenkins Cobertura REST API calls or Cobertura XML files

#### Install
- pip install cobertura-aggregator
- Define your config file
- cobertura_agg --config /path/to/config_file.py

Here's a sample of the aggregator config dict:
```python
SETTINGS = {
    "NAME_1": {
        "TYPE": "jenkins_api",
        "USERNAME": "username",
        "API_TOKEN": "api_token",
        "DOMAIN": "http://jenkins.domain.com",
        "JOBS": [
            "job_1",
            "job_2"
        ],
        "TARGETS": [
            "target1",
            "target2"
        ]
    },
    "NAME_2": {
        "TYPE": "xml",
        "XML_FILES": [
            "/path/to/xml_1",
            "/path/to/xml_2"
        ],
        "TARGETS": [
            "target_1",
            "target_2"
        ],
        "REPORT_PATH": "/path/to/report"
    }
}
```

You can mix and match as many of these objects as you like in your settings file:
```python
{
    <API_CONFIG_1>,
    ...
    <API_CONFIG_N>,
    <XML_CONFIG_1>,
    ...
    <XML_CONFIG_N>
}
```

#### SETTINGS dictionary parameters
- "NAME" - the application/project name you'd like to define for a config - this can be whatever you like
- TYPE - [__*jenkins_api*__ OR __*xml*__] the format type to aggregate
- TARGETS - list of folder/file names that you want summarized. They should be relative paths based on the current working directory of the test suite
- REPORT_PATH - [optional] - path to write report file to

For __*xml*__ TYPE you need to define:
- XML_FILES - list of paths to Cobertura XML reports

For __*jenkins_api*__ TYPE you need to define:
- USERNAME - your Jenkins username
- API_TOKEN - the API token/key Jenkins generates for your user
- DOMAIN - where is the location of the Jenkins' jobs and builds
- JOBS - list of jobs to include in your aggregation

#### Sample output
```
---------
NAME REPORT
---------

Target     Line%    Branch%
---------  -------  ---------
target1    68.66%   47.42%
target2    29.71%   27.00%
```

#### External Packages
- https://pypi.python.org/pypi/tabulate
- https://pypi.python.org/pypi/cli_tools/0.2.4

License
=======
The MIT License (MIT)

Copyright (c) 2014 Juan Gutierrez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
