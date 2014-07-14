import cs.configuration as configuration
import os
import os.path
from os.path import expanduser
import json
import requests
import cs.messages
import cs.debug as debug


class Results:

    master_hash = ''

    def __init__(self, master_hash):
        self.master_hash = master_hash

    def get_master_results(self):

        data = self.get_master_result_from_local()

        if data != None:
            return data

        debug.show("Master data from local cache not found")

        data = self.get_master_result_from_server()

        return data



    def get_master_result_from_local(self):

        debug.show("Getting the master result from cache")

        filename = self.verify_cache_file()

        if filename == False:
            return None

        raw_data = ''

        debug.show("Opening the local cache file: %s" % (filename))

        with open (filename, "r") as jsonfile:
            raw_data = jsonfile.read()

        debug.show("Reading json from local cache file")

        try:
            data = json.loads(raw_data)
        except ValueError:
            print("An error has ocurred to parse json from file: %s" % (filename))
            exit(2)

        return data



    def get_master_result_from_server(self):

        debug.show("Trying to get master data from server")

        if configuration.RESULT_URL == '':
            debug.show("Server url not informed")
            return None

        req_url = '%s%s.json' % (configuration.RESULT_URL, self.master_hash)
        
        debug.show("Getting the master result from: %s" % (req_url))
        
        req = requests.get(req_url)

        if req.status_code != 200:
            debug.show("Invalid request status code: %s" %(req.status_code))
            return None

        debug.show("Reading json from request content")

        try:
            data = json.loads(req.content)
        except ValueError:
            print("An error has ocurred to parse json from url: %s" % (req_url))
            return None

        self.save_master_results_on_cache(data)

        return data


    def save_master_results_on_cache(self, result):

        cache_dir = self.get_cache_dir(True)

        if cache_dir == False:
            return False

        debug.show("Trying to save the master data on the local cache")

        filename = '%s%s.json' % (cache_dir, self.master_hash)
        self.save_master_results(filename, result)

        return True



    def save_master_results(self, filename, result):

        debug.show("Saving master results on: %s" % (filename))
        
        with open(filename, 'wb') as outfile:
            json.dump(result, outfile)



    def verify_cache_file(self):
        cache_dir = self.get_cache_dir()

        if cache_dir == False:
            return False

        filename = "%s%s.json" % (cache_dir, self.master_hash)

        if not os.path.isfile(filename):
            debug.show("Cache file not found: %s" % (filename))
            return False

        debug.show("File found: %s" % (filename))

        return filename


    def get_cache_dir(self, create_dir = False):
        cache_dir = configuration.DEFAULT_CACHE_DIR

        debug.show("Verifying if cache path exists: %s" % (cache_dir))

        if cache_dir == '':
            debug.show("Cache dir not informed")
            return False

        if cache_dir[0] == '~':
            cache_dir = os.path.expanduser(cache_dir)

        if not os.path.isdir(cache_dir):
            debug.show("Cache path not found: %s" % (cache_dir))
            if create_dir:
                debug.show("Creating the cache dir: %s" % (cache_dir))
                os.makedirs(cache_dir)
                return cache_dir
            return False

        return cache_dir