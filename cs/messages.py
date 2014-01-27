from termcolor import colored, cprint
from cs import configuration

CHARS_PER_LINE = 80

def header():
    print "\n"
    cprint("CS - Code Sheriff".center(CHARS_PER_LINE - 2), 'white', 'on_blue')
    print "\n Analysing the code...\n"

def result(status, result):
    details(result)
    progress_bar(status, result['problems_caused'])

def details(result):
    for tool_name, tool_result in result['tools'].iteritems():
        title = "Summary in %s:" % (tool_name)
        cprint(title.center(CHARS_PER_LINE - 2), attrs=['reverse'])
        for file_name, file_result in tool_result['files'].iteritems():
            problems_caused = colored_problems(file_result['problems_caused'])
            print " * %s => %s" % (file_name, problems_caused)
        print "Problens in this tool %s:\n" % colored_problems(tool_result['problems_caused'])

def colored_problems(problems):
    color = 'yellow'
    if (problems < 0):
        color = 'green'
    if (problems > 0):
        color = 'red'
    return colored(problems, color)

def progress_bar(status, problems):
    messages = {
        'ok': {'text':'Ok :)', 'bgcolor': 'on_yellow'},
        'great': {'text':'Great :D', 'bgcolor': 'on_green'},
        'bad':  {'text':'Bad :(', 'bgcolor': 'on_red'}
        }
    text = progress_message(problems) + " " + messages[status]['text']
    cprint(text.center(CHARS_PER_LINE - 2), 'grey', messages[status]['bgcolor'], attrs=['dark', 'bold'])

def progress_message(problems):
    if (problems == configuration.ACCEPTABLE_NEW_PROBLEMS):
        return 'The number of problems was not increased.'
    action = 'more'
    if (problems < configuration.ACCEPTABLE_NEW_PROBLEMS):
        action = 'less'
        problems *= -1
    return 'There is %d %s problem(s) on this branch than on master.' % (problems, action)

