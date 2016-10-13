"""Provides basic matrix manipulation functions for data for use within data
transformations.

When used within transformation script in ppt:
import transformations
#reload(transformations)
#reload(transformations.sorting)
my_class = transformations.MatrixManipulator(Matrix)
my_class.sort_rows(Matrix, by_column = 0)

Updated August 2016
@author: ccurson

"""

__version__ = '4.3.0'
from functools import wraps


class MatrixDataSortManipulator():
    r"""Class for manipulating sorting of rows and columns.

    This class is imported into Data.MatrixDataManipulator in data.py within
    the transformations package.

    Examples:
    >>> import sorting
    >>> import utils.matrixfuncs as matrixfuncs
    >>> import utils.utilities as utilities
    >>> m = matrixfuncs.create_test_matrix()
    >>> _my_class = sorting.MatrixDataSortManipulator(m)
    >>> _my_class.sort_rows(by_column=1)
    >>> print m[0][0][0].Value
    1
    >>> print m[0].Member.Label
    myRow 2
    >>> _my_class.sort_columns(by_row=2)
    >>> print m[0][0][0].Value
    1
    >>> print m[0].Member.Label
    myRow 2
    >>> _my_class.sort_rows(client_name="myRow 4")
    >>> print m[0].Member.Label
    myRow 4
    >>> _my_class.sort_rows(descending=False)
    >>> print m[0].Member.Label
    myRow 2

    """

    def __init__(self, matrix):
        self.matrix = matrix

    import utils.logger as log
    logger = log.logger

    def wrap_matrix_logger_sort(func):
        """Wrapper function - Wrap all functions within the class so that
        the matrix and logger and all sorting parameters are passed to
        functions with given parameters. This wrapper also passes the
        sorting variables for sorting functions.
        
        """


        @wraps(func)
        def func_wrapper(self, matrix=None, logger=None, by_column=0, by_row=0,
                         using_cell_value=0, descending=True, file_name=None,
                         client_name=None, sort_row=None, *args):
            # Return the class with a matrix and logger parameter.

            matrix = self.matrix
            logger = self.logger

            return func(self, matrix, logger, by_column, by_row,
                        using_cell_value, descending, file_name, client_name,
                        sort_row, args)
        return func_wrapper

    def _update_labels_with_groups(self, sort_row):
        """Update the labels to include group labels as otherwise multi group
        selections for sorting will end up with confused group labels. For
        example a Top 2 summary table.
        
        """
        from labels.format_labels import FormatSettings
        
        if sort_row:
            for row in self.matrix:
                
                if row.Member.Group.Label != "":
                    settings = FormatSettings(label_format="Group:{0.Group}::: {0.Label}")
                else:
                    settings = FormatSettings(label_format="{0.Label}")
                label = settings.label_format(row.Member)
                row.Member.Label = unicode(label)
        else:
            for col in self.matrix[0]:
                
                if col.TopMember.Group.Label != "":
                    settings = FormatSettings(label_format="Group:{0.Group}::: {0.Label}")
                else:
                    settings = FormatSettings(label_format="{0.Label}")
                label = settings.label_format(col.TopMember)
                col.TopMember.Label = unicode(label)

    def _update_labels_remove_groups(self, sort_row):
        """Update the labels to remove the group labels added by
        _update_labels_with_groups.   
        
        NOTE: Do not remove the group labels in some multi-group selections.
        
        """
        
        if sort_row:
            # Only undo grp labels if the group count matches the number of
            # rows or group count = 1. If multiple items selected from multiple
            # groups then you will not be able to tell which is which without 
            # the group text.
            
            group_count = self.matrix.SideAxis.Groups.Count
            row_count = self.matrix.SideAxis.DataMembers.Count
            if group_count == row_count or group_count == 1:
                for row in self.matrix:
                    try:
                        full_label = row.Member.Label.split("::: ")
                        row.Member.Label = full_label[1]
                        _grp = full_label[0].split("Group:")[1].split("::: ")[0]                        
                        row.Member.Group.Label = _grp
                    except:
                        pass
                    
            else: # blank out groups labels as they are likely to be in wrong order.
                for row in self.matrix:
                    row.Member.Label = row.Member.Label.split("Group:")[1].replace("::: ", " : ")
                    row.Member.Group.Label = ""
                
        else:  
            # Only undo grp labels if the group count matches the number of
            # columns or group count = 1. If multiple items selected from
            # multiple groups then you will not be able to tell which is which 
            # without the group text.
            
            group_count = self.matrix.TopAxis.Groups.Count
            col_count = self.matrix.TopAxis.DataMembers.Count
            if group_count == col_count or group_count == 1:         
                for col in self.matrix[0]:
                    try:
                        full_label = col.TopMember.Label.split("::: ")
                        col.TopMember.Label = full_label[1]
                        _grp = full_label[0].split("Group:")[1].split("::: ")[0]
                        col.TopMember.Group.Label = _grp
                    except:
                        pass
                        
            else: # blank out groups labels as they are likely to be in wrong order.
                for col in self.matrix[0]:
                    col.TopMember.Label = col.TopMember.Label.split("Group:")[1].replace("::: ", " : ")
                    col.TopMember.Group.Label = ""
                
    @wrap_matrix_logger_sort
    def _make_dictionary_from_axis(self, matrix, logger, by_column, by_row,
                                   using_cell_value, descending, file_name,
                                   client_name, sort_row, *args):
        """Make a dictionary containing the structure of the Axis
        including Nets.

        Example:
        
        dict[ElementIndex][Label]
        dict[ElementIndex][NumericValue]
        dict[NetIndex][Label]
        dict[NetIndex][NumericValue]
        dict[NetIndex][ElementIndex][label]
        dict[NetIndex][ElementIndex][NumericValue]
        dict[NetIndex][InnerNetIndex][Label]
        dict[NetIndex][InnerNetIndex][Numeric Value]
        dict[NetIndex][InnerNetIndex][ElementIndex][label]
        dict[NetIndex][InnerNetIndex][ElementIndex][NumericValue]

        """
                
        def _make_dict(_d, member, val):

            _index = member.DataIndex
            _d[_index] = dict()
            _d[_index]["Label"] = member.Label
            _d[_index]["NumericValue"] = val

        _dict = dict()

        net_index = None
        if sort_row:
            for row in matrix:
                val = str(row[by_column][using_cell_value].NumericValue)
                member = row.Member
                if row.Member.IndentLevel == 0:
                    _make_dict(_dict, member, val)
                    net_index = row.Member.DataIndex
                if row.Member.IndentLevel == 1:
                    _make_dict(_dict[net_index], member, val)
                    net_index2 = row.Member.DataIndex
                if row.Member.IndentLevel == 2:
                    _make_dict(_dict[net_index][net_index2], member, val)

        else:  # sort_columns
            for col in matrix[by_row]:
                val = str(col[using_cell_value].NumericValue)
                member = col.TopMember
                if col.TopMember.IndentLevel == 0:
                    _make_dict(_dict, member, val)
                    net_index = col.TopMember.DataIndex
                if col.TopMember.IndentLevel == 1:
                    _make_dict(_dict[net_index], member, val)
                    net_index2 = col.TopMember.DataIndex
                if col.TopMember.IndentLevel == 2:
                    _make_dict(_dict[net_index][net_index2], member, val)
                
        #print "Nested dictionary from axis: ", _dict
        #print ""

        return _dict

    def _sorted_list_from_dict(self, matrix, descending, file_name,
                               client_name, _dict, sort_row):
        """Return a sorted list of tuples including:
        (DataIndex, Label, NumericValue).

        The sorted list represents the order for the axis to be displayed,
        keeping nets in place, and sorting items within the nets.
        Also taking into account file_name for keeping items at the end, and
        client_name for keeping items at the start.

        """

        from operator import itemgetter

        sorted_list = list()

        def add_to_list(_d, *args):
            """Interate through the different levels of the dictionary.
            Only pass *args if they are needed for the dict name structure,
            eg inner nets:  _dict[row[0]][row1[0]]

            """

            def _sort_tuple_nicely(l, _list=list()):
                """Return a list of tuples in sorted order, key based on item 2
                in the tuple, and reading values as numeric, not alpha

                """

                import re
                # Remove the decimal point and negative symbols before running 
                # isdigit().  Return key as a float
                convert = lambda l: float(l) if l.replace(".", "").replace("-", "").isdigit() else None
                alphanum_key = lambda key: [convert(c)
                                            for c in re.split('(-[0-9]+)', key)]

                _lst = sorted(l, key=alphanum_key, reverse=descending)
                
                _ret_list = list()
                for i in _lst:
                    for j in _list:
                        if j[2] == i:
                            if j not in _ret_list:
                                _ret_list.append(j)

                return _ret_list

            _list_of_tuples = [(k, _d[k]["Label"], _d[k]["NumericValue"]) for k
                               in _d.keys() if k != "NumericValue" and k != "Label"]
            
            _order = [l[2] for l in _list_of_tuples]
            
            if len(_list_of_tuples) > 0:

                for row in _sort_tuple_nicely(_order, _list=_list_of_tuples):
                    sorted_list.append(row)

                    try:
                        row1 = row
                        # elements in Net 1
                        add_to_list(_d[row[0]], [row1])
                        try:
                            row2 = row
                            # elements in inner Net
                            add_to_list(_d[row1[0]][row[0]], [row1, row2])
                        except:
                            pass
                    except:
                        pass
                                
            return sorted_list

        sorted_list = add_to_list(_dict)
        
        # if filename is not None, place these values at the end
        if file_name is None and client_name is None:
            return sorted_list

        def _find_keep_items(self):
            """If file_name is not None, find all items listed and place them
            at the end of the sorted list.

            And if client_name is not None, find client_name and place at
            the start of the sorted list.

            """

            # move client_name to start of list.
            
            # Note Matrix labels have been updated to include group name at
            # this point, so comparison is made to the split("::: ")
            if client_name is not None:
                if sort_row:
                    _keep_start = [x for x in sorted_list
                                   if client_name == matrix[int(x[0])].Member.Label.split("::: ")[1]]
                else:
                    _keep_start = [x for x in sorted_list
                                   if client_name == matrix[0][int(x[0])].TopMember.Label.split("::: ")[1]]
                if len(_keep_start) > 0:
                    sorted_list.remove(_keep_start[0])
                    sorted_list.insert(0, _keep_start[0])

            # move _keep_at_end  items to end of list.
            # Note Matrix labels have been updated to include group name at
            # this point, so comparison is made to the split("::: ")
            if file_name is not None:
                try:
                    # read the file_name file.
                    from utils.utilities import read_comma_separated_file
                    _keep_at_end = read_comma_separated_file(file_name)
                    
                    if _keep_at_end is not None:
                        if sort_row:
                            _keep_end = [x for x in sorted_list for item
                                         in _keep_at_end if item
                                         == matrix[int(x[0])].Member.Label.split("::: ")[1]]
                        else:
                            _keep_end = [x for x in sorted_list for item
                                         in _keep_at_end if item ==
                                         matrix[0][int(x[0])].TopMember.Label.split("::: ")[1]]

                        if len(_keep_end) > 0:
                            for item in _keep_end:
                                sorted_list.remove(item)
                                sorted_list.append(item)
                except:
                    print "Unable to read _file_name: " + file_name

        _find_keep_items(self)
        
        return sorted_list

    def _reorder_rows_and_cols(self, matrix, sorted_list, sort_row):
        """Reorder rows of Matrix based on an input list of rows."""

        from operator import itemgetter

        if sort_row:
            new_position = sorted_list.__len__()-1 # start at last row
            for required_row in reversed(sorted_list):
                # matrix labels will be rechecked on each iteration as the
                # positions of the rows can move each time.
                matrix_labels = list()
                i = 0  
                # note DataIndex is not used (i used instead) due to matrixfuncs
                # using a fake matrix which cannot reset DataIndex 
                for r in matrix:
                    matrix_labels.append((r.Member.Label, i))
                    i += 1
                
                for r in matrix_labels:
                    label = required_row[1]
                    current_position = r[1]
                    if r[0] == label:
                        
                        if current_position < new_position:
                            for _i in range(current_position, new_position):
                                matrix.SwitchRows(_i, _i+1)
                        elif current_position > new_position:
                            for _i in reversed(range(new_position,
                                                    current_position)):
                                matrix.SwitchRows(_i+1, _i)                        
                new_position -= 1
        else:
            
            new_position = sorted_list.__len__()-1 # start at last column
            for required_col in reversed(sorted_list):
                # matrix labels will be rechecked on each iteration as the
                # positions of the columns can move each time.
                matrix_labels = list()
                i = 0
                for c in matrix[0]:
                    matrix_labels.append((c.TopMember.Label, i))
                    i += 1
                
                for c in matrix_labels:
                    label = required_col[1]
                    current_position = c[1]

                    if c[0] == label:
                        if current_position < new_position:
                            for _i in range(current_position, new_position):
                                matrix.SwitchColumns(_i, _i+1)
                        elif current_position > new_position:
                            for i in reversed(range(new_position,
                                                    current_position)):
                                matrix.SwitchColumns(_i+1, _i)                        
                new_position -= 1
            
        return

    @wrap_matrix_logger_sort
    def sort_rows(self, matrix, logger, by_column, by_row,
                  using_cell_value, descending, file_name, client_name, *args):
        """Sorts the rows in the active matrix numerically, sort within nets
        and sort nets if present.

        :param by_column: Use the values in this column to determine the sort
                order of the rows. Default = 0
        :param using_cell_value: When there are multiple values within a cell
                use this to control which value row within each cell is used
                for sorting (zero-based). Default = 0
        :param descending: Determines the order in which the values should be
                sorted. Default = True
        :param file_name: text file containing a list of row names to fix at
                the end of the sort order on the table/chart.  
                file_name is located in the pptx folder, and contains a comma
                separated row, e.g.: "Other","Don't know","None of these"
                Default = None
        :param client_name: client_name is a text string which must match the
                row label exactly. This row will be placed first in the sort 
                order.  Default = None

        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | tr.sort_rows()
        | or
        | tr.sort_rows(by_column = 1, client_name = "Brand A")
        
        """

        if (matrix.Count < 2):
            print IndexError("index out of range " +
                             str(matrix.Count) + " row in table")
            pass

        if (matrix.TopAxis.DataMembers.Count <= by_column):
            raise IndexError("index out of range " +
                             str(by_column) + " by_column")

        if (matrix[by_row][by_column].Count < using_cell_value + 1):
            raise IndexError("index out of range " +
                             str(matrix[by_row][by_column].Count)
                             + " cell value in cell")

        # Sort the rows
        sort_row = True
        self._update_labels_with_groups(sort_row)
        _dict_from_axis = self._make_dictionary_from_axis(matrix, logger,
                                          by_column=by_column,
                                          using_cell_value=using_cell_value,
                                          descending=descending,
                                          sort_row=sort_row)
        _ordered_list = self._sorted_list_from_dict(matrix, descending,
                                                    file_name, client_name,
                                                    _dict_from_axis, sort_row)
        
        self._reorder_rows_and_cols(matrix, _ordered_list, sort_row)

        # This will only remove the group labels if the number of groups
        # matches the number of rows. 
        self._update_labels_remove_groups(sort_row)

    @wrap_matrix_logger_sort
    def sort_columns(self, matrix, logger, by_column, by_row,
                  using_cell_value, descending, file_name, client_name, *args):
        """Sorts the columns in the active matrix numerically, sort within nets
        and sort nets if present.

        :param by_row: Use the values in this row to determine the sort
                order of the columns. Default = 0
        :param using_cell_value: When there are multiple values within a cell
                use this to control which value row within each cell is used
                for sorting (zero-based). Default = 0
        :param descending: Determines the order in which the values should be
                sorted. Default = True
        :param file_name: text file containing a list of row names to fix at
                the end of the sort order on the table/chart.  
                file_name is located in the pptx folder, and contains a comma
                separated row, e.g.: "Other","Don't know","None of these"
                Default = None
        :param client_name: client_name is a text string which must match the
                column label exactly. This column will be placed first in the 
                sort order.  Default = None
        
        Example:
        
        | tr = transformations.MatrixManipulator(Matrix)
        | tr.sort_columns()
        | or
        | tr.sort_columns(by_row = 1, client_name = "Brand A")
        
        """

        if (matrix.TopAxis.DataMembers.Count < 2):
            raise IndexError("index out of range " +
                             str(matrix.Count) + " row in table")

        if (matrix.SideAxis.DataMembers.Count <= by_row):
            raise IndexError("index out of range " +
                             str(by_row) + " by_row")

        if (matrix[by_row][by_column].Count < using_cell_value + 1):
            raise IndexError("index out of range " +
                             str(matrix[by_row][by_column].Count)
                             + " cell value in cell")

        # Sort the columns
        sort_row = False
        self._update_labels_with_groups(sort_row)
        _dict_from_axis = self._make_dictionary_from_axis(matrix, logger,
                                          by_row=by_row,
                                          using_cell_value=using_cell_value,
                                          descending=descending,
                                          sort_row=sort_row)
        _ordered_list = self._sorted_list_from_dict(matrix, descending,
                                                    file_name, client_name,
                                                    _dict_from_axis, sort_row)
        self._reorder_rows_and_cols(matrix, _ordered_list, sort_row)
        self._update_labels_remove_groups(sort_row)


    #   End of class

if __name__ == "__main__":
    import doctest
    doctest.testmod()

"""
To run doctest, using a command prompt, go to:

cd
C:\Projects\RepSuite\Releases\4.3\Forgetdata\Libraries\Lib\forgetdata\Scripts
>python transformations\sorting.py

"""
