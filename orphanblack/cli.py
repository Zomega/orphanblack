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
import sys

import os
import traceback
import click
import pickle  # TODO: THIS IS A SECURITY RISK. Make JSON based version.
from tabulate import tabulate

import ast_suppliers
import clone_detection_algorithm

from parameters import Parameters
from report import Report, CloneSummary, Snippet
import html_writer

# TODO: Incorprate into CLI?
# TODO: Rewrite CLI as calls to API, once API exists.
"""To run Clone Digger type:
python clonedigger.py [OPTION]... [SOURCE FILE OR DIRECTORY]...

The typical usage is:
python clonedigger.py source_file_1 source_file_2 ...
  or
python clonedigger.py path_to_source_tree
Don't forget to remove automatically generated sources, tests and third party libraries from the source tree.

Notice:
The semantics of threshold options is discussed in the paper "Duplicate code detection using anti-unification", which can be downloaded from the site http://clonedigger.sourceforge.net . All arguments are optional. Supported options are:
"""

# TODO: Remaining stuff... Add or replace functionality with .files
# TODO: Removing prefix banning for now.
'''
  cmdline.add_option('-f', '--force',
             action='store_true', dest='force',
             help='')
  cmdline.add_option('--force-diff',
             action='store_true', dest='use_diff',
             help='force highlighting of differences based on the diff algorithm')
  cmdline.add_option('--fast',
             action='store_true', dest='clusterize_using_hash',
             help='find only clones, which differ in variable and function names and constants')
  cmdline.add_option('--ignore-dir',
             action='append', dest='ignore_dirs',
             help='exclude directories from parsing')
  cmdline.add_option('--report-unifiers',
             action='store_true', dest='report_unifiers',
             help='')
  cmdline.add_option('--func-prefixes',
             action='store',
             dest='f_prefixes',
             help='skip functions/methods with these prefixes (provide a CSV string as argument)')
  cmdline.add_option('--file-list', dest='file_list',
             help='a file that contains a list of file names that must be processed by Clone Digger')

######################

@click.option('--clusterize-using-dcup',
              is_flag=True,
              help="Mark each statement with its D-cup value instead of the most similar pattern.")
'''


@click.group()
def orphanblack_cli():
    pass


@orphanblack_cli.command()
@click.option('-l', '--language',
              type=click.Choice(['python', 'java', 'lua', 'javascript', 'js']),
              default='python',
              help="The language of the provided files.")
@click.option('--no-recursion', is_flag=True)
@click.option('--distance-threshold',
              type=int,
              default=None)  # TODO: Help
@click.option('--hashing-depth',
              type=int,
              default=None)  # TODO: Help
@click.option('--size-threshold',
              type=int,
              default=None)  # TODO: Help
@click.argument('source_file_names',
                type=click.Path(exists=True),
                nargs=-1)
def scan(language, no_recursion, distance_threshold, hashing_depth, size_threshold, source_file_names):

  supplier = ast_suppliers.abstract_syntax_tree_suppliers[language]

  parameters = Parameters()

  if distance_threshold is None:
    parameters.distance_threshold = supplier.distance_threshold
  else:
    parameters.distance_threshold = distance_threshold

  if size_threshold is None:
    parameters.size_threshold = supplier.size_threshold
  else:
    parameters.size_threshold = size_threshold

  source_files = []
  source_file_names = list(source_file_names)

  report = Report(parameters)

  ####### TODO: MAKE FILE LIST
  ####### TODO: Populate parameters
  #for option in cmdline.option_list:
  #  if option.dest == 'file_list' and options.file_list is not None:
  #    source_file_names.extend(open(options.file_list).read().split())
  #    continue
  #  elif option.dest is None:
  #    continue
  #  setattr(arguments, option.dest, getattr(options, option.dest))
  ########

  def parse_file(file_name):
    try:
      print 'Parsing ', file_name, '...',
      sys.stdout.flush()
      source_file = supplier(file_name, parameters)
      source_file.getTree().propagateCoveredLineNumbers()
      source_file.getTree().propagateHeight()
      source_files.append(source_file)
      report.addFileName(file_name)
      print 'done'
    except:
      s = 'Error: can\'t parse "%s" \n: ' % (file_name,) + traceback.format_exc()
      report.addErrorInformation(s)
      print s

  def walk(dirname):
    for dirpath, dirs, files in os.walk(file_name):
      dirs[:] = (not ignore_dirs and dirs) or [d for d in dirs if d not in options.ignore_dirs]
      # Skip all non-parseable files
      files[:] = [f for f in files
                  if os.path.splitext(f)[1][1:] == supplier.extension]
      yield (dirpath, dirs, files)

  for file_name in source_file_names:
    if os.path.isdir(file_name):
      if no_recursion:
        dirpath = file_name
        files = [os.path.join(file_name, f) for f in os.listdir(file_name)
                 if os.path.splitext(f)[1][1:] == supplier.extension]
        for f in files:
          parse_file(f)
      else:
        for dirpath, dirnames, filenames in walk(file_name):
          for f in filenames:
            parse_file(os.path.join(dirpath, f))
    else:
      parse_file(file_name)

  duplicates = clone_detection_algorithm.findDuplicateCode(source_files, report)
  n = 1
  for duplicate in duplicates:
    distance = duplicate.calcDistance()
    summary = CloneSummary(
      "Clone #"+str(n),
      [  # TODO: This is a mess! Most of this info should be assembled on the fly and in member functions.
       Snippet(
        duplicate[i].getSourceFile()._file_name,
        duplicate[i].getCoveredLineNumbers(),
        '\n'.join([line for line in duplicate[i].getSourceLines()])
        ) for i in [0, 1]], distance)
    report.addClone(summary)
    n += 1
  report.sortByCloneSize()

  with open(".orphanblack", "wb") as f:
    pickle.dump(report, f)


@orphanblack_cli.command()
@click.option('-v', '--verbose', is_flag=True)
def report(verbose):
  with open(".orphanblack", "r") as f:
    report = pickle.load(f)
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
  with open(".orphanblack", "r") as f:
    report = pickle.load(f)
  html_writer.write(report, output_file_name)

# This portion of the CLI implements copyright and liscense notices in line
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
