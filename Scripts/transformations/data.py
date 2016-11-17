"""Provides basic matrix manipulation functions for data for use within data
transformations.

Updated Aug 2016
@author: ccurson

"""

__version__ = '4.3.0'
from functools import wraps


from sorting import MatrixDataSortManipulator as SortRowsColumns

class MatrixDataManipulator(SortRowsColumns):
    r"""Class for manipulating data cells.
    This class is imported into matrixManipulator in __init__.py within the
    transformations package

    Examples:
    >>> import data as Data
    >>> import utils.matrixfuncs as matrixfuncs
    >>> m = matrixfuncs.create_test_matrix()
    >>> _my_class = Data.MatrixDataManipulator(m)
    >>> print _my_class.get_data_values()[0:9]
    [u'101', u'20', u'330', u'102', u'51', u'6', u'7', u'108', u'9']
    >>> m[0].Member.Label = "Base"
    >>> print _my_class.get_base_row_values()
    101, 20, 330, 102, 51
    >>> _my_class.sort_rows()
    >>> print m[1].Member.Label
    myRow 3
    >>> print m[0][3][0].Value
    102
    >>> print _my_class.get_data_values()[0:9]
    [u'101', u'20', u'330', u'102', u'51', u'100', u'10', u'12', u'13']
    
    """
    '''
    >>> _my_class.category_difference(1,2)
    >>> print m[0][3][0].Value
    310
    '''

    def __init__(self, matrix):
        self.matrix = matrix

    import utils.logger as log
    logger = log.logger

    #wrap functions
    def wrap_matrix_logger(func):
        @wraps(func)
        def func_wrapper(self, *args):
            # Wrapper function - Wrap all functions within the class so that
            # the matrix and logger are passed to functions with given parameters

            matrix = self.matrix
            logger = self.logger
            return func(self, matrix, logger, args)
        return func_wrapper

    def wrap_matrix_logger_format(func):
        # Wrapper function - Wrap all functions within the class so that the
        # matrix and logger are passed to functions with given parameters.
        # This wrapper also passes a label_format and cell_format property for
        # the formatting for labels.

        @wraps(func)
        def func_wrapper(self, matrix=None, logger=None, label_format="{0}", 
                         cell_format="{0}", *args):
            # Return the class with a matrix and logger parameter.

            matrix = self.matrix
            logger = self.logger
            
            return func(self, matrix, logger, label_format, cell_format, args)
        return func_wrapper


    #   Data Value functions
    @wrap_matrix_logger
    def get_data_values(self, matrix, logger, *args):
        """Return a list of lists containing the data values for each row
        of the matrix.
        Only the first cell item will be returned.

        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | data_values = tr.get_data_values()
        
        """

        return [c[0].Value if c.Count != 0 else "" for r in matrix for c in r]

    @wrap_matrix_logger
    def get_base_row_values(self, matrix, logger, *args):
        """Return a list of base values from the base (first) column of the
        matrix. Bases will be returned from rows with Label, Total or Base.

        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | base_row_values = tr.get_base_row_values()
        
        """

        from labels.format_labels import FormatSettings
        settings = FormatSettings(label_format="{0[0].Value}")
        _base_labels = ["Base", "Total"]
        return ", ".join([settings.label_format(c)
                          for r in matrix for c in r if
                          r.Member.Label in _base_labels])

    @wrap_matrix_logger
    def get_base_column_values(self, matrix, logger, *args):
        """Return a list of base values from the base (first) row of the
        matrix. Bases will be returned from columns with Label, Total or Base.

        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | base_column_values = tr.get_base_column_values()
        
        """

        from labels.format_labels import FormatSettings
        settings = FormatSettings(label_format="{0[0].Value}")

        matrix[0][0].TopMember.Label = "Base"
        _base_labels = ["Base", "Total"]
        return ", ".join(
            [settings.label_format(c) for r in matrix for c in r
             if c.TopMember.Label in _base_labels])

    @wrap_matrix_logger
    def get_dict_cell_values(self, matrix, logger, *args):
        """Return a dictionary containing the row/column and data values for
        each cell within the matrix.
        All cell items will be returned.

        Dictionary format:

        | {
        | 'row1':
        |     {
        |     'col1': [cell Value1, cell Value2],
        |     'col2': [cell Value1, cell Value2]
        |     },
        | 'row2':
        |     {
        |     'col1': [cell Value1, cell Value2],
        |     'col2': [cell Value1, cell Value2]
        |     }
        | }

        Example:
         
        | tr = transformations.MatrixManipulator(Matrix)
        | cell_value_dict = tr.get_dict_cell_values()
        
        """

        label = ""
        top_label = ""
        _AllCellItems = dict()
        for r in matrix:
            for c in r:
                label = r.Member.Label + " " + str(r.Member.Group.SortIndex)
                _AllCellItems.setdefault(label, dict())
                top_label = c.TopMember.Label + " " + \
                    str(c.TopMember.Group.SortIndex)
                _AllCellItems[label].setdefault(top_label, None)

                _AllCellItems[label][top_label] = [item.Value for item in c]
        return _AllCellItems

    @wrap_matrix_logger_format
    def set_data_formatted_labels(self, matrix, logger, label_format="{0}",
                                  cell_format="{0}", *args):
        """Set Labels of the data cells to contain formatted labels of the
        users' choice.

        :param cell_format: Text format using FormatSettings class to format
            the cell values.
                
        Example:
        
        | myclass = transformations.MatrixManipulator(Matrix)
        | myclass.set_data_formatted_labels(cell_format =
        |         "{0[0].Value} - {0.SideMember.Label} : {0.TopMember.Label}")

        """
        
        if cell_format == "{0}":
            return
        from labels.format_labels import FormatSettings
        settings = FormatSettings(
            label_format=label_format,
            cell_format=cell_format)

        for r in matrix:
            for c in r:
                c[0].Value = settings.cell_format(matrix[r.Member.DataIndex][
                    c.TopMember.DataIndex]) if c[
                    0].GetNumericValue() is not None else c[0].Value

    @wrap_matrix_logger_format
    def format_percent_as_whole_number(self, matrix, logger, *args):
        """Set data values that are stored as percentages to be whole numbers
                
        Example:
        
        | myclass = transformations.MatrixManipulator(Matrix)
        | myclass.format_percent_as_whole_number()

        """
        
        for r in matrix:
            for c in r:
                if c[0].FormatString == "0%" or c[0].FormatString == "0.00%":
                    c[0].NumericValue = c[0].NumericValue * 100
                    c[0].FormatString = "0"
    
    @wrap_matrix_logger_format
    def format_whole_number_as_percent(self, matrix, logger, *args):
        """Set data values that are stored as whole number to be percentages
                
        Example:
        
        | myclass = transformations.MatrixManipulator(Matrix)
        | myclass.format_whole_number_as_percent()

        """
        
        for r in matrix:
            for c in r:
                if c[0].FormatString == "0" or c[0].FormatString == "0.00":
                    c[0].NumericValue = c[0].NumericValue / 100
                    c[0].FormatString = "0%"
                    
                                    
    @wrap_matrix_logger
    def category_difference(self, matrix, logger, *args):
        """Insert a new column and insert the difference between the
        2 selected categories, y-x

        :param x: First Column in the difference calculation
        :param y: Second Column in the difference calculation
        
        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | tr.category_difference(0,1)
        
        """

        try:
            _x = args[0][0]
            _y = args[0][1]
        except:
            logger("No suitable columns chosen")
            return

        _cols = matrix.TopAxis.DataMembers

        # if the table hasn't got enough categories issue error
        if _cols.Count < _y:
            logger("IndexError: index out of range " + str(_y))
            return
        if _cols.Count < _x:
            logger("IndexError: index out of range " + str(_x))
            return
        # insert a blank row after y to hold our values
        _newColumn = matrix.InsertBlankColumnAfter(_cols[_y], "diff", "Shift")

        # Using the matrix, and find the difference of y-x and put into the new
        # column
        for row in matrix:
            # calculate the difference value
            try:
                _valx = row[_x][0].GetNumericValue()
                _valy = row[_y][0].GetNumericValue()
                _valnew = _valy - _valx
            except:
                _valnew = "-"
            # place the diff value into the new column, and format the result
            # the same as the original values.
            cell = row[_newColumn]
            cell.AddValue(str(_valnew), None)
            try:
                cell[0].FormatString = row[_x][0].FormatString
            except:
                pass

    @wrap_matrix_logger
    def renumber_sig_tests(self, matrix, logger, *args):
        """Renumber stats test results to ABC order for the selected columns.

        If the selection made only contains some columns, then the original
        Sig test result column names will be confusing when displayed on the
        slide. You can renumber them to the ABC order before presenting the
        results on the slide.

        :param _warn_when_no_stats: If no Statistics results are present in the
            Matrix, a warning will be issued. Default value is False
            
        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | _warn_when_no_stats = True
        | tr.renumber_sig_tests(_warn_when_no_stats)
        
        """

        try:
            _warn_when_no_stats = args[0][0]
        except:
            _warn_when_no_stats = False
        _letter_mapping = dict()
        _atoz = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        _counter = 0

        # if counter > 25, an error is raised as the renumbering will be
        # incorrect.
        _numCol = matrix.TopAxis.DataMembers.Count
        if _numCol > 25 or _numCol == 0:
            logger("IndexError: index out of range " + str(_numCol))
            # return

        _contains_stats = False
        # Assign the correct letter to the selected columns
        for col in matrix.TopAxis.DataMembers:
            if(len(col.MemberSigTestHeading) > 0):
                _contains_stats = True
                _logical_letter = str(_atoz[_counter])
                _letter_mapping[col.MemberSigTestHeading] = _logical_letter
                col.MemberSigTestHeading = str(_logical_letter)
                _counter += 1
        if _warn_when_no_stats:
            if _contains_stats is False:
                logger("ValueError: No stats results found in matrix")

        # use mapping to map the original result to the new letter and update
        # the cell with the new result.
        for row in matrix:
            for cell in row:
                if cell.Count > 1:
                    _original = cell[cell.Count - 1].Value
                    _new = str()
                    for letter in _original:
                        if(letter in _letter_mapping):
                            _new += _letter_mapping[letter]
                    cell[cell.Count - 1].Value += _new
                    cell.SigTestResult = _new

    @wrap_matrix_logger
    def convert_significance_results_to_arrows(self, matrix, logger, *args):
        """Convert your significant results into up and down arrows within
        your chart.

        This script is used in conjunction with
        charts.convert_glyphs_to_color_wingdings(Chart) function as this
        changes the font to display the arrows in the data label of the chart.

        This example script assumes that the number of cell Items in the table
        is 1, plus the significance test result is present where appropriate.

        This was created using a table which showed significant difference
        between one column (wave) and the next column (wave) only, so maximum
        result per cell is 1. In addition, the significance was displayed in
        the current column if it was significantly higher or lower (sometimes
        significance results are displayed in the higher column).
        
        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | tr.convert_significance_results_to_arrows()
        
        In the Afterfill action, you will now need to run:
        
        | charts.convert_glyphs_to_color_wingdings(Chart)
        
        """

        # Check if there are Stats Columns in this table?
        _statsFound = 0
        for i in range(0, matrix.TopAxis.DataMembers.Count):
            if matrix.TopAxis.DataMembers[
                    i].MemberSigTestHeading.__len__() > 0:
                _statsFound = 1
                break

        if _statsFound == 0:
            logger("ValueError: index was out of range. MemberSigTestHeading" +
                   "not found")

        _matrixcols = matrix.TopAxis.DataMembers

        for row in matrix:
            for col in row:
                _colIndex = col.TopMember.DataIndex
                if col.Count > 1:  # sigTestResultPresent
                    # Need to find which column it's significantly different
                    # to:
                    _significanceColumn = -1
                    for _colHeader in range(0, _matrixcols.Count):
                        _mc = _matrixcols[_colHeader]
                        if _mc.MemberSigTestHeading in col[1].Value:
                            _significanceColumn = _colHeader
                    if _significanceColumn > -1:
                        if col[0].Value > row[_significanceColumn][0].Value:
                            col.AddValue(chr(0xE9), None)
                            col.AddValue("up", None)
                            row[_colIndex].RemoveValueAt(1)
                            row[_colIndex].SigTestResult = col[1].Value
                        else:
                            col.AddValue(chr(0xEA), None)
                            col.AddValue("down", None)
                            row[_colIndex].RemoveValueAt(1)
                            row[_colIndex].SigTestResult = col[1].Value


    @wrap_matrix_logger
    def clone_matrix(self, matrix, logger, *args):
        """Clone a matrix into another object for use when manipulating data.
    
        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | clone_matrix = tr.clone_matrix()

        """

        try:
            import System.Xml
        except:
            import clr
            clr.AddReference("System.Xml")
        from System.Xml.Serialization import XmlSerializer

        ser = XmlSerializer(matrix.GetType())
        import System.IO
        stream = System.IO.MemoryStream()
        ser.Serialize(stream, matrix)
        stream.Seek(0, System.IO.SeekOrigin.Begin)
        matrix_clone = ser.Deserialize(stream)
        stream.Close()
        return matrix_clone

    @wrap_matrix_logger
    def make_series_from_grid_slices(self, matrix, logger, *args):
        """Creates a grid format table from a flat table where you have grid
        slices appended down the side of the table, and wish these selections
        to appear as one series.
        
        For example (3 series):
        
        |   Statement 1 - Top2   X
        |   Statement 2 - Top2   X
        |   Statement 3 - Top2   X
        |
        
        This will appear as (1 series):
        
        | ____|Statement 1|Statement 2|Statement 3|
        | Top2|
        | 
        
        Note, this does not work when there is nesting or concatenation on the
        top axis.

        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | tr.make_series_from_grid_slices()
        
        """

        if (matrix.SideAxis.Groups.Count < 2):
            return  # nothing to do
        if (matrix.TopAxis.Groups.Count > 1):
            raise Exception(
                "The table cannot have nesting or concatenation on the top")

        # replicate the existing top group for each selected series
        _master_top_group = matrix.TopAxis.Groups[0]
        _master_side_group = matrix.SideAxis.Groups[0]

        for _i in range(1, matrix.SideAxis.Groups.Count):
            # active_group means the one we are transferring from side to top
            _active_group = matrix.SideAxis.Groups[_i]

            # top_group is the new group we are creating for the top
            _top_group = matrix.TopAxis.Groups.AddNew(
                None, _active_group.Name + "_top", _active_group.Label)
            for _master_member in _master_top_group:
                _new_member = _top_group.AddNewMember(
                    _master_member.Name,
                    _master_member.Label,
                    _master_member.IsVisible,
                    _master_member.IsSummaryScore)
                matrix.TopAxis.DataMembers.Add(_new_member)

            # transfer any values over from side to top to become part of the
            # main series
            for _member in _active_group:
                _source_row = matrix[_member]
                # find the target row in the first group
                for _target_member in _master_side_group:
                    if _target_member.Label == _member.Label:
                        _target_row = matrix[_target_member]

                        for _i in range(_master_top_group.Count):
                            _source_col = _master_top_group[_i]
                            _target_col = _top_group[_i]
                            for _val in _source_row[_source_col]:
                                _target_row[_target_col].AddValue(_val)

        _master_top_group.Label = matrix.SideAxis.Groups[0].Label

        while matrix.Count > _master_side_group.Count:
            matrix.DeleteRow(_master_side_group.Count)

    @wrap_matrix_logger
    def merge_series_by_label(self, matrix, logger, *args):
        """
        Merges the series (rows) in the active matrix by their labels.

        For example:

        |     _________|January|Februar|  March|  April|    May|   June|
        |     Brand 1|
        |     Brand 1|
        | 
        
        will merge to:

        |     _________|January|Februar|  March|  April|    May|   June|
        |     Brand 1|
        |
        
        Example: 
        
        | tr = transformations.MatrixManipulator(Matrix)
        | tr.merge_series_by_label()
        
        """

        _dict_series = dict()
        _rows_to_del = []
        for row in matrix:
            if(row.Member.Label in _dict_series):
                _target_row = _dict_series[row.Member.Label]

                for cell in row:
                    _target_cell = _target_row[cell.TopMember]
                    for value in cell:
                        _clone = value.Clone()
                        _target_cell.AddValue(_clone)
                _rows_to_del.append(row.Member.DataIndex)
            else:
                _dict_series[row.Member.Label] = row

        # clear up by deleting the merged rows out
        _rows_to_del.reverse()
        for _i in _rows_to_del:
            matrix.DeleteRow(_i)

    @wrap_matrix_logger
    def merge_categories_by_label(self, matrix, logger, *args):
        """
        Merges the categories (columns) in the active matrix by their labels.

        For example:
        
        |    _________|January|Februar|  March|January|Februar|  March|
        |    Brand 1|
        |    Brand 2|
        |
        
        will merge to:
        
        |    _________|January|Februar|  March|
        |    Brand 1|
        |    Brand 2|
        |
        
        Example: 
        
        | tr = transformations.MatrixManipulator(Matrix)
        | tr.merge_categories_by_label()
        
        """

        _dict_cols = dict()
        _cols_to_del = []
        for col in matrix.TopAxis.DataMembers:
            if(col.Label in _dict_cols):
                targetcol = _dict_cols[col.Label]

                for row in matrix:
                    cell = row[col]
                    _target_cell = row[targetcol]
                    for value in cell:
                        _clone = value.Clone()
                        _target_cell.AddValue(_clone)
                _cols_to_del.append(col.DataIndex)
            else:
                _dict_cols[col.Label] = col

        _cols_to_del.reverse()
        for _i in _cols_to_del:
            matrix.DeleteColumn(_i)
    
    #   End of class

if __name__ == "__main__":
    import doctest
    doctest.testmod()

"""
To run doctest, using a command prompt, go to:

cd C:\Projects\RepSuite\Releases\4.3\Forgetdata\Libraries\Lib\forgetdata\Scripts>
>python transformations\data.py

"""