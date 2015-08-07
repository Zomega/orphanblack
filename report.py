# TODO: report serialization without pickle because that's insecure.

import textwrap


# TODO: TEXT OF FILES!
class Snippet:
  def __init__(self, filename, lines, text):
    def deindent(string):
      if string and string[0] == '\n':
        string = string[1:]
      return textwrap.dedent(string)
    self.filename = filename
    self.lines = lines
    self.text = deindent(text)

  @property
  def first_line(self):
    return min(self.lines)

  @property
  def last_line(self):
    return max(self.lines)

  @property
  def size(self):
    return len(self.lines)


# Minimal Clone Summary for serialization.
class CloneSummary:
  def __init__(self, name, snippets, distance):
    self.name = name
    self.snippets = snippets
    self.distance = distance

  @property
  def size(self):
    return sum([snippet.size for snippet in self.snippets]) / len(self.snippets)


class Report:
  def __init__(self, parameters):
    self._parameters = parameters
    self._error_info = []
    self._clones = []
    self._file_names = []
    self._mark_to_statement_hash = None

  @property
  def parameters(self):
    return self._parameters

  @property
  def clones(self):
    return self._clones

  @property
  def filenames(self):
    return self._file_names

  def setMarkToStatementHash(self, mark_to_statement_hash):  # TODO: Figure out what this is and if it belongs
    self._mark_to_statement_hash = mark_to_statement_hash

  def addFileName(self, file_name):
    self._file_names.append(file_name)

  def addErrorInformation(self, error_info):
    self._error_info.append(error_info)

  def addClone(self, clone):
    self._clones.append(clone)

  def sortByCloneSize(self):
    def f(a, b):
      return cmp(b.size, a.size)
    self._clones.sort(f)
