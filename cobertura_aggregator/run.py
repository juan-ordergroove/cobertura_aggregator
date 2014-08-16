"""Cobertura aggregation runner"""
import imp
import argparse
from base import CoberturaXMLAggregator, CoberturaJSONAggregator


def run():
    """runner"""
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str)
    args = parser.parse_args()

    settings_mod = imp.load_source('SETTINGS', args.config)
    settings_dict = settings_mod.SETTINGS

    # Convert to use python argparse built in
    api_agg = CoberturaJSONAggregator()
    xml_agg = CoberturaXMLAggregator()
    for name, settings in settings_dict.iteritems():
        agg_type = settings.get(CoberturaXMLAggregator.TYPE_KEY)
        if agg_type == 'xml':
            aggregator = xml_agg
        elif agg_type == 'jenkins_api':
            aggregator = api_agg

        aggregator.set_settings(name, settings)
        aggregator.generate_report()
        aggregator.print_report()

if __name__ == '__main__':

    run()
