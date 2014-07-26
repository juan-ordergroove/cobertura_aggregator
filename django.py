"""Generic coverage report analyzer @ app level"""
import subprocess
import sys
import uuid

try:
    from settings import SETTINGS
except ImportError as exc:
    raise "Settings module error: does not exist or malformed: {}".format(exc)


def subprocess_cmd(command):
    """Run multipe commands in subprocess module"""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout


def build_coverage_args(settings):
    """Coverage CLI argument generator"""
    cov_args = [
        "coverage",
        "run",
        "--branch",
        "--source='.'",
        "--omit={}".format(settings['OMIT']),
        "{}/manage.py".format(settings.get('MANAGE_PATH', '')),
        "test"
        ]

    if hasattr(settings, 'APPS'):
        cov_args.append(settings.APPS)
    return cov_args


def get_default_commands(name, settings):
    """Default process commands for executing coverage commands"""
    process_list = []
    try:
        process_list += ['cd', settings['SOURCE']]
        process_list += [
            '&&',
            'source',
            '{}/bin/activate'.format(settings['VENV_SOURCE'])
            ]
    except KeyError as exc:
        raise "Missing key required: {}".format(exc)
    except OSError as exc:
        raise "Source path {} for {} misconfigured: {}".format(
            name,
            settings['SOURCE'],
            exc
            )
    return process_list


def analyze_report(name, settings, coverage_report):
    """Analyze coverage report and summarize to given folders"""
    try:
        folders = settings['FOLDERS']
    except KeyError as exc:
        raise "Missing key required: {}".format(exc)

    _folders = {}
    for folder in folders:
        _folders[folder] = {
            'stats': {
                'lines': 0,
                'lines_missed': 0,
                'cond': 0,
                'cond_missed': 0,
                'total': 0,
                'total_missed': 0,
                'coverage': '0',
            }
        }

    with open(coverage_report) as coverage_file:
        for line in coverage_file:
            for folder in _folders:
                if line.find(folder) == 0:
                    stats = line.split()
                    curr_stats = _folders[folder]['stats']
                    curr_stats['lines'] += int(stats[1])
                    curr_stats['lines_missed'] += int(stats[2])
                    curr_stats['cond'] += int(stats[3])
                    curr_stats['cond_missed'] += int(stats[4])
                    curr_stats['total'] = curr_stats['lines'] + curr_stats['cond']
                    curr_stats['total_missed'] = curr_stats['lines_missed'] + curr_stats['cond_missed']
                    if curr_stats['total']:
                        percent_total = float(curr_stats['total_missed']) / float(curr_stats['total']) * 100
                        curr_stats['coverage'] = 100 - percent_total
                    else:
                        curr_stats['coverage'] = float(100)
                    curr_stats['coverage'] = '%.2f' % (curr_stats['coverage'])
                    _folders[folder]['stats'] = curr_stats

    total = 0
    total_missed = 0
    coverage = 0
    for folder in _folders:
        print '{}: {}%'.format(folder, _folders[folder]['stats']['coverage'])
        total += _folders[folder]['stats']['total']
        total_missed += _folders[folder]['stats']['total_missed']
    if total_missed:
        percent_total = float(total_missed) / float(total) * 100
        coverage = 100 - percent_total
    else:
        coverage = float(100)
    print 'Core Coverage: %.2f%%' % coverage


def run():
    """Coverage summary runner"""
    for name, project_settings in SETTINGS.iteritems():
        # Run the tests and prep for the next report
        if "--regenerate" in sys.argv:
            process_list = get_default_commands(name, project_settings)
            coverage_args = build_coverage_args(project_settings)
            process_list += ['&&'] + coverage_args
            subprocess_cmd(' '.join(process_list))

        # Generate and read the report
        coverage_report = '/tmp/{}'.format(uuid.uuid4())
        process_list = get_default_commands(name, project_settings)
        process_list += ['&& coverage report -m > {}'.format(coverage_report)]
        subprocess_cmd(' '.join(process_list))

        analyze_report(name, project_settings, coverage_report)
        subprocess_cmd('rm -f {}'.format(coverage_report))

if __name__ == '__main__':
    run()
