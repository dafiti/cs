from cs.gitAdapter import GitAdapter
from cs.statistics import Statistics
import cs.configuration as configuration
from cs.results import Results
import json
import requests
import cs.messages
import cs.debug as debug

class Starter:
    changed_files = {}
    results = {}
    scores = {}
    master_results = {}
    result_url = {}
    master_hash = ''
    process_master = False

    def __init__(self):
        self.plugins            = []
        self.repository_path    = '.'
        self.control_version    = GitAdapter(configuration.TARGET_BRANCH, self.repository_path)
        self.master_hash        = self.control_version.get_master_hash()
        self.changed_files      = self.control_version.get_changed_files()
        self.default_test_path  = configuration.TEST_PATH

        self.results = Results(self.master_hash)
        data = self.results.get_master_results()

        if data != None:
            self.master_results = data
        else:
            self.process_master = True

    def attach(self, plugin):
        try:
            plugin.set_default_test_path(self.default_test_path)
        except ValueError as e:
            print e.message
            exit(2)
        self.plugins.append(plugin)

    def run(self):
        self.scores = {'bad': 0, 'acceptable': 0, 'great': 0}

        self.process_plugins()

        self.control_version.checkout_initial_branch()

        if self.process_master:
            self.results.save_master_results_on_cache(self.master_results)

        if configuration.SAVE_RESULT:
            self.save_result()

        return self.get_status()


    def process_plugins(self):
        for plugin in self.plugins:
            self.process_plugin(plugin)


    def process_plugin(self, plugin):
        if self.process_master:
            self.process_master_results(plugin)

        if configuration.ONLY_ON_MASTER:
            debug.show("Processing data only on master branch")
            return

        plugin.set_result(configuration.MASTER_BRANCH, self.master_results[plugin.get_name()])
        status = plugin.run()
        status_name = plugin.get_status_name(status)
        self.scores[status_name] += 1
        debug.show("%s => %s" % (plugin.__class__.__name__, status_name))


    def process_master_results(self, plugin):
        self.control_version.checkout_master()
        master_result = plugin.check(configuration.MASTER_BRANCH)
        self.master_results[plugin.get_name()] = master_result
        self.control_version.checkout_current_branch()


    def get_status(self):
        if self.scores['bad'] > 0:
            return 'bad'
        if self.scores['great'] > self.scores['acceptable']:
            return 'great'
        return 'ok'


    def save_result(self):
        filename = '%s%s.json' % (configuration.SAVE_RESULT, self.master_hash)
        debug.show("Saving the master result in: %s" % (filename))
        results.save_master_results(filename, self.master_results)


