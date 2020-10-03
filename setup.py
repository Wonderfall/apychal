from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md")) as f:
    long_description = f.read()

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name = "apychal",
    description = "Async version of pychal (drop-in replacement to pychallonge)",
    long_description = long_description,
    long_description_content_type='text/markdown',
    author = "Wonderfall",
    author_email = "wonderfall@protonmail.com",
    url = "https://github.com/Wonderfall/apychal",
    license = "Public Domain",
    version = "1.9.8",
    keywords = ['tournaments', 'challonge'],
    packages = find_packages(),
    platforms=['any'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    install_requires = requirements
)
