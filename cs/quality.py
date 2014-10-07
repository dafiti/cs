from subprocess import *

import cs.configuration as configuration
import cs.debug as debug
import os

class Quality:
    result = {}
    control_version = None

    def __init__(self, control_version):
        self.control_version = control_version

    def run(self):
        debug.show("-" * 78)
        debug.show("Tool %s:" % (self.__class__.__name__))

        self.control_version.checkout_current_branch()
        self.result[configuration.EXAMINATED_BRANCH] = self.check(configuration.EXAMINATED_BRANCH)

        self.result['diff'] = self.diff(self.result[configuration.EXAMINATED_BRANCH], self.result[configuration.MASTER_BRANCH])
        return self.get_status(self.result['diff']['final_score'])

    def get_name(self):
        raise Exception("Please, implement the get_name function on the child class")
        exit(2)

    def check(self, examinated_branch):
        raise Exception("Implement check method in child class returning int")
        exit(2)

    def diff(self, branch_problems, master_problems):
        print "Implement diff method in child class returning json"
        exit(2)

    def get_status(self, final_score):
        print "Implement get_status method in child class returning -1 for bad, 0 for acceptable and 1 for great (int)"
        exit(2)

    def get_status_name(self, score):
        status = "acceptable"
        if (score > 0):
            status = "great"
        if (score < 0):
            status = "bad"
        return status

    def set_default_test_path(self, default_test_path):
        app_path = os.getcwd()
        self.default_test_path = "%s/%s" % (app_path, default_test_path)
        if not os.path.exists(self.default_test_path):
            raise ValueError('Invalid default test path: "%s"' % (self.default_test_path))
        if not self.default_test_path[-1:] == "/":
            self.default_test_path = "%s/" % (self.default_test_path)	

    def get_default_test_path(self, sufix = ''):
        if (sufix != ''):
            return '%s%s' % (self.default_test_path, sufix)

        return self.default_test_path

    def get_result(self, branch = configuration.MASTER_BRANCH):
        if branch not in self.result:
            raise Exception("Branch not found")

        return self.result[branch]

    def set_result(self, branch, result):
        self.result[branch] = result
