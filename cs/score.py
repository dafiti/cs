
from subprocess import *
from cs.quality import *
import cs.configuration
import cs.debug

class Score(Quality):
    check_tool = ''
    not_installed_message = ''
    changed_files = {}
    problems_branch = 0

    def __init__(self, control_version, changed_files):
        try:
            check_output(self.check_tool, shell=True)    
        except CalledProcessError:
            print not_installed_message
            exit(2)
        self.changed_files = changed_files
        Quality.__init__(self, control_version)

    def check(self, examinated_branch):
        result = {}
        for file_name, file_branch in self.changed_files.iteritems():
            result[file_name] = 0
            if (file_branch == examinated_branch or file_branch == 'both'):
                result[file_name] = self.get_problems(file_name)
            debug.show(" * %s has %d problems" % (file_name, result[file_name]))
        return result

    def get_problems(file_name):
        print "Implement get_problems method in child class returning int"
        exit(2)

    def diff(self, branch_problems, master_problems):
        final_score = 0
        result = {'files': {}}
        debug.show("\nProgress details:")
        for file_name, problems in branch_problems.iteritems():
            score_file = problems - master_problems[file_name]
            result['files'][file_name] = {'problems_caused': score_file}
            final_score += score_file
            debug.show(" * %s new problems: %d" % (file_name, score_file))
        result['final_score'] = final_score
        return result

    def get_status(self, problems):
        if (problems > 0):
            return -1
        if (problems < 0):
            return 1
        return 0

