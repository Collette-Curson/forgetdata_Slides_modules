"""Provides basic matrix manipulation functions for categories for use within
data transformations.

Updated Jan 2016
@author: ccursons

"""

__version__ = '4.3.0'
from functools import wraps


class MatrixCategoryManipulator():
    r"""Class for manipulating series and series labels.
    This class is imported into MatrixManipulator in __init__.py within the
    transformations package

    Examples:
    >>> import categories as Categories
    >>> import utils.matrixfuncs as matrixfuncs
    >>> m = matrixfuncs.create_test_matrix()
    >>> _my_class = Categories.MatrixCategoryManipulator(m)
    >>> print _my_class.get_category_labels()  #taken from categories module
    [u'myColumn 0', u'myColumn 1', u'myColumn 2', u'myColumn 3', u'myColumn 4']
    >>> print _my_class.get_category_base_summary()
    myColumn 0: 101, myColumn 1: 20, myColumn 2: 330, myColumn 3: 102, myColumn 4: 51
    >>> _my_class.select_categories(["myColumn 1"])
    >>> print _my_class.get_category_labels()
    [u'myColumn 1']
    >>> m = matrixfuncs.create_test_matrix()
    >>> _my_class = Categories.MatrixCategoryManipulator(m)
    >>> _my_class.del_categories(["myColumn 1"])
    >>> print _my_class.get_category_labels()
    [u'myColumn 0', u'myColumn 2', u'myColumn 3', u'myColumn 4']

    """

    import utils.logger as log
    logger = log.logger

    def __init__(self, matrix):
        self.matrix = matrix

    def wrap_matrix_logger(func):
        # Wrapper function - Wrap all functions within the class so that the
        # matrix and log are passed to functions with given parameters

        @wraps(func)
        def func_wrapper(self, *args):
            # Return the class with a matrix and logger parameter

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
        def func_wrapper(self, row_number=0, column_number=0, label="", *args):
            # Return the class with a matrix and logger parameter

            matrix = self.matrix
            logger = self.logger
            return func(self, matrix, logger, row_number,
                        column_number, label, args)
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

    # Category Label functions (columns)
    @wrap_matrix_logger
    def get_category_labels(self, matrix, logger, *args):
        """Return a list containing the category (column) labels
        
        Example:
        
        | myclass = transformations.MatrixManipulator(Matrix)
        | labels = myclass.get_category_labels()
        
        """

        try:
            return [c.TopMember.Label for c in matrix[0]]
        except:
            logger("Index Error: Index was out of range")

    @wrap_matrix_logger
    def get_category_group_labels(self, matrix, logger, *args):
        """Return a list containing the category (column) group labels
        
        Example:
        
        | myclass = transformations.MatrixManipulator(Matrix)
        | group_labels = myclass.get_category_group_labels()
        
        """

        try:
            return [_grp.Label for _grp in matrix.TopAxis.Groups]
        except:
            logger("Index Error: Index was out of range")

    @wrap_matrix_logger
    def get_category_base_summary(self, matrix, logger, *args):
        """Return the Base summary of the Row, using the format:
        
        Column Label: Base Value, Column Label: Base Value

        Example:
        
        | myclass = transformations.MatrixManipulator(Matrix)
        | base_summary = myclass.get_category_base_summary()
        
        """

        from labels.format_labels import FormatSettings
        settings = FormatSettings(
            label_format="{0.TopMember.Label}: {0[0].Value}")

        return ", ".join([settings.label_format(c) for c in matrix[0]])

    @wrap_matrix_logger
    def set_category_base_summary(self, matrix, logger, *args):
        """Set Labels to category (column) labels with Base Value, using format:
        
        Column Label (Base Value)
        
        Example:
        
        | myclass = transformations.MatrixManipulator(Matrix)
        | myclass.set_category_base_summary()
        
        """

        from labels.format_labels import FormatSettings
        settings = FormatSettings(
            label_format="{0.TopMember.Label} (n={0[0].Value})")
        for _c in matrix[0]:
            _c.TopMember.Label = settings.label_format(_c) if _c.Count > 0 else ""
        matrix.DeleteRow(0)

    @wrap_matrix_logger_format
    def set_category_formatted_labels(
            self, matrix, logger, label_format="{0}", cell_format={0}, *args):
        """Set Labels to contain formatted labels of the users' choice.
        
        :param label_format: Text format using FormatSettings class to format
                the labels. 
        
        Example:
        
        | myclass = transformations.MatrixManipulator(Matrix)
        | myclass.set_categories_formatted_labels(
        |     label_format="{0.TopMember.Group.Label} :: {0.TopMember.Label}")

        """

        from labels.format_labels import FormatSettings
        settings = FormatSettings(
            label_format=label_format, cell_format=cell_format)
        if label_format != "{0}":
            for _c in matrix[0]:
                _c.TopMember.Label = settings.label_format(_c) if _c.Count > 0 else ""

    @wrap_matrix_logger_format
    def set_category_groups_formatted_labels(
            self, matrix, logger, label_format="{0}", cell_format={0}, *args):
        """Set Group Labels to contain formatted labels of the users' choice.
        
        :param label_format: Text format using FormatSettings class to format
                the labels. 
                
        Example:
        
        | myclass = transformations.MatrixManipulator(Matrix)
        | myclass.set_categories_groups_formatted_labels(
        |                             label_format="{0.Label} :: {0.SortIndex})

        """

        from labels.format_labels import FormatSettings
        settings = FormatSettings(
            label_format=label_format, cell_format=cell_format)
        if label_format != "{0}":
            for _grp in matrix.TopAxis.Groups:
                _grp.Label = settings.label_format(_grp)

    # Other functions for Selecting or Deleting
    @wrap_matrix_logger
    def del_base_category(self, matrix, logger, *args):
        """Delete any column containing the word 'Base'.
        
        The Texts used as 'Base' can be amended as required using a list 
        parameter.
        
        :param _list_of_bases: list of texts to be treated as bases. 
            Default = 'Base'
        
        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | tr.del_base_category()
        | or
        | _list_of_bases = ['Total', 'Base', 'All Respondents']
        | tr.del_base_category(_list_of_bases)
      
        """
        
        try:
            if args[0][0].__len__() > 0:
                bases = args[0][0]
        except:
            bases = ["Base"]
        
        
        _delete_cols = [c.TopMember.DataIndex for c in matrix[
            0] if c.TopMember.Label in bases]
        for item in reversed(_delete_cols):
            matrix.DeleteColumn(item)

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

        # identify if the _list_to_del contains labels in matrix
        # if _list_to_del.__len__() ==2 and _list_to_del[1]=="":
        #    _list_to_del = _list_to_del[0]

        # identify if the _list_to_del contains labels in matrix
        _rows_or_cols = self._get_matching_items(
            matrix, logger, _list_to_del, row)

        logger("Rows To Delete are: " + str(_rows_or_cols))

        if _rows_or_cols is not None:
            _do_delete(_rows_or_cols)

    #   Series and Categories - Select or Delete functions
    @wrap_matrix_logger
    def del_categories(self, matrix, logger, _list_to_del, *args):
        """Remove specific categories (columns) labels or indexes from a
        selection.

        For example, delete Don't know columns from a selection.

        :param _list_to_del: This is an array containing text labels or
            indexes.

        It is assumed that if a label is found then the _list_to_del
        is a list of labels, else it is a list of Indexes.
    
        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | tr.del_categories(["myColumn 1", "myColumn 2"])
        | or
        | tr.del_categories([1,2])
        
        """

        if "[" not in str(_list_to_del):
            logger(str(_list_to_del),
                   ": _list_to_del parameter needs to be a list. " +
                   "Nothing to delete")
            return

        try:
            _list_to_del = _list_to_del[0]
        except:
            pass

        #   check if _list_to_del is empty, and return.
        if _list_to_del.__len__() == 0:
            logger("Nothing to delete")
            return

        #   identify if _list_to_del contains labels or indexes present
        #   in matrix, and delete the relevant items
        self._del_items(matrix, logger, _list_to_del, False)

    @wrap_matrix_logger
    def select_categories(self, matrix, logger, _list_to_keep, *args):
        """Keep the categories (columns) found in the array `[_list_to_keep]`,
        and delete all other columns not in this selection.

        This is useful for a select all selection, and then you can pass in an
        array for which columns you wish to keep for each chart.

        :param _list_to_keep: Array containing an array of text labels.

        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | tr.select_categories([["myColumn 1", "myColumn 2"]])
        
        """

        try:
            _list_to_keep = _list_to_keep[0]
        except:
            pass

        _found_list = self._get_matching_items(
            matrix, logger, _list_to_keep, False)

        if _found_list is not None:
            _lst_to_delete = [c.TopMember.DataIndex for c in matrix[0]
                              if c.TopMember.DataIndex not in _found_list]
            self._del_items(matrix, logger, _lst_to_delete, False)
        else:
            logger("No selection found, all rows/cols will be deleted")
            _lst_to_delete = [c.TopMember.DataIndex for c in matrix[0]]
            self._del_items(matrix, logger, _lst_to_delete, False)

    @wrap_matrix_logger
    def insert_gap_between_category_groups(self, matrix, logger, *args):
        """Insert a blank column between category groups within the Matrix, for
        charts or tables
        
        Example:

        | tr = transformations.MatrixManipulator(Matrix)
        | tr.insert_gap_between_category_groups()
        
        """

        try:
            _previous_group = str(matrix.TopAxis.DataMembers[0].Group)
        except:
            raise ValueError("index was out of range. Group does not exist.")

        _insert_col = []
        for col in range(0, matrix.TopAxis.DataMembers.Count):
            if (str(matrix.TopAxis.DataMembers[col].Group) != _previous_group):
                _insert_col.append(col - 1)
                _previous_group = str(matrix.TopAxis.DataMembers[col].Group)

        logger(
            "insert_gap_between_groups, insert categories: " +
            str(_insert_col))

        for col in reversed(_insert_col):
            _new_col = matrix.InsertBlankColumnAfter(
                matrix.TopAxis.DataMembers[col], "", "")

    @wrap_matrix_logger_insert
    def insert_category(self, matrix, logger, row_number=0,
                        column_number=0, label="", *args):
        """Insert a column into the Matrix.

        :param column_number: position to insert the column. Default = 0
        :param label: label for the inserted column. Default = ""

        Example:

        | tr = transformations.MatrixManipulator(Matrix)
        | tr.insert_category(column_number=3, label = "Inserted Column")
        
        """

        if column_number > matrix.TopAxis.DataMembers.Count - 1:
            logger("cannot insert category, not enough columns")
            return

        _member = matrix[0][column_number].TopMember
        _name = "new_column" + str(column_number)
        _new_column = matrix.InsertBlankColumnAfter(_member, _name, label)
        
        import utils.utilities as utilities
        utilities.print_matrix(matrix)
        matrix.SwitchColumns(_member.DataIndex, _new_column.DataIndex)


if __name__ == "__main__":
    import doctest
    doctest.testmod()


"""
To run doctest, using a command prompt, go to:

cd C:\Projects\RepSuite\Releases\4.3\Forgetdata\Libraries\Lib\forgetdata\Scripts>
>python transformations\categories.py

"""