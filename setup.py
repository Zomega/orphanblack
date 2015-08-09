from distutils.core import setup
import os

# This attempts to provide a safe reStructuredTxt for PyPI based on README.md
long_description = 'Static Analysis for Software Clone Detection'
if os.path.exists('README.rst'):
    long_description = open('README.rst').read()

setup(
  name='orphanblack',
  packages=['orphanblack'],
  install_requires=[
    "Jinja2",
    "tabulate",
    "click"
    ],  # TODO: versioning info?
  version='0.1.11',
  description='Static Analysis for Software Clone Detection',
  long_description=long_description,
  author='Will Oursler',
  author_email='woursler@gmail.com',
  url='https://github.com/Zomega/orphanblack',
  download_url='https://github.com/Zomega/orphanblack/tarball/0.1.11',
  keywords=['testing', 'clone', 'static analysis', 'clonedigger', 'buildbot'],
  classifiers=[],
  package_dir={'orphanblack': 'orphanblack'},
  package_data={'orphanblack': ['templates/*.html']},
  entry_points={
    'console_scripts': [
      'orphanblack = orphanblack.cli:orphanblack_cli',
    ]
  }
)
