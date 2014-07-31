"""Coverage aggregator tests"""
import os
import unittest
from coverage_agg import CoberturaAggregator

COBERTURA_SETTINGS = {
    'TYPE': 'cobertura',
    'NAME': 'cobertura_test',
    'REPORT_PATH': os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'fixtures/cobertura_sample.xml'
        ),
    'TARGETS': [
        'mytests',
        'widget_core/v3/core-model.js',
        'widget_core/common/getElementsByRegex.js'
    ]
}


class CoberturaAggregationTests(unittest.TestCase):
    """Test cases for agggreating cobertura reports"""
    def setUp(self):
        self.aggregator = CoberturaAggregator(COBERTURA_SETTINGS)

    def test_report_generator(self):
        self.aggregator.generate_report()
        expected_result = [
            'Target\t\tLine%\t\tBranch%',
            'mytests:\t\t73.33%\t\t48.65%',
            'widget_core/v3/core-model.js:\t\t84.44%\t\t77.01%',
            'widget_core/common/getElementsByRegex.js:\t\t100.00%\t\t100.00%'
            ]
        self.assertEqual(self.aggregator._report, expected_result)
