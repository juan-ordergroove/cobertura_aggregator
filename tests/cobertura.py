"""Coverage aggregator tests"""
import os
import unittest
from coverage_agg import CoberturaAggregator

cobertura_settings = [
    {
        'TYPE': 'cobertura',
        'NAME': 'cobertura_test',
        'REPORT_PATH': os.path.join(
            os.path.dirname(__file__),
            'fixtures/cobertura.xml'
            ),
        'TARGETS': []
    }
]


class CoberturaAggregationTests(unittest.TestCase):
    """Test cases for agggreating cobertura reports"""
    pass
