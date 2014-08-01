"""Coverage aggregator tests"""
import os
import unittest
from cobertura_agg import CoberturaAggregator

COBERTURA_SETTINGS = {
    'COBERTURA_REPORT': [os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'fixtures/cobertura_sample.xml'
        )],
    'TARGETS': [
        'mytests',
        'widget_core/v3/core-model.js',
        'widget_core/common/getElementsByRegex.js'
    ]
}


class CoberturaAggregationTests(unittest.TestCase):
    """Test cases for agggreating cobertura reports"""
    def setUp(self):
        self.test_name = 'tests'
        self.aggregator = CoberturaAggregator(self.test_name, COBERTURA_SETTINGS)

    def test_report_generator(self):
        """Test generating a report"""
        self.aggregator.generate_report()
        expected_result = [
            ['mytests', '73.33%', '48.65%'],
            ['widget_core/v3/core-model.js', '84.44%', '77.01%'],
            ['widget_core/common/getElementsByRegex.js', '100.00%', '100.00%']
        ]
        self.assertEqual(self.aggregator._report, expected_result)

    def test_print_report(self):
        """Test report generation"""
        settings = COBERTURA_SETTINGS
        settings[self.aggregator.REPORT_PATH_KEY] = '/tmp/'
        self.aggregator.set_settings(self.test_name, COBERTURA_SETTINGS)

        self.aggregator.generate_report()
        self.aggregator.print_report()

        report_file = self.aggregator.get_report_file()
        with open(report_file) as report:
            self.assertEqual(report.read(),
                             """Target                                    Line%    Branch%
----------------------------------------  -------  ---------
mytests                                   73.33%   48.65%
widget_core/v3/core-model.js              84.44%   77.01%
widget_core/common/getElementsByRegex.js  100.00%  100.00%"""
                             )
        os.unlink(report_file)
