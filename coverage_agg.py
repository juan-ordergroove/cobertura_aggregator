"""Generic coverage report analyzer @ app level"""
import os
import subprocess
import sys
import uuid


def subprocess_cmd(command, dry_run=False):
    """Run multipe commands in subprocess module"""
    if dry_run:
        print command
        return
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    process.communicate()[0].strip()


class CoverageAggregator(object):
    """Coverage report aggregator"""

    def __init__(self, settings={}, dry_run=False, verbose=False):
        if settings:
            self._validate(settings)
        self._name = settings.get('NAME', 'Unnamed')
        self._venv_source = settings.get('VENV_SOURCE')
        self._report_path = settings.get('REPORT_PATH')
        self._targets = settings.get('TARGETS')
        self._apps = settings.get('APPS', [])
        self._dry_run = dry_run
        self._verbose = verbose
        self._tmp_coverage_report = ''
        self._report = []

    def get_report(self):
        """_report getter"""
        return self._report

    def get_report_name(self):
        """_name getter"""
        return self._name

    def set_settings(self, settings, dry_run=False, verbose=False):
        """Reset instance settings"""
        self.__init__(settings, dry_run, verbose)

    def run(self):
        """Aggregator runner"""
        self._generate_report()
        self._analyze_report()
        return self._report

    def _generate_report(self):
        """Coverage report file generator"""
        args = []

        # Change directory to report path
        args.append('cd {}'.format(self._report_path))

        # Activate virtual env
        args.append('source {}'.format(self._venv_source))

        # Write report to file
        self._tmp_coverage_report = '/tmp/{}'.format(uuid.uuid4())
        args.append('coverage report -m > {}'.format(self._tmp_coverage_report))
        subprocess_cmd(' && '.join(args), self._dry_run)

    def _validate(self, settings):
        venv_source = settings.get('VENV_SOURCE')
        assert venv_source, "VENV_SOURCE improperly configured"
        assert settings.get('TARGETS'), "TARGETS error: aggregation target required"

        bin_activate = 'bin/activate'
        trailing_slash = venv_source.endswith('/')
        if not trailing_slash:
            bin_activate = '/{}'.format(bin_activate)

        venv_source = '{}{}'.format(venv_source, bin_activate)
        assert os.path.exists(venv_source), \
            "VENV_SOURCE error: path does not exist"
        assert os.path.exists(settings.get('REPORT_PATH')), \
            "REPORT_PATH settings path does not exist"
        settings['VENV_SOURCE'] = venv_source

    def _analyze_report(self):
        """Analyze coverage report and summarize for given targets"""
        target_stats = {}
        for target in self._targets:
            target_stats[target] = {
                'lines': 0,
                'lines_missed': 0,
                'cond': 0,
                'cond_missed': 0,
                'total': 0,
                'total_missed': 0,
                'coverage': '0',
            }

        with open(self._tmp_coverage_report) as coverage_file:
            for line in coverage_file:
                for target in target_stats:
                    if "NoSource:" in line:
                        continue

                    if line.find(target) == 0:
                        if self._verbose:
                            print line.strip()
                        stats = line.split()
                        curr_stats = self._analyze_line(
                            stats,
                            target_stats[target]
                            )
                        target_stats[target] = curr_stats

        total = 0
        total_missed = 0

        # Use the array self._targets to ensure order...
        for target in self._targets:
            self._report.append('{}: {}%'.format(
                target,
                target_stats[target]['coverage'])
            )
            total += target_stats[target]['total']
            total_missed += target_stats[target]['total_missed']

        coverage = 0
        if total_missed:
            percent_total = float(total_missed) / float(total) * 100
            coverage = 100 - percent_total
        else:
            coverage = float(100)
        self._report.append('OVERALL {} COVERAGE: {:.2f}%'.format(
            self.get_report_name().upper(),
            coverage
            )
        )

    @staticmethod
    def _analyze_line(line_stats, stats):
        """Coverage line aggregator"""
        assert len(line_stats) >= 5, \
            "Please ensure this coverage report was \
            generated with branch analysis enabled: \
            coverage --branch..."

        stats['lines'] += int(line_stats[1])
        stats['lines_missed'] += int(line_stats[2])
        stats['cond'] += int(line_stats[3])
        stats['cond_missed'] += int(line_stats[4])
        stats['total'] = stats['lines'] + stats['cond']
        stats['total_missed'] = stats['lines_missed'] + stats['cond_missed']
        if stats['total']:
            percent_total = float(stats['total_missed']) / float(stats['total'])
            stats['coverage'] = 100 - (percent_total * 100)
        else:
            stats['coverage'] = float(100)
        stats['coverage'] = '%.2f' % (stats['coverage'])
        return stats

if __name__ == '__main__':
    try:
        from settings import SETTINGS
    except ImportError as exc:
        raise "Settings module error: {}".format(exc)

    # Convert to use python argparse built in
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv
    coverage_aggregator = CoverageAggregator()
    reports = {}
    for settings in SETTINGS:
        coverage_aggregator.set_settings(settings, dry_run, verbose)
        coverage_aggregator.run()
        reports[coverage_aggregator.get_report_name()] = coverage_aggregator.get_report()

    for name, report in reports.iteritems():
        print name
        for row in report:
            print row
        print ''
