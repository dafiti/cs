
import cs.configuration
import cs.debug

class Statistics:
    problems_master = 0
    problems_branch = 0
    result = {'problems_caused':0, 'tools': {}}

    def __init__(self):
        self.MASTER = configuration.MASTER_BRANCH
        self.BRANCH = configuration.EXAMINATED_BRANCH

    def validate(self, collection):
        if (type(collection) != dict 
            or self.is_valid_branch_data(collection, self.MASTER) == False
            or self.is_valid_branch_data(collection, self.BRANCH) == False):
            message = "Collection must be dictionary with '%s' and '%s' keys as dictionary too."
            raise ValueError(message % (self.MASTER, self.BRANCH))

    def is_valid_branch_data(self, collection, branch):
        if (collection.has_key(branch) == False or type(collection[branch]) != dict):
            return False
        return True

    def process(self, collection, changed_files):
        try:
            self.validate(collection)
        except CalledProcessError as e:
            print e.message
            exit(2)

        score = 0
        for tool in collection[self.BRANCH].keys():
            self.result['tools'][tool] = {'files':{}}
            score_tool = 0
            for file_name, file_branch in changed_files.iteritems():
                score_file = collection[self.BRANCH][tool][file_name] - collection[self.MASTER][tool][file_name]
                self.result['tools'][tool]['files'][file_name] = {'problems_caused': score_file}
                score_tool += score_file
            score += score_tool
            self.result['tools'][tool]['problems_caused'] = score_tool

        self.result['problems_caused'] = score
        
    def get_status(self):
        status = "ok"
        acceptable = configuration.ACCEPTABLE_NEW_PROBLEMS
        if (self.problems_branch == acceptable or self.result['problems_caused'] < acceptable):
            status = "great"
        if (self.result['problems_caused'] > acceptable):
            status = "bad"
        return status

