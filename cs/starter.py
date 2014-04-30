from cs.gitAdapter import GitAdapter
import cs.debug as debug

class Starter(object):
    changed_files = {}
    results = {}
    scores = {}

    def __init__(self, branch, default_test_path):
        self.plugins = []
        self.repository_path = '.'
        self.control_version = GitAdapter(branch, self.repository_path)
        self.changed_files = self.control_version.get_changed_files()
        self.default_test_path = default_test_path
        
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
            status = plugin.run()
            status_name = plugin.get_status_name(status)
            self.scores[status_name] += 1
            debug.show("%s => %s" % (plugin.__class__.__name__, status_name))
        self.control_version.checkout_initial_branch()
        return self.get_status()

    def get_status(self):
        if self.scores['bad'] > 0:
            return 'bad'
        if self.scores['great'] > self.scores['acceptable']:
            return 'great'
        return 'ok'
