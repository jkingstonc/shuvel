

# Class to help with sending to std out

from colorama import init, Fore, Back, Style

init()

class Log:

    # E.g. status of file:
    def status_message(message):
        print(Fore.WHITE+message)

    # E.g. new file added
    def status_confirmed(message):
        print(Fore.GREEN+message)

    # E.g. Not in .shuv repo
    def status_warning(message):
        print(Fore.ORANGE+message)

    # E.g. file doesn't exist!
    def status_error(message):
        print(Fore.RED+message)