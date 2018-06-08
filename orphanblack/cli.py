#!/usr/bin/python

#    Copyright 2008 Peter Bulychev
#    Copyright 2015 Will Oursler
#
#    This file is part of Clone Digger.
#
#    Clone Digger is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Clone Digger is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Clone Digger.  If not, see <http://www.gnu.org/licenses/>.
import click
from tabulate import tabulate

import ast_suppliers
import api

import manifest
from parameters import Parameters
from report import save_report, load_report
import html_writer

# TODO: configure with flags stuff, copy to logs...
# logging.basicConfig(level=logging.DEBUG)

# TODO: Incorprate into CLI?
# TODO: Rewrite CLI as calls to API, once API exists.


@click.group()
def orphanblack_cli():
    pass


@orphanblack_cli.command()
@click.option('-l', '--language',
              type=click.Choice(['python', 'java', 'lua', 'javascript', 'js']),
              default='python',
              help="The language of the provided files.")
# These options / arguments determine which files will be scanned.
@click.argument('source_file_names',
                type=click.Path(exists=True),
                nargs=-1)
@click.option('--file-manifest',
              type=click.Path(exists=True),
              default=None,
              help="The file manifest (formatted like a PyPI MANIFEST.in)\
              describes which files should be scanned.")
def scan(language, file_manifest, source_file_names):

  # Determine the files to scan. If no files are given, use a default manifest.
  if len(source_file_names) == 0 and file_manifest is None:
    file_manifest = manifest.default_manifest(language)

  source_file_names = set(source_file_names)
  if file_manifest is not None:
    source_file_names.update(set(manifest.contents(file_manifest)))

  supplier = ast_suppliers.abstract_syntax_tree_suppliers[language]

  # TODO: Configuration files!
  # TODO: Parameter generation in API
  parameters = Parameters()
  parameters.distance_threshold = supplier.distance_threshold
  parameters.size_threshold = supplier.size_threshold

  report = api.scan(language, source_file_names, parameters)

  save_report(".orphanblack", report)


@orphanblack_cli.command()
@click.option('-v', '--verbose', is_flag=True)
def report(verbose):
  report = load_report('.orphanblack')
  print "Found", len(report.clones), "clones.\n\n"
  for clone in report.clones:
    print clone.name
    print "="*len(clone.name)
    print "Distance between two fragments =", clone.distance
    print "Clone size =", clone.size

    def rangify(lines):
      return str(min(lines)) + ' through ' + str(max(lines))

    table = [[snippet.filename, str(snippet.first_line) + ' through ' + str(snippet.last_line)] for snippet in clone.snippets]
    print tabulate(table, headers=["File", "Lines"], tablefmt="fancy_grid")
    if verbose:
      for snippet in clone.snippets:
        print ''
        title = snippet.filename + ":" + str(snippet.first_line) + "-" + str(snippet.last_line)
        print "*"+"="*len(title)+"*"
        print "|"+title+"|"
        print "*"+"="*len(title)+"*"
        print snippet.text
    print '\n\n'


@orphanblack_cli.command()
@click.option('-o', '--output',
              'output_file_name',
              type=click.Path(),
              default='output.html',
              help="An HTML report will be written to this file. \
                    Defaults to output.html")
def html(output_file_name):
  """Outputs a readable html page."""
  report = load_report('.orphanblack')
  html_writer.write(report, output_file_name)

# This portion of the CLI implements copyright and license notices in line
# with the GNU GPL3 best practices. It is not a replacement for LICENSE.txt.

copyright_message = """
orphanblack is a refactor (derivative work) of clonedigger

orphanblack   Copyright (C) 2015 Will Oursler
clonedigger   Copyright (C) 2008 Peter Bulychev

orphanblack comes with ABSOLUTELY NO WARRANTY; for details type `show warranty'.

This is free software, and you are welcome to redistribute it under certain
conditions; see LICENSE.txt for details.
"""

warranty_message = """
orphanblack is licensed under the GNU GPL 3.

As such, there is no warranty for the program, to the extent permitted by
applicable law.  Except when otherwise stated in writing the copyright
holders and/or other parties provide the program "as is" without warranty
of any kind, either expressed or implied, including, but not limited to,
the implied warranties of merchantability and fitness for a particular
purpose.  The entire risk as to the quality and performance of the program
is with you.  Should the program prove defective, you assume the cost of
all necessary servicing, repair or correction.

In no event unless required by applicable law or agreed to in writing
will any copyright holder, or any other party who modifies and/or conveys
the program as permitted above, be liable to you for damages, including any
general, special, incidental or consequential damages arising out of the
use or inability to use the program (including but not limited to loss of
data or data being rendered inaccurate or losses sustained by you or third
parties or a failure of the program to operate with any other programs),
even if such holder or other party has been advised of the possibility of
such damages.

For more details, see the full license, which should have been distributed
with this software as "LICENSE.txt".
"""


@orphanblack_cli.group()
def show():
  pass


@show.command()
def copyright():
  print copyright_message


@show.command()
def warranty():
  print warranty_message


if __name__ == '__main__':
  orphanblack_cli()
