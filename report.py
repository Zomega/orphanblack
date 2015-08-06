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
            return cmp(b.getMaxCoveredLineNumbersCount(), a.getMaxCoveredLineNumbersCount())
        self._clones.sort(f)
