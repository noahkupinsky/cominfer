from command_finder import CommandFinder
from command_runner import CommandRunner


class CommandInferrer:
    def __init__(self, description):
        self.description = description

    def infer(self):
        commands = CommandFinder().find_commands()
        CommandRunner(self.description, commands).run()
