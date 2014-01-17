from subprocess import *
from cs.score import *

import cs.debug

class Phpmd(Score):

    def __init__(self, control_version, changed_files):
        self.check_tool = 'phpmd --version'
        self.not_installed_message = "PHP Mess Detector is not installed. To install it take a look on: \nhttp://pear.phpmd.org/ and http://phpmd.org/"
        Score.__init__(self, control_version, changed_files)

    def get_problems(self, file_name):
        xml_path = self.get_default_test_path('phpmd.xml')
        command = "phpmd %s text %s | grep '%s' | wc -l" % (file_name, xml_path, file_name)
        return int(check_output(command, shell=True))
