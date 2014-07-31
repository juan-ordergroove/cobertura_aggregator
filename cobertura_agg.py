"""Cobertura XML report aggregator for a given set of TARGETS"""
import os
import xml.etree.ElementTree as ET
from tabulate import tabulate


class CoberturaAggregator(object):
    """Cobertura report aggregator"""
    NAME_KEY = 'NAME'
    REPORT_PATH_KEY = 'REPORT_PATH'
    TARGETS_KEY = 'TARGETS'

    def __init__(self, settings={}):
        if settings:
            self._validate(settings)

        self._name = settings.get(self.NAME_KEY, 'Unnamed')
        self._report_path = settings.get(self.REPORT_PATH_KEY, '')
        self._targets = settings.get(self.TARGETS_KEY, [])
        self._report = []
        self._target_stats = {}
        for target in self._targets:
            self._target_stats[target] = {
                'lines': 0,
                'lines_missed': 0,
                'cond': 0,
                'cond_missed': 0,
                'line_coverage': '0',
                'cond_coverage': '0',
            }


        if settings:
            self._xml_tree = ET.parse(self._report_path)

    @classmethod
    def _validate(cls, settings):
        """Config validator"""
        report_path = settings.get(cls.REPORT_PATH_KEY)
        assert report_path, "Please provide a REPORT_PATH configuration"
        assert os.path.exists(report_path), "REPORT_PATH does not exist"
        assert settings.get(cls.TARGETS_KEY), "Please provide TARGETS in settings"

    def set_settings(self, settings):
        """Reset instance settings"""
        self.__init__(settings)

    def print_report(self):
        """Print the report"""
        headers = ['Target', 'Line%', 'Branch%']
        print tabulate(self._report, headers)

    def generate_report(self):
        """
            for each <classes> tags
             if any TARGETS are in the <class> "filename" attribute
             for each <line> tag
              increment line counter
              if "hits" attribute > 0, increment covered counter
              if "branch" attribute == True, increment branch
               total and branch coverage total
             update coverage percentages
            iterate over stats and compute totals
        """
        root = self._xml_tree.getroot()
        for classes in root.iter('classes'):
            self._get_stats(classes)

        for target in self._targets:
            stats = self._target_stats[target]
            self._report.append([
                target,
                stats['line_coverage'],
                stats['cond_coverage']
                ]
            )

    def _get_stats(self, classes):
        """Search for target aggregations"""
        cobertura_class = classes.find('class')
        class_fn = cobertura_class.get('filename')
        for target in self._targets:
            if class_fn.find(target) == 0:
                self._get_target_stats(target, classes)

    def _get_target_stats(self, target, classes):
        """Update target aggregation"""
        lines_covered = 0
        total_lines = 0
        branches_covered = 0
        total_branches = 0

        for line in classes.iter('line'):
            total_lines += 1
            if int(line.get('hits')) > 0:
                lines_covered += 1

            if line.get('branch') == "true":
                branch_stats = line.get('condition-coverage')
                b_covered, \
                    b_total = self._parse_branch_stats(branch_stats)
                branches_covered += b_covered
                total_branches += b_total

        stats = self._target_stats[target]
        stats['lines'] += total_lines
        stats['lines_missed'] += (total_lines - lines_covered)
        if total_lines:
            perc = float(stats['lines_missed']) / float(stats['lines'])
            stats['line_coverage'] = 100 - (perc * 100)
        else:
            stats['line_coverage'] = stats['line_coverage'] or float(100)

        stats['cond'] += total_branches
        stats['cond_missed'] += (total_branches - branches_covered)
        if total_branches:
            perc = float(stats['cond_missed']) / float(stats['cond'])
            stats['cond_coverage'] = 100 - (perc * 100)
        else:
            stats['cond_coverage'] = stats['line_coverage'] or float(100)
        self._target_stats[target] = stats

    @staticmethod
    def _parse_branch_stats(s):
        """Parse branch string from XML: condition-coverage="50% (1/2)" """
        covered = 0
        total = 0
        branch_stats = s[s.find("(")+1:s.find(")")]
        covered, total = branch_stats.split('/')
        return int(covered), int(total)
