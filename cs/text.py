from termcolor import colored, cprint
import cs.configuration

class Text:
    CHARS_PER_LINE = 80

    def __init__(self):
        print "\n"
        cprint("DCQC - Dafiti Control Quality Code".center(self.CHARS_PER_LINE - 2), 'white', 'on_blue')
        print "\n Analysing the code...\n"

    def result(self, status, result):
        self.details(result)
        self.progress_bar(status, result['problems_caused'])

    def details(self, result):
        for tool_name, tool_result in result['tools'].iteritems():
            title = "Summary in %s:" % (tool_name)
            cprint(title.center(CHARS_PER_LINE - 2), attrs=['reverse'])
            for file_name, file_result in tool_result['files'].iteritems():
                problems_caused = self.colored_problems(file_result['problems_caused'])
                print " * %s => %s" % (file_name, problems_caused)
            print "Problens in this tool %s:\n" % self.colored_problems(tool_result['problems_caused'])

    def colored_problems(self, problems):
        color = 'yellow'
        if (problems < 0):
            color = 'green'
        if (problems > 0):
            color = 'red'
        return colored(problems, color)


    def progress_bar(self, status, problems):
        messages = {
            'ok': {'text':'Ok :)', 'bgcolor': 'on_yellow'}, 
            'great': {'text':'Great :D', 'bgcolor': 'on_green'}, 
            'bad':  {'text':'Bad :(', 'bgcolor': 'on_red'}
            }
        text = self.progress_message(problems) + " " + messages[status]['text']
        cprint(text.center(CHARS_PER_LINE - 2), 'grey', messages[status]['bgcolor'], attrs=['dark', 'bold'])

    def progress_message(self, problems):
        if (problems == configuration.ACCEPTABLE_NEW_PROBLEMS):
            return 'The number of problems was not increased.'
        action = 'more'
        if (problems < configuration.ACCEPTABLE_NEW_PROBLEMS):
            action = 'less'
            problems *= -1
        return 'There is %d %s problem(s) on this branch than on master.' % (problems, action)