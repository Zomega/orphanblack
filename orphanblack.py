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

import ast_suppliers
import clone_detection_algorithm

from parameters import Parameters
from report import Report
import html_writer

# TODO: Incorprate into CLI?
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
@click.option('-o', '--output',
              'output_file_name',
              type=click.Path(),
              default='output.html',
              help="An HTML report will be written to this file. \
                    Defaults to output.html")
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
def scan(language, no_recursion, output_file_name, distance_threshold, hashing_depth, size_threshold, source_file_names):

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
      if arguments.no_recursion:
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
  for duplicate in duplicates:
    report.addClone(duplicate)
  report.sortByCloneSize()
  try:
    html_writer.write(report, output_file_name)
  except:
    print "catched error, removing output file"
    if os.path.exists(output_file_name):
      os.remove(output_file_name)
    raise


@orphanblack_cli.command()
def report():
  """Reports results"""
  print "REPORT"


@orphanblack_cli.command()
def html():
  """Outputs a readable html page."""
  print "WRITE TO HTML"

if __name__ == '__main__':
  orphanblack_cli()
