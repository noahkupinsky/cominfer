import os
import subprocess
import shutil
from cominfer.command_inferrer import CommandInferrer
import re

def main():
    description = 'Command line tool for creating boilerplate cominfer packages.'
    directory = os.path.dirname(os.path.realpath(__file__))
    CommandInferrer(description, directory).infer()
    
def package(path, repo=False, install=False):
    PackageCreator(path).create_package(repo, install)


class PackageCreator:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self._validate_name()

    def _validate_name(self):
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_-]*$', self.name):
            raise ValueError('Name must only contain letters, numbers, dashes, and underscores.')

    def create_package(self, repo=False, install=False):
        self._create_root_directory()
        self._create_package_contents()
        if repo:
            self._create_git_repository()
        if install:
            self._install_package_locally()

    def _create_root_directory(self):
        if os.path.exists(self.path):
            raise FileExistsError('Path already exists.')
        os.makedirs(self.path)
        self._create_file(os.path.join(self.path, 'setup.py'), PackageCreator._get_setup_content(self.name))
        self._create_file(os.path.join(self.path, 'README.md'), f'# {self.name}\n\nYour Description Here.')

    def _create_package_contents(self):
        package_dir = os.path.join(self.path, self.name)
        os.makedirs(package_dir)
        self._create_file(os.path.join(package_dir, '__init__.py'), '')
        self._create_file(os.path.join(package_dir, 'command.py'), PackageCreator._get_command_content())
        self._create_file(os.path.join(package_dir, 'example.py'), PackageCreator._get_example_content())

    def _create_file(self, path, content):
        with open(path, 'w') as file:
            file.write(content)

    def _create_git_repository(self):
        subprocess.run(['git', 'init', self.path])
        self._create_gitignore()
        self._make_initial_commit()

    def _create_gitignore(self):
        shutil.copy(os.path.join(os.path.dirname(__file__), '.gitignore_template'),
                    os.path.join(self.path, '.gitignore'))

    def _make_initial_commit(self):
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', 'Initial commit'])

    def _install_package_locally(self):
        subprocess.run(['pip', 'install', '-e', self.path])

    @staticmethod
    def _get_setup_content(name):
        return f"""
from setuptools import setup, find_packages

setup(
    name='{name}',
    version='0.1',
    packages=find_packages(),
    install_requires=['cominfer'],
    entry_points={{
        'console_scripts': [
            '{name}={name}.command:main',
        ],
    }},
    author='Your name here',
    author_email='Your email here',
    description='Your description here.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
"""

    @staticmethod
    def _get_command_content():
        return """
import os
from cominfer.command_inferrer import CommandInferrer

def main():
    description = 'Command line tool description'
    directory = os.path.dirname(os.path.realpath(__file__))
    CommandInferrer(description, directory).infer()
"""

    @staticmethod
    def _get_example_content():
        return """
def example():
    print('Hello, world!')
"""
