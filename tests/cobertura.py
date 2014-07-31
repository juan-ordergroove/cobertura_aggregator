"""Coverage aggregator tests"""
import os
import unittest
from cobertura_agg import CoberturaAggregator

COBERTURA_SETTINGS = {
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
        """Test generating a report"""
        self.aggregator.generate_report()
        expected_result = [
            ['mytests', 73.33333333333333, 48.64864864864865],
            ['widget_core/v3/core-model.js', 84.44444444444444, 77.00892857142857],
            ['widget_core/common/getElementsByRegex.js', 100.0, 100.0]
        ]
        self.assertEqual(self.aggregator._report, expected_result)

    def test_validations(self):
        """Test empty TARGETS configuration"""
        settings = COBERTURA_SETTINGS
        del settings[self.aggregator.TARGETS_KEY]

        self.assertRaises(
            AssertionError,
            self.aggregator.set_settings,
            settings
        )

        del settings[self.aggregator.REPORT_PATH_KEY]
        self.assertRaises(
            AssertionError,
            self.aggregator.set_settings,
            settings
        )

    def test_parse_branch_stats(self):
        """Branch stat parsing unit tests"""
        test_string = ""
        self.assertRaises(
            ValueError,
            self.aggregator._parse_branch_stats,
            test_string
            )

        test_string = "(4/5)"
        covered, total = self.aggregator._parse_branch_stats(test_string)
        self.assertEqual(covered, 4)
        self.assertEqual(total, 5)

        test_string = "XY% (4/5)"
        covered, total = self.aggregator._parse_branch_stats(test_string)
        self.assertEqual(covered, 4)
        self.assertEqual(total, 5)
