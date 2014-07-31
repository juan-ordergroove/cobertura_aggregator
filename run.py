from cobertura_agg import CoberturaAggregator

if __name__ == '__main__':
    try:
        from settings import SETTINGS
    except ImportError as exc:
        print "Settings module error: {}".format(exc)

    # Convert to use python argparse built in
    aggregator = CoberturaAggregator()
    for settings in SETTINGS:
        aggregator.set_settings(settings)
        aggregator.generate_report()
        aggregator.print_report()
