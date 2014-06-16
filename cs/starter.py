from cs.gitAdapter import GitAdapter
from cs.statistics import Statistics
import cs.configuration as configuration
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

    def __init__(self, branch, default_test_path, default_result_url):
        self.plugins = []
        self.repository_path = '.'
        self.control_version = GitAdapter(branch, self.repository_path)
        self.changed_files = self.control_version.get_changed_files()
        self.default_test_path = default_test_path
        self.result_url = default_result_url
        req = requests.get(default_result_url)
        data = json.loads(req.content)

        if data != None:
            self.master_results = data

    def attach(self, plugin):
        try:
            plugin.set_default_test_path(self.default_test_path)
        except ValueError as e:
            print e.message
            exit(2)
        self.plugins.append(plugin)

    def run(self):
        self.scores = {'bad': 0, 'acceptable': 0, 'great': 0}
        for plugin in self.plugins:
            plugin.set_result(configuration.MASTER_BRANCH, self.master_results[plugin.get_name()])
            status = plugin.run()
            status_name = plugin.get_status_name(status)
            self.scores[status_name] += 1
            debug.show("%s => %s" % (plugin.__class__.__name__, status_name))
        self.control_version.checkout_initial_branch()
        self.save_result()
        return self.get_status()

    def get_status(self):
        if self.scores['bad'] > 0:
            return 'bad'
        if self.scores['great'] > self.scores['acceptable']:
            return 'great'
        return 'ok'

    def save_result(self):
        with open('codesheriff.result', 'wb') as outfile:
            json.dump(self.master_results, outfile)