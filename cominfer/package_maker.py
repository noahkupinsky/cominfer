import os
import subprocess
import shutil
from cominfer.command_inferrer import CommandInferrer
import re

def main():
    description = 'Command line tool for creating boilerplate cominfer packages.'
    directory = os.path.dirname(os.path.realpath(__file__))
    CommandInferrer(description, directory).infer()
    
def package(path, with_repo=False, install=False):
    PackageMaker(path, with_repo, install).make_package()


class PackageMaker:
    def __init__(self, path, with_repo, install):
        self.path = path
        self.name = os.path.basename(path)
        self.with_repo = with_repo
        self.install = install
        self._ensure_path_does_not_exist()

    def _ensure_path_does_not_exist(self):
        if os.path.exists(self.path):
            raise FileExistsError(f'Path {self.path} already exists.')
        
    def _is_valid_package_name(self):
        return re.match(r'^[a-zA-Z0-9_-]+$', self.name)

    def make_package(self):
        self._make_root()
        self._make_interior_package_contents()
        self._make_initial_commit()
        if self.install:
            self._install_package_locally()

    def _make_root(self):
        os.makedirs(self.path)
        if self.with_repo:
            self._make_repo()
        self._make_file(
            os.path.join(self.path, 'setup.py'),
            self._get_setup_content()
        )

    def _make_interior_package_contents(self):
        os.makedirs(os.path.join(self.path, self.name))
        self._make_file(
            self._interior_package_path('__init__.py'),
            '',
        )
        self._make_file(
            self._interior_package_path('command.py'), 
            self._get_command_content()
        )
        self._make_file(
            self._interior_package_path('example.py'),
            self._get_example_content()
        )

    def _make_initial_commit(self):
        os.chdir(self.path)
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', 'Initial commit'])

    def _make_file(self, path, content):
        with open(path, 'w') as file:
            file.write(content)

    def _interior_package_path(self, filename):
        return os.path.join(self.path, self.name, filename)

    def _make_repo(self):
        subprocess.run(['git', 'init', self.path])
        current_dir = os.path.dirname(os.path.realpath(__file__))
        gitignore_template_path = os.path.join(current_dir, '.gitignore_template')
        shutil.copy(gitignore_template_path, os.path.join(self.path, '.gitignore'))
        with open(os.path.join(self.path, 'README.md'), 'w') as readme:
            readme.write(f'# {self.name}\n\nDescription goes here.')

    def _install_package_locally(self):
        os.chdir(self.path)
        subprocess.run(['pip', 'install', '-e', self.path])
    
    def _get_setup_content(self):
        return f"""from setuptools import setup, find_packages

setup(
    name='{self.name}',
    version='0.1',
    packages=find_packages(),
    install_requires=['cominfer'],
    entry_points={{
        'console_scripts': [
            '{self.name}={self.name}.command:main',
        ],
    }},
)
"""

    def _get_command_content(self):
        return """import os
from cominfer.command_inferrer import CommandInferrer

def main():
    description = 'Command line tool description'
    directory = os.path.dirname(os.path.realpath(__file__))
    CommandInferrer(description, directory).infer()
"""

    def _get_example_content(self):
        return """
def example():
    print('Hello, world!')      
"""