from cs.quality import *
from subprocess import *
import os
import string
import re
import cs.debug

class Phpunitcoverage(Quality):

    def __init__(self, control_version):
        try:            
            check_output('phpunit --version', shell=True)    
        except CalledProcessError:
            print "PHPUnit is not installed. To install it take a look on: "
            print "http://phpunit.de/manual/3.7/pt_br/installation.html"
            exit(2)
        Quality.__init__(self, control_version)

    def check(self, examinated_branch):
        result = {}
        result = self.get_problems()
        return result

    def get_problems(self):

        test_path = self.get_default_test_path()
        app_path = os.getcwd()

        os.chdir(test_path)

        command = "phpunit --coverage-text | grep --after-context=3 '^\ Summary:'"
        coverage_result = check_output(command, shell=True)
        os.chdir(app_path)
        return self.parse_summary(coverage_result)

    def parse_summary(self, coverage_result):
        summary = {}
        regex = re.compile("((Classes|Methods|Lines):)\ +(\d{2,3}\.\d{1,2})%", re.UNICODE)
        for line in coverage_result.split('\n'):
            matchObj = re.match( r'.*(Classes|Methods|Lines): +(\d{1,3}\.\d{1,2}).*', line, re.M|re.I)
            if matchObj:
                summary[matchObj.group(1)] = float(matchObj.group(2))
                debug.show(" * %s has coverage of %s" % (matchObj.group(1), matchObj.group(2)))
        return summary

    def diff(self, branch_coverage, master_coverage):
        sum_coverage = 0
        items = 0
        result = {}
        debug.show("\nProgress details:")
        for attribute, percentual in branch_coverage.iteritems():
            result[attribute] = percentual - master_coverage[attribute]
            sum_coverage += result[attribute]
            items += 1
            debug.show(" * %s coverage progress was %s" % (attribute, str(result[attribute])))
        result['final_score'] = round(sum_coverage / items, 2)
        return result

    def get_status(self, coverage_progress):
        if (coverage_progress < 0):
            return -1
        if (coverage_progress > 0):
            return 1
        return 0