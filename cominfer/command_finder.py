from comutils import PythonFunctionFinder


class CommandFinder(PythonFunctionFinder):
    def find_commands(self):
        return [
            command
            for name, command in self.find_functions().items()
            if name != 'main' and not name.startswith('_')
        ]
