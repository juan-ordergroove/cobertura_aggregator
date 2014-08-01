"""Cobertura aggregation runner"""
from cobertura_agg import CoberturaAggregator


def run():
    """runner"""
    try:
        from settings import SETTINGS
    except ImportError as exc:
        print "Settings module error: {}".format(exc)

    # Convert to use python argparse built in
    aggregator = CoberturaAggregator()
    for name, settings in SETTINGS.iteritems():
        aggregator.set_settings(name, settings)
        aggregator.generate_report()
        aggregator.print_report()

if __name__ == '__main__':
    run()
