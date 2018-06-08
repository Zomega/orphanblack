# TODO: This file needs to allow explicitly the following:
# Run a scan on a particular path with any file selection criteria
# Load results of any previous scan
# Automatically find candidate results to load.

# TODO: Do apis take filenames or file objects?
import logging
import traceback  # TODO: Remove this dependency.

import ast_suppliers
import clone_detection_algorithm

from report import Report, CloneSummary, Snippet


# TODO: Be able to feed in file objects instead?
def scan(language, filenames, parameters):
  supplier = ast_suppliers.abstract_syntax_tree_suppliers[language]

  source_files = []

  report = Report(parameters)

  def parse_file(filename):
    try:
      logging.info('Parsing ' + filename + '...')
      source_file = supplier(filename, parameters)
      source_file.getTree().propagateCoveredLineNumbers()
      source_file.getTree().propagateHeight()
      source_files.append(source_file)
      report.addFileName(filename)
      logging.info('done')
    except:
      logging.warn('Can\'t parse "%s" \n: ' % (filename,) + traceback.format_exc())

  for filename in filenames:
      parse_file(filename)

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

  return report
