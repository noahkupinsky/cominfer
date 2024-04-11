import argparse
import inspect


class CommandRunner:
    def __init__(self, description, commands):
        self.parser = argparse.ArgumentParser(description=description)
        self.subparsers = self.parser.add_subparsers(dest='command_name')
        self.commands = {command.__name__: command for command in commands}
        [self._add_command_parser(command) for command in commands]

    def run(self):
        args = self.parser.parse_args()
        command_function = self.commands[args.command_name]
        command_args = self._get_command_args(args, command_function)
        command_function(**command_args) # call function with arguments

    def _add_command_parser(self, command):
        parameters = self._get_parameters(command)
        command_parser = self.subparsers.add_parser(command.__name__)
        for name in parameters:
            command_parser.add_argument(name)

    def _get_command_args(self, args, command):
        args_dict = vars(args)
        parameters = self._get_parameters(command)
        command_args = {name: args_dict[name] for name in parameters}
        return command_args
    
    def _get_parameters(self, function):
        return [param.name for param in inspect.signature(function).parameters.values()]
