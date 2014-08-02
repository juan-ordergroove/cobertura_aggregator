"""Cobertura aggregation runner"""
import argparse
import simplejson
from base import CoverageXMLAggregator, CoberturaJSONAggregator


def run():
    """runner"""
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=argparse.FileType('r'))
    args = parser.parse_args()

    settings_dict = simplejson.loads(args.file.read())

    # Convert to use python argparse built in
    cobertura_agg = CoberturaJSONAggregator()
    coverage_agg = CoverageXMLAggregator()
    for name, settings in settings_dict.iteritems():
        print name, settings
        agg_type = settings.get(CoverageXMLAggregator.TYPE_KEY)
        if agg_type == 'coverage_xml':
            aggregator = coverage_agg
        elif agg_type == 'cobertura_json':
            aggregator = cobertura_agg

        aggregator.set_settings(name, settings)
        aggregator.generate_report()
        aggregator.print_report()

if __name__ == '__main__':

    run()
