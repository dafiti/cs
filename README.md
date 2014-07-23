# CodeSheriff

CodeSheriff is a code quality tool mainly developed by Dafiti Brazil for PHP
projects.

## How it works

CodeSheriff compares two git branches and gives stats about its quality
using tools like PHPMD, PHPCS and PHPUnit for code code coverage.

CodeSheriff can work with CI tools like Jenkins and validate quality of code
before it goes live or a branch is merged into master.

## I) Requirements:

python 2.6+
python-pip


And the PHP tools for each plugin:

phpcs
phpmd
phpunit


## II) Installation:

```shell
sudo apt-get install python
sudo apt-get install python-pip
git clone git@github.com:dafiti/cs.git
cd cs
sudo python setup.py install
```

Note: the code sheriff requires some python plugins as 'GitPython', 'termcolor' and 'requests', but all the plugins are installed thru the python setuptools.


### III) Usage:

```shell
cd project/
cs <MY_BRANCH>
```

## IV) Options:

We have two ways to run the cs with options:

1. script parameters:

bruno@nobru:/var/www/project# cs --help
usage: cs [-h] [-p PATH] [-r RESULT] [-s SAVE] [-m MASTER] [-d] [-o] branch

Code Sheriff

positional arguments:
  branch                The branch that have to be checked

optional arguments:
  -h, --help                    show this help message and exit
  -p PATH, --path PATH          The path of configurations and tests files
  -r RESULT, --result RESULT    The server result URL
  -s SAVE, --save SAVE          Path where to save the result locally
  -m MASTER, --master MASTER    The default master branch
  -d, --debug                   Active debug mode
  -o, --only                    Process CS only on master branch
 

2. Config file: 

The cs try to find the build.xml and parse it.

Options: test_path, result_url and cache_dir

test_path: the path where the cs have to find the configuration files for plugins and the phpunit tests

cache_dir: the default cache directory

result_url: the url for results API

Example for build.xml:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project>
    <codesheriff>
        <test_path>project/sub/path/tests/</test_path>
        <result_url>http://my_api/codesheriff/</result_url>
    </codesheriff>
</project>
```

V) How the cache works:

1) Code sheriff verify if the master result cache exists on the cache dir (default: ~/.codesheriff/<MASTER_HASH>.json)

2) If not, code sheriff verify if the result api url is setted and then, try to get the cache from the API. http://API/<MASTER_HASH>.json

3) If not, code sheriff runs first on the master (to get the results to compare) and, at the finish, creates a local cache with the results.


## Contributing

Open an issue or fork this project and open a pull request.
