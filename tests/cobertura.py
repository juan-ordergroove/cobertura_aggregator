"""Coverage aggregator tests"""
import os
import unittest
from coverage_agg import CoberturaAggregator

COBERTURA_SETTINGS = [
    {
        'TYPE': 'cobertura',
        'NAME': 'cobertura_test',
        'REPORT_PATH': os.path.join(
            os.path.dirname(__file__),
            'fixtures/cobertura.xml'
            ),
        'TARGETS': [
            'mytests',
            'widget_core/v3/core-model.js',
            'widget_core/common/getElementsByRegex.js'
            ]
    }
]


class CoberturaAggregationTests(unittest.TestCase):
    """Test cases for agggreating cobertura reports"""
    def setUp(self):
        self.aggregator = CoberturaAggregator(COBERTURA_SETTINGS)

    def x(self):
        self.aggregator.generate_report()
