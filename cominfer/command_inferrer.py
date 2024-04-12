from cominfer.command_finder import CommandFinder
from cominfer.command_runner import CommandRunner


class CommandInferrer:
    def __init__(self, description, directory):
        self.description = description
        self.directory = directory

    def infer(self):
        commands = CommandFinder(self.directory).find_commands()
        CommandRunner(self.description, commands).run()
