"""Provides basic matrix manipulation functions for series use within data
transformations.

Updated Jan 2016
@author: ccurson

"""

__version__ = '4.3.0'

from functools import wraps


class MatrixSeriesManipulator():
    """Class for manipulating series and series labels.
    This class is imported into MatrixManipulator in __init__.py within the
    transformations package

    Examples:
    >>> import series as Series
    >>> import utils.matrixfuncs as matrixfuncs
    >>> m = matrixfuncs.create_test_matrix()
    >>> _my_class = Series.MatrixSeriesManipulator(m)
    >>> print _my_class.get_series_labels()  #taken from series module
    [u'myRow 0', u'myRow 1', u'myRow 2', u'myRow 3', u'myRow 4']
    >>> print _my_class.get_series_base_summary()
    myRow 0: 101, myRow 1: 6, myRow 2: 1, myRow 3: 100, myRow 4: 5
    >>> _my_class.select_series(["myRow 1"])
    >>> print _my_class.get_series_labels()
    [u'myRow 1']
    >>> m = matrixfuncs.create_test_matrix()
    >>> _my_class = Series.MatrixSeriesManipulator(m)
    >>> _my_class.del_series(["myRow 1"])
    >>> print _my_class.get_series_labels()
    [u'myRow 0', u'myRow 2', u'myRow 3', u'myRow 4']
    
    """

    import utils.logger as log
    logger = log.logger

    def __init__(self, matrix):
        self.matrix = matrix

    def wrap_matrix_logger(func):
        # Wrapper function - Wrap all functions within the class so that the
        # matrix and logger are passed to functions with given parameters.

        @wraps(func)
        def func_wrapper(self, *args):
            # Return the class with a matrix and logger parameter.
            
            matrix = self.matrix
            logger = self.logger
            return func(self, matrix, logger, args)
        return func_wrapper

    def wrap_matrix_logger_insert(func):
        # Wrapper function - Wrap all functions within the class so that the
        # matrix and logger are passed to functions with given parameters.
        # This wrapper also passes a row/col number and a label for insert_series
        # and insert_categories.

        @wraps(func)
        def func_wrapper(self, row_number=0, col_number=0, label="", *args):
            # Return the class with a matrix and logger parameter.

            matrix = self.matrix
            logger = self.logger
            return func(self, matrix, logger, row_number, col_number,
                        label, args)
        return func_wrapper

    def wrap_matrix_logger_format(func):
        # Wrapper function - Wrap all functions within the class so that the
        # matrix and logger are passed to functions with given parameters.
        # This wrapper also passes a label_format and cell_format property for
        # the formatting for labels.

        @wraps(func)
        def func_wrapper(self, label_format="{0}", cell_format="{0}", *args):
            # Return the class with a matrix and logger parameter.

            matrix = self.matrix
            logger = self.logger
            return func(self, matrix, logger, label_format, cell_format, args)
        return func_wrapper

    # Series Label functions (rows)
    @wrap_matrix_logger
    def get_series_labels(self, matrix, logger, *args):
        """Return a list containing the series (row) labels.
        
        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | labels = tr.get_series_labels()
        
        """

        return [r.Member.Label for r in matrix]

    @wrap_matrix_logger
    def get_series_group_labels(self, matrix, logger, *args):
        """Return a list containing the series (row) group labels.
        
        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | group_labels = tr.get_series_group_labels()
        
        """

        return [grp.Label for grp in matrix.SideAxis.Groups]

    @wrap_matrix_logger
    def get_series_base_summary(self, matrix, logger, *args):
        """Return the Base summary of the Row with base taken from the first
        column, using the format:
        Row Label: Base, Row Label: Base
        
        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | series_base_labels = tr.get_series_base_summary()

        """

        from labels.format_labels import FormatSettings
        settings = FormatSettings(label_format="{0.Member.Label}: " +
                                  "{0[0][0].Value}")
        return ", ".join([settings.label_format(r) for r in matrix])

    @wrap_matrix_logger
    def set_series_base_summary(self, matrix, logger, *args):
        """Set Labels to contain the series (row) labels with Base Value
        
        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | tr.set_series_base_summary()

        """

        from labels.format_labels import FormatSettings
        settings = FormatSettings(label_format="{0.SideMember.Label} " +
                                  "(n={0[0].Value})")
        for r in matrix:
            _c = r[0].Count
            r.Member.Label = settings.label_format(r[0]) if _c > 0 else ""
        matrix.DeleteColumn(0)

    @wrap_matrix_logger_format
    def set_series_formatted_labels(self, matrix, logger,
                                    label_format="{0}", cell_format={0},
                                    *args):
        """Set Labels to contain formatted labels of the users choice.

        Example:
        
        | myclass = transformations.MatrixManipulator(Matrix)
        | myclass.set_series_formatted_labels(label_format =
        |                 "{0.SideMember.Group.Label} :: {0.SideMember.Label}")

        """

        if label_format == "{0}":
            return

        from labels.format_labels import FormatSettings
        settings = FormatSettings(label_format=label_format,
                                  cell_format=cell_format)

        for r in matrix:
            _c = r[0].Count
            r.Member.Label = settings.label_format(r[0]) if _c > 0 else ""

    @wrap_matrix_logger_format
    def set_series_groups_formatted_labels(self, matrix, logger,
                                           label_format="{0}", cell_format={0},
                                           *args):
        """Set Group Labels to contain formatted labels of the users choice.

        Example:
        
        | myclass = transformations.MatrixManipulator(Matrix)
        | myclass.set_series_groups_formatted_labels(label_format =
        |                                       "{0.Label} :: {0.SortIndex}")

        """

        if label_format == "{0}":
            return

        from labels.format_labels import FormatSettings
        settings = FormatSettings(label_format=label_format,
                                  cell_format=cell_format)

        for grp in matrix.SideAxis.Groups:
            grp.Label = settings.label_format(grp)

    @wrap_matrix_logger
    def number_series(self, matrix, logger, *args):
        """Number the questions in sequential order in the row headings

        :param delimiter: Value to be placed after the statement number, eg "."
            Default ""  

        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | tr.number_series()
        
        """

        try:
            delimiter = args[0][0]
        except:
            delimiter = " "

        for r in matrix:
            _lbl = r.Member.Label
            r.Member.Label = str(r.Member.DataIndex + 1) + delimiter + _lbl

    @wrap_matrix_logger
    def del_base_series(self, matrix, logger, *args):
        """Delete any row containing the word 'Base'
        
        The Texts used as 'Base' can be amended as required using a list 
        parameter.
        
        :param: _list_of_bases: list of texts to be treated as bases. 
            Default = 'Base'
        
        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | tr.del_base_series()
        | or
        | _list_of_bases = ['Total', 'Base', 'All Respondents']
        | tr.del_base_series(_list_of_bases)
        
        """

        try:
            if args[0][0].__len__() > 0:
                bases = args[0][0]
        except:
            bases = ["Base"]
        
        _delete_rows = [r.Member.DataIndex for r in matrix if
                        r.Member.Label in bases]
        for item in reversed(_delete_rows):
            matrix.DeleteRow(item)

    def _get_matching_items(self, matrix, logger, _list_to_del, row):
        """Used by del_series.
        Return a list of matching indexes found in the matrix when compared
        with the _list_to_del.
        First check if matching labels, else check for matching indexes.

        """

        if row is True:
            _labels = self.get_series_labels()
            # identify if labels match
            _match = list()

            try:
                _match = [x for r in _list_to_del for x in _labels if
                          str(r) == x and str(r).__len__() > 1]
            except:
                pass
            if _match.__len__() > 0:  # labels found, find indexes for items
                _match_by_index = [
                    r.Member.DataIndex for r in matrix for x in _match
                    if str(x) in r.Member.Label]

                if _match.__len__() < _list_to_del.__len__():
                    _non_match = [
                        r for r in _list_to_del if r not in _match]
                    logger(str(_non_match) +
                           ": items not found in the matrix")
                return _match_by_index
            else:  # identify if indexes match
                _rows = matrix.Count
                _match = [
                    r for r in _list_to_del if r >= 0 and r < _rows]
                if _match.__len__() > 0:
                    if _match.__len__() != _list_to_del.__len__():
                        _non_match = [
                            r for r in _list_to_del if r < 0 or r >= _rows]
                        logger(str(_non_match) +
                               ": items not found in the matrix")
                    return _match
                else:
                    logger(str(_list_to_del) + ": No match found in list")
        else:  # columns
            _labels = self.get_category_labels()
            # identify if labels match
            _match = list()
            try:
                _match = [x for r in _list_to_del for x in _labels if
                          str(r) == x and str(r).__len__() > 1]
            except:
                pass
            if _match.__len__() > 0:  # labels found, find indexes for items
                _match_by_index = [
                    r.TopMember.DataIndex for r in matrix[0] for x in _match
                    if str(x) in r.TopMember.Label]

                if _match.__len__() < _list_to_del.__len__():
                    _non_match = [
                        r for r in _list_to_del if r not in _match]
                    logger(str(_non_match) +
                           ": items not found in the matrix")
                return _match_by_index

            else:  # identify if indexes match`
                _cols = matrix.TopAxis.DataMembers.Count
                _match = [
                    r for r in _list_to_del if r >= 0 and r < _cols]

                if _match.__len__() > 0:
                    if _match.__len__() != _list_to_del.__len__():
                        _non_match = [
                            r for r in _list_to_del if r < 0 or r >= _cols]
                        logger(str(_non_match) +
                               ": items not found in the matrix")
                    return _match
                else:
                    logger(str(_list_to_del) + ": No match found in list")

    def _del_items(self, matrix, logger, _list_to_del, row):
        """Delete the rows or columns in _list_to_del"""

        def _do_delete(_lst_by_index):
            """Delete the lstByIndex from matrix"""

            for item in reversed(_lst_by_index):
                if row is True:
                    matrix.DeleteRow(item)
                else:
                    matrix.DeleteColumn(item)

        _rows_or_cols = self._get_matching_items(matrix, logger,
                                                 _list_to_del, row)

        logger("Rows To Delete are: " + str(_rows_or_cols))
        if _rows_or_cols is not None:
            _do_delete(_rows_or_cols)

    # Select or Delete functions
    @wrap_matrix_logger
    def del_series(self, matrix, logger, _list_to_del, *args):
        """Remove specific series (row) labels or indexes from a selection.

        For example, delete Top 2 / Bottom 2 rows after they have been used for
        calculating Diff scores.

        :param _list_to_del: array containing an array of text labels
            or indexes.

        It is assumed that if a label is found then the _list_to_del
        is a list of labels, else it is a list of Indexes.
        
        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | tr.del_series(["myRow 1", "myRow 2"])
        | or
        | tr.del_series([1,2])
        """

        if "[" not in str(_list_to_del):
            logger(str(_list_to_del), ": _list_to_del parameter needs to be" +
                   "a list.  Nothing to delete")
            return

        try:
            _list_to_del = _list_to_del[0]
        except:
            pass

        # check if _list_to_del is empty, and return.
        if _list_to_del.__len__() == 0:
            logger("Nothing to delete")
            return
        # identify if _list_to_del contains labels or indexes present
        # in matrix, and delete the relevant items
        self._del_items(matrix, logger, _list_to_del, True)

    @wrap_matrix_logger
    def select_series(self, matrix, logger, _list_to_keep, *args):
        """Keep the rows found in the array `[_list_to_keep]`, and delete all
        other rows not in this selection.

        This is useful for a select all selection, and then you can pass in an
        array for which rows you wish to keep for each chart.

        :param _list_to_keep: Array containing an array of text labels.

        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | tr.select_series([["myRow 1", "myRow 2"]])
        
        """

        try:
            _list_to_keep = _list_to_keep[0]
        except:
            pass

        _found_list = self._get_matching_items(matrix, logger,
                                               _list_to_keep, True)

        if _found_list is not None:
            _lst_to_delete = [r.Member.DataIndex for r in matrix
                              if r.Member.DataIndex not in _found_list]
            self._del_items(matrix, logger, _lst_to_delete, True)
        else:
            logger("No selection found, all rows/cols will be deleted")
            _lst_to_delete = [r.Member.DataIndex for r in matrix]
            self._del_items(matrix, logger, _lst_to_delete, True)

    @wrap_matrix_logger
    def insert_gap_between_series_groups(self, matrix, logger, *args):
        """Insert a blank row between series groups within the Matrix for
        charts or tables
        
        Example:

        | tr = transformations.MatrixManipulator(Matrix)
        | tr.insert_gap_between_series_groups()

        """
        
        try:
            _previous_group = str(matrix.SideAxis.DataMembers[0].Group)
        except:
            raise ValueError("index was out of range. Group does not exist.")

        _insert_row = []

        for _r in range(0, matrix.Count):

            if (str(matrix.SideAxis.DataMembers[_r].Group) != _previous_group):
                _previous_group = str(matrix.SideAxis.DataMembers[_r].Group)
                _insert_row.append(_r-1)

        logger("insert_gap_between_groups, insert rows: " + str(_insert_row))

        for row in reversed(_insert_row):
            _row = matrix.SideAxis.DataMembers[row]
            _new_row = matrix.InsertBlankRowAfter(_row, "", "")

    @wrap_matrix_logger
    def insert_topN_into_series(self, matrix, logger, _N, *args):
        """Insert a new row at the top of the series containing
        topN result

        :param N: This is the number of rows to include in the summary
            row.
           
        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | tr.insert_topN_into_series(4)
        
        """

        # if the table hasn't got enough rows do nothing
        n = _N[0]
        if (matrix.Count < n):
            logger("Not enough rows in table to insert a Top "
                   + str(n) + " series")
            return

        # insert a blank row after n to hold our values
        _new_row = matrix.InsertBlankRowAfter(matrix.SideAxis.DataMembers[0],
                                              "TopN", "Top " + str(n))
        matrix.SwitchRows(0, 1)

        # go across all the columns and sum the values

        for col in matrix.TopAxis.DataMembers:
            sumVal = 0
            for _row in range(1, n+1):
                _val = matrix[_row][col.DataIndex][0].GetNumericValue()
                if _val is not None:
                    sumVal += matrix[_row][col.DataIndex][0].GetNumericValue()
                else:
                    sumVal = 0
                    logger("Cannot insert TopN into series. " +
                           "CellValue found is None")
                    break
            matrix[0][col.DataIndex].AddValue(str(int(sumVal * 100)) +
                                              "%", None)

    @wrap_matrix_logger_insert
    def insert_series(self, matrix, logger, row_number=0,
                      col_number=0, label="", *args):
        """Insert a row into the matrix.

        :param row_number: position to insert the row. Default = 0
        :param label: label for the inserted row. Default = ""

        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | tr.insert_series(row_number=2, label = "Inserted Row")
        
        """

        if row_number > matrix.Count-1:
            logger("cannot insert series, not enough rows")
            return

        _member = matrix[row_number].Member
        _name = "new_row" + str(row_number)
        _new_row = matrix.InsertBlankRowAfter(_member, _name, label)
        matrix.SwitchRows(_member.DataIndex, _new_row.DataIndex)

    #   End of class

if __name__ == "__main__":    
    import doctest
    doctest.testmod()


"""
To run doctest, using a command prompt, go to:

cd C:\Projects\RepSuite\Releases\4.3\Forgetdata\Libraries\Lib\forgetdata\Scripts>
>python transformations\series.py

"""