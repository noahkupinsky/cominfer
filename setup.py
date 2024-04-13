from setuptools import setup, find_packages

setup(
    name='cominfer',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'argparse',
        'importlib-metadata; python_version<"3.8"',
    ],
    entry_points={
        'console_scripts': [
            'cominfer=cominfer.package_creator:main',
        ],
    },
    author='Noah Kupinsky',
    author_email='noah@kupinsky.com',
    description='A tool for synchronizing note files to GitHub repositories.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
