from distutils.core import setup

setup(
  name='orphanblack',
  packages=['orphanblack'],
  install_requires=[
    "jinja2",
    "pickle",
    "tabulate",
    "click"],  # TODO: versioning info?
  version='0.1',
  description='Static Analysis for Software Clone Detection',
  author='Will Oursler',
  author_email='woursler@gmail.com',
  url='https://github.com/Zomega/orphanblack',
  download_url='https://github.com/Zomega/orphanblack/tarball/0.1',
  keywords=['testing', 'clone', 'static analysis', 'clonedigger', 'buildbot'],
  classifiers=[],
  entry_points={
    'console_scripts': [
      'orphanblack = orphanblack.cli:main',
    ]
  }
)
