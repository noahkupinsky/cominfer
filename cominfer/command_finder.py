import inspect
import os
import importlib.util


class CommandFinder:
    def __init__(self):
        self.dir = os.path.dirname(os.path.realpath(__file__))

    def find_commands(self):
        return [
            command for module in self._find_modules()
            for name, command in self._find_public_functions(module).items()
            if name != 'main'
        ]

    def _find_public_functions(self, module):
        return {
            name: function
            for name, function in inspect.getmembers(module, inspect.isfunction)
            if not name.startswith('_')
        }
    
    def _find_modules(self):
        return [
            self._get_module_from_file(file_name)
            for file_name in os.listdir(self.dir)
            if file_name.endswith('.py')
        ]

    def _get_module_from_file(self, file_name):
        spec = self._get_module_spec_from_file(file_name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    def _get_module_spec_from_file(self, file_name):
        module_name = file_name.replace('.py', '')
        file_path = os.path.join(self.dir, file_name)
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        return spec