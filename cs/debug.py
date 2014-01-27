import configuration

def show(message):
    if configuration.SHOW_DEBUG:
        print message
