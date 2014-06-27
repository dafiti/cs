
from sys import argv, exit
from git import *

import cs.configuration as configuration
import cs.debug as debug

class GitAdapter:
    base_branch = 'master'
    initial_branch = ''
    current_branch = ''

    def __init__(self, branch, repository_path):
        self.repository_path = repository_path
        self.repo = Repo(repository_path)
        self.initial_branch = self.repo.head.reference.name
        try:
            self.set_current_branch(branch)
        except ValueError as e:
            print e.message
            exit(2)

    def checkout(self, branch):
        self.repo.git.checkout(branch)
        debug.show("\nSwitched to branch '%s'" % (branch))

    def checkout_master(self):
        if (self.repo.head.reference.name == self.base_branch):
            debug.show("\nThe branch already is master")
            return 
        self.repo.heads.master.checkout()
        debug.show("\nSwitched to branch '%s'" % (self.base_branch))

    def checkout_current_branch(self):
        self.checkout(self.current_branch)

    def checkout_initial_branch(self):
        self.checkout(self.initial_branch)

    def set_current_branch(self, branch):
        current_branch = self.initial_branch
        if (branch != ''):
            current_branch = branch

        self.current_branch = current_branch

    def get_changed_files(self):
        files = {}
        debug.show("\nChecking changed files")
        self.checkout_master()
        try:
            changes = self.repo.index.diff(self.current_branch)
        except BadObject:
            self.checkout_initial_branch()
            print 'An error has occurred when tried to diff the branches. Are you sure that the branch exists?'
            exit(1)

        for obj in changes:
            files[self.get_file_name(obj)] = self.get_file_branch(obj)
        return files

    def get_file_name(self, obj):
        if (obj.a_blob is not None):
            return obj.a_blob.path
        elif (obj.b_blob is not None):
            return obj.b_blob.path
        return None

    def get_file_branch(self, obj):
        action = 'none'
        if (obj.a_blob is not None and obj.b_blob is not None):
            action = 'both'
        elif (obj.a_blob is not None):
            action = configuration.EXAMINATED_BRANCH
        elif (obj.b_blob is not None):
            action = configuration.MASTER_BRANCH
        return action

    def get_master_hash(self):
        return self.repo.heads.master.commit