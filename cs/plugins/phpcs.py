from subprocess import *
from cs.score import *
import os
import cs.debug

class Phpcs(Score):
    
    def __init__(self, control_version, changed_files):
        self.check_tool = 'phpcs --version'
        self.not_installed_message = "PHP_CodeSniffer is not installed. To install it take a look on: \nhttp://pear.php.net/package/PHP_CodeSniffer/"
        Score.__init__(self, control_version, changed_files)

    def get_name(self):
        return 'phpcs'

    def get_problems(self, file_name):
        xml_path = self.get_default_test_path('phpcs.xml')
        command = "phpcs --standard=%s %s | grep '^\ *[0-9].*' | wc -l" % (xml_path, file_name)
        return int(check_output(command, shell=True))

