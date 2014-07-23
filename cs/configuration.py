import os.path
import xml.etree.ElementTree as ET

MASTER_BRANCH           = 'master'
EXAMINATED_BRANCH       = 'branch'
SHOW_DEBUG              = False
ACCEPTABLE_NEW_PROBLEMS = 0
TEST_PATH               = 'tests'
RESULT_URL              = ''
TARGET_BRANCH           = 'master'
SAVE_RESULT             = False
DEFAULT_CACHE_DIR       = '~/.codesheriff/'
ONLY_ON_MASTER          = False
CONFIG_FILE             = 'build.xml'


def setConfig(args):
    global MASTER_BRANCH
    global TARGET_BRANCH
    global RESULT_URL
    global SHOW_DEBUG
    global TEST_PATH
    global SAVE_RESULT
    global DEFAULT_CACHE_DIR
    global ONLY_ON_MASTER

    if args.result != None:
        RESULT_URL = args.result

    if os.path.isfile(CONFIG_FILE):
        tree = ET.parse(CONFIG_FILE)
        root = tree.getroot()
        cs_node = root.find('codesheriff')
        if cs_node != None:
            default_test_path_node = cs_node.find('test_path')
            if default_test_path_node != None:
                TEST_PATH = default_test_path_node.text

            default_result_url_node = cs_node.find('result_url')
            if default_result_url_node != None:
                RESULT_URL = default_result_url_node.text

            default_cache_dir_node = cs_node.find('cache_dir')
            if default_cache_dir_node != None:
                DEFAULT_CACHE_DIR = default_cache_dir_node.text

    TARGET_BRANCH   = args.branch
    ONLY_ON_MASTER  = args.only
    SHOW_DEBUG      = args.debug

    if (args.master != None):
        MASTER_BRANCH = args.master

    if (args.path != None):
        TEST_PATH = args.path

    if (args.save != None):
        SAVE_RESULT = args.save
