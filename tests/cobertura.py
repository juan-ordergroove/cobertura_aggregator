"""Cobertura aggregator tests"""
import os
import unittest
from mock import patch
from base import CoberturaJSONAggregator

COBERTURA_SETTINGS = {
    CoberturaJSONAggregator.COBERTURA_URL_KEY: [
        'http://localhost/jobs/build/196/cobertura/api/json?depth=4'
    ],
    CoberturaJSONAggregator.TARGETS_KEY: [
        'club',
        'cron',
    ],
}


class CoberturaJSONAggregatorTests(unittest.TestCase):
    """Test cases for aggregating cobertura JSON via Jenkins REST API"""
    def setUp(self):
        self.test_name = 'test'
        self.aggregator = CoberturaJSONAggregator(self.test_name, COBERTURA_SETTINGS)
        fixture_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'fixtures/cobertura.json'
        )
        with open(fixture_path) as fixture_file:
            self._cobertura_json = fixture_file.read()

    @patch('base.urllib2.urlopen')
    def test_report_generator(self, mock_urlopen):
        mock_urlopen().read.return_value = self._cobertura_json
        self.aggregator.generate_report()
        expected_result = [
            ['club', '67.50%', '62.50%'],
            ['cron', '8.15%', '6.25%']
        ]
        self.assertEqual(self.aggregator._report, expected_result)
