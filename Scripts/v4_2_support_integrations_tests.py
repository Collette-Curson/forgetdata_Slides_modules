'''
Updated 7th April 2016
@author: ccurson

###v4_2_support MODULE TESTS
This set of regression tests will test all of the functions within the
"v4_2_support" module of the main Scripts installed with Slides.

This class is to be used for other data formats, eg pandas, so run these
with the matrixfuncs.py to generate the Matrix from a List.

Also to be run using Matrix created using Slides.

See $RepSuite\Releases\4.3\Forgetdata\Libraries\Lib\forgetdata\Scripts\

v4_2_support.py module.

'''

########Variables that can be reset when running this test###############

use_test_data = True

# Real data only used when use_test_data == False.

import os

mtd_filepath = os.path.abspath(os.path.join(
    '\\transformations\\utils\\Master Demo 2010.mtd'))

# table within mtd file used for tests when use_test_data==False

table_selected = 0

if use_test_data:

    print ""
    print "This regression test is run using TEST DATA"
    print ""

else:

    print ""
    print "This regression test is run using SLIDES! DATA"
    print ""

#########################################################################


from unittest import (TestCase, main)
import transformations as tr
import transformations.utils.matrixfuncs as matrixfuncs
import v4_2_support

def make_matrix():
    """make a matrix either from test_matrix or by connecting to Slides."""

    # this imports category, category, data, text, pptx_data

    if use_test_data:
        # make a test matrix using create_test_matrix
        m = matrixfuncs.create_test_matrix()

    else:
        # make a matrix by connecting to Slides! and connecting to a data
        # table.
        import transformations.utils.slidesconf as slidesconf
        from Forgetdata.Matrix import ConnectionDefinition
        conn = ConnectionDefinition()
        conn.ConnectionString = mtd_filepath  # set at top of file
        conn.Name = "Test"
        conn.Provider = "SPSS MTD File"
        liveConnection = slidesconf.connect(conn.ConnectionString,
                                            name=conn.Name,
                                            provider_name=conn.Provider)

        m = liveConnection[table_selected]

    x = tr.MatrixManipulator(m)
    matrixfuncs.printMatrix(m)

    for c in m[0]:
        c.TopMember.Label = c.TopMember.Label.encode('ascii', 'ignore')

    return m, x


class Test(TestCase):

    """Class for unit testing v4_2_support.py module from Slides.
    m is a matrix created from a list of lists or is a Slides Matrix
    defined by defined by make_matrix()

    """

    def _addStatsHeadersToMatrix(self, m):
        """This will add stats test headers into the Matrix."""

        atoz = "JKLMNOPQRSTUVWXYZABCDEFGHI"

        counter = 0

        for col in m.TopAxis.DataMembers:
            if counter < 26:
                logicalletter = str(atoz[counter])
                col.MemberSigTestHeading = logicalletter
                counter += 1
            else:
                counter = 0

    def _addStatsTestsToMatrix(self, m):
        """This will add stats test headers and results into the Matrix."""

        # add stat letters to columns
        self._addStatsHeadersToMatrix(m)

        # add stat results to cells
        for row in m:
            for cell in row:
                # set the stat result to be the same as the next column's stat
                # heading
                try:
                    cell.SigTestResult = m.TopAxis.DataMembers[
                        cell.TopMember.DataIndex + 1].MemberSigTestHeading
                except:
                    cell.SigTestResult = m.TopAxis.DataMembers[
                        0].MemberSigTestHeading
                cell.AddValue(cell.SigTestResult, None)

    def _rank_position(self, _lst_incl_cells):
        """Used by sorting functions for testing the order within a table,
        returns a set as rows can have equal rank, so order cannot be used.

        """

        counter = 0
        previous_val = 0
        _new_set = set()

        for item in _lst_incl_cells:
            if item != "":
                _val = item.split(" ", 1)
                if _val[0] != previous_val:
                    counter += 1
                _new_set.add((counter, _val[1]))
                previous_val = _val[0]
        return _new_set

    def _sorted_nicely(self, l):
        """Sort numerically, exclude non numeric results from the sort """

        import re

        convert = lambda text: int(text) if text.isdigit() else ""

        alphanum_key = lambda key: [
            convert(c) for c in re.split(
                '([0-9]+)', key)]

        return sorted(l, key=alphanum_key)

    def _sorting_order_rows(
            self,
            m,
            byColumn=0,
            usingCellValue=0,
            descending=True,
            file_name=None,
            client_name=None):
        """Sort matrix into the sorted order without using sort functions.
        Get rank position to calculate if the output is correct.

        """

        def _get_list_without_excluded_items(client_name, _keep_at_end):

            if _keep_at_end != []:
                return [str(r[byColumn][usingCellValue].Value) + " " +
                        r.Member.Label for r in m if not r.Member.Label in \
                        _keep_at_end]

            elif client_name is not None:
                return [str(r[byColumn][usingCellValue].Value) + " " +
                        r.Member.Label for r in m if \
                        r.Member.Label != client_name]

            else:
                return [str(r[byColumn][usingCellValue].Value) +
                        " " + r.Member.Label for r in m]

        _keep_at_end = self._get_keep_at_end(file_name)

        _lst = _get_list_without_excluded_items(client_name, _keep_at_end)

        # reverse the list to make ascending order
        if descending:
            _lst_incl_cells = list(reversed(self._sorted_nicely(_lst)))
        else:
            _lst_incl_cells = list(self._sorted_nicely(_lst))

        return self._rank_position(_lst_incl_cells)

    def _sorting_order_columns(
            self,
            m,
            byRow=0,
            usingCellValue=0,
            descending=True,
            file_name=None,
            client_name=None):
        """Sort matrix into the sorted order without using sort functions.
        Get rank position to calculate if the output is correct.

        """

        def _get_list_without_excluded_items(client_name, _keep_at_end):

            if _keep_at_end != []:
                return [str(c[usingCellValue].Value) + " " + \
                        c.TopMember.Label for c in m[byRow] if not \
                        c.TopMember.Label in _keep_at_end]

            elif client_name is not None:
                return [str(c[usingCellValue].Value) + " " + \
                        c.TopMember.Label for c in m[byRow] if \
                        c.TopMember.Label != client_name]

            else:
                return [str(c[usingCellValue].Value) + " " +
                        c.TopMember.Label for c in m[byRow]]

        _keep_at_end = self._get_keep_at_end(file_name)

        _lst = _get_list_without_excluded_items(client_name, _keep_at_end)

        # reverse the list to make ascending order
        if descending:
            _lst_incl_cells = list(reversed(self._sorted_nicely(_lst)))
        else:
            _lst_incl_cells = list(self._sorted_nicely(_lst))

        return self._rank_position(_lst_incl_cells)

    def _get_keep_at_end(self, file_name):
        """Return a list from a csv file."""

        from transformations.utils.utilities import read_comma_separated_file
        try:
            _keep_at_end = read_comma_separated_file(file_name)
        except:
            raise "Unable to read _file_name: "

        if _keep_at_end is None:
            _keep_at_end = list()
        return _keep_at_end

    def _get_labels_from_m_rows(
            self,
            m,
            byColumn=0,
            usingCellValue=0,
            descending=True,
            file_name=None,
            client_name=None):
        """Return a list of formated labels with values from matrix"""

        # note usingCellValue is not implemented as it wasnt working as
        # expected in this line:

        #settings = FormatSettings(label_format="{0[usingCellValue].Value} \
        #{0.SideMember.Label}")

        from transformations.labels.format_labels import FormatSettings

        settings = FormatSettings(
            label_format="{0[0].Value} {0.SideMember.Label}")

        if file_name is not None:
            _keep_at_end = self._get_keep_at_end(file_name)
            _labels_tmp = [settings.label_format(r[byColumn]) if r[
                0].Count > 0 and not r.Member.Label in _keep_at_end else "" \
                           for r in m]

        elif client_name is not None:
            _labels_tmp = [settings.label_format(r[byColumn]) if r[
                0].Count > 0 and r.Member.Label != client_name else "" \
                           for r in m]

        else:
            _labels_tmp = [
                settings.label_format(
                    r[byColumn]) if r[byColumn].Count > 0 else "" for r in m]

        if descending:
            return self._rank_position(
                reversed(self._sorted_nicely(_labels_tmp)))

        else:
            return self._rank_position(self._sorted_nicely(_labels_tmp))

    def _get_labels_from_m_columns(
            self,
            m,
            byRow=0,
            usingCellValue=0,
            descending=True,
            file_name=None,
            client_name=None):
        """Return a list of formated labels with values from matrix"""

        # note usingCellValue is not implemented as it wasnt working as
        # expected in this line:

        #settings = FormatSettings(label_format="{0[usingCellValue].Value} \
        #{0.SideMember.Label}")

        from transformations.labels.format_labels import FormatSettings
        settings = FormatSettings(
            label_format="{0[0].Value} {0.TopMember.Label}")

        if file_name is not None:
            _keep_at_end = self._get_keep_at_end(file_name)

            _labels_tmp = [settings.label_format(c) if m[
                byRow].Count > 0 and not c.TopMember.Label in \
                           _keep_at_end else "" for c in m[byRow]]

        elif client_name is not None:
            _labels_tmp = [settings.label_format(c) if m[byRow].Count > 0 and \
                           c.TopMember.Label != client_name else "" 
                           for c in m[byRow]]

        else:
            _labels_tmp = [settings.label_format(
                c) if m[byRow].Count > 0 else "" for c in m[byRow]]

        if descending:
            return self._rank_position(
                reversed(self._sorted_nicely(_labels_tmp)))

        else:
            return self._rank_position(self._sorted_nicely(_labels_tmp))

    #########################################################

    # Start of regression tests for v4_2_support module     #

    #########################################################

    def test_SortRows_default(self):

        m, x = make_matrix()
        _sort_col = 0
        _matrix_labels = self._sorting_order_rows(
            m, byColumn=_sort_col, usingCellValue=0)
        v4_2_support.SortRows(Matrix=m,)
        _labels = self._get_labels_from_m_rows(m, byColumn=_sort_col)

        self.assertTrue(_labels.difference(_matrix_labels) == set([]))
        print "test_SortRows_default", _labels

    def test_SortRows_byColumn(self):

        m, x = make_matrix()
        _sort_col = 2
        _matrix_labels = self._sorting_order_rows(
            m, byColumn=_sort_col, usingCellValue=0)
        v4_2_support.SortRows(Matrix=m, byColumn=_sort_col)
        _labels = self._get_labels_from_m_rows(m, byColumn=_sort_col)

        self.assertTrue(_labels.difference(_matrix_labels) == set([]))
        print "test_SortRows_byColumn", _labels

    def test_SortRows_byColumn_invalid(self):
        
        m, x = make_matrix()
        _sort_col = 100
        
        with self.assertRaisesRegexp(IndexError, 'index out of range'):
            v4_2_support.SortRows(Matrix=m, byColumn=_sort_col)
        print "test_SortRows_byColumn_invalid", "_sort_col = ", _sort_col

    def test_SortRows_usingCellValue(self):

        m, x = make_matrix()
        _usingCellValue = 0
        _matrix_labels = self._sorting_order_rows(
            m, byColumn=0, usingCellValue=_usingCellValue)
        v4_2_support.SortRows(Matrix=m, usingCellValue=_usingCellValue)
        _labels = self._get_labels_from_m_rows(
            m, usingCellValue=_usingCellValue)

        self.assertTrue(_labels.difference(_matrix_labels) == set([]))
        print "test_SortRows_usingCellValue", _labels

    def test_SortRows_usingCellValue_invalid(self):

        m, x = make_matrix()
        _usingCellValue = 3
        
        with self.assertRaisesRegexp(IndexError, 'index out of range'):
            v4_2_support.SortRows(Matrix=m, usingCellValue=_usingCellValue)
        print "test_SortRows_usingCellValue_invalid", _usingCellValue

    def test_SortRows_descending(self):

        m, x = make_matrix()
        _descending = True
        _matrix_labels = self._sorting_order_rows(m, descending=_descending)
        v4_2_support.SortRows(Matrix=m, descending=_descending)
        _labels = self._get_labels_from_m_rows(m, descending=_descending)

        self.assertTrue(_labels.difference(_matrix_labels) == set([]))
        print "test_SortRows_descending", _labels

    def test_SortRows_ascending(self):

        m, x = make_matrix()
        _descending = False
        _matrix_labels = self._sorting_order_rows(m, descending=_descending)
        v4_2_support.SortRows(Matrix=m, descending=_descending)
        _labels = self._get_labels_from_m_rows(m, descending=_descending)

        self.assertTrue(_labels.difference(_matrix_labels) == set([]))
        print "test_SortRows_ascending", _labels

    def test_SortRows_with_all_options(self):

        m, x = make_matrix()
        _byColumn = 2
        _usingCellValue = 0
        _descending = False
        _matrix_labels = self._sorting_order_rows(
            m,
            byColumn=_byColumn,
            usingCellValue=_usingCellValue,
            descending=_descending)
        v4_2_support.SortRows(
            Matrix=m,
            byColumn=_byColumn,
            usingCellValue=_usingCellValue,
            descending=_descending)
        _labels = self._get_labels_from_m_rows(
            m,
            byColumn=_byColumn,
            usingCellValue=_usingCellValue,
            descending=_descending)
        
        self.assertTrue(_labels.difference(_matrix_labels) == set([]))
        print "test_SortRows_with_all_options", _labels

    def test_SortColumns_default(self):

        m, x = make_matrix()
        _sort_row = 0
        _matrix_labels = self._sorting_order_columns(m, byRow=_sort_row)
        v4_2_support.SortColumns(Matrix=m, )
        _labels = self._get_labels_from_m_columns(m, byRow=_sort_row)

        self.assertTrue(_labels.difference(_matrix_labels) == set([]))
        print "test_SortColumns_default", _labels

    def test_SortColumns_byRow(self):

        m, x = make_matrix()
        _sort_row = 2
        _matrix_labels = self._sorting_order_columns(m, byRow=_sort_row)
        v4_2_support.SortColumns(Matrix=m, byRow=_sort_row)
        _labels = self._get_labels_from_m_columns(m, byRow=_sort_row)
        
        self.assertTrue(_labels.difference(_matrix_labels) == set([]))
        print "test_SortColumns_byRow", _labels

    def test_SortColumns_byRow_invalid(self):

        m, x = make_matrix()

        _sort_row = 100

        with self.assertRaisesRegexp(IndexError, 'index out of range'):

            v4_2_support.SortColumns(Matrix=m, byRow=_sort_row)

        print "test_SortColumns_byRow_invalid", "_sort_row = ", _sort_row

    def test_SortColumns_usingCellValue(self):

        m, x = make_matrix()
        _usingCellValue = 0
        _matrix_labels = self._sorting_order_columns(
            m, usingCellValue=_usingCellValue)
        v4_2_support.SortColumns(Matrix=m, usingCellValue=_usingCellValue)
        _labels = self._get_labels_from_m_columns(
            m, usingCellValue=_usingCellValue)

        self.assertTrue(_labels.difference(_matrix_labels) == set([]))
        print "test_SortColumns_usingCellValue", _labels

    def test_SortColumns_usingCellValue_invalid(self):

        m, x = make_matrix()
        _usingCellValue = 3

        with self.assertRaisesRegexp(IndexError, 'index out of range'):
            v4_2_support.SortColumns(Matrix=m, usingCellValue=_usingCellValue)
        print "test_SortColumns_usingCellValue_invalid", _usingCellValue

    def test_SortColumns_descending(self):

        m, x = make_matrix()
        _descending = True
        _matrix_labels = self._sorting_order_columns(m, descending=_descending)
        v4_2_support.SortColumns(Matrix=m, descending=_descending)
        _labels = self._get_labels_from_m_columns(m, descending=_descending)

        self.assertTrue(_labels.difference(_matrix_labels) == set([]))
        print "test_SortColumns_descending", _labels

    def test_SortColumns_ascending(self):

        m, x = make_matrix()
        _descending = False
        _matrix_labels = self._sorting_order_columns(m, descending=_descending)
        v4_2_support.SortColumns(Matrix=m, descending=_descending)
        _labels = self._get_labels_from_m_columns(m, descending=_descending)

        self.assertTrue(_labels.difference(_matrix_labels) == set([]))
        print "test_SortColumns_ascending", _labels

    def test_SortColumns_with_all_options(self):

        m, x = make_matrix()
        _byRow = 2
        _usingCellValue = 0
        _descending = False
        _matrix_labels = self._sorting_order_columns(
            m, byRow=_byRow, usingCellValue=_usingCellValue,
            descending=_descending)
        v4_2_support.SortColumns(
            Matrix=m,
            byRow=_byRow,
            usingCellValue=_usingCellValue,
            descending=_descending)
        _labels = self._get_labels_from_m_columns(
            m, byRow=_byRow, usingCellValue=_usingCellValue,
            descending=_descending)

        self.assertTrue(_labels.difference(_matrix_labels) == set([]))
        print "test_SortColumns_with_all_options", _labels

    def test_BaseSummaryToSeriesHeadings(self):

        m, x = make_matrix()
        _matrix_labels = [r.Member.Label +
                          " (n=" + r[0][0].Value + ")" for r in m]
        v4_2_support.BaseSummaryToSeriesHeadings(Matrix=m)
        _labels = x.get_series_labels()
        
        self.assertEqual(_labels, _matrix_labels)
        print "test_BaseSummaryToSeriesHeadings = ", _matrix_labels

    def test_BaseSummaryToCategoryHeadings(self):

        m, x = make_matrix()
        _matrix_labels = [c.TopMember.Label +
                          " (n=" + c[0].Value + ")" for c in m[0]]
        v4_2_support.BaseSummaryToCategoryHeadings(Matrix=m)
        _labels = x.get_category_labels()

        self.assertEqual(_labels, _matrix_labels)
        print "test_BaseSummaryToCategoryHeadings = ", _matrix_labels

    def test_BaseSummaryToTableRows(self):

        m, x = make_matrix()
        _matrix_labels = ["(n=" + r[0][0].Value + ")" for r in m]
        v4_2_support.BaseSummaryToTableRows(Matrix=m)
        _labels = x.get_series_labels()

        self.assertEqual(_labels, _matrix_labels)
        print "test_BaseSummaryToTableRows = ", _matrix_labels

    def test_ColumnDifference(self):

        m, x = make_matrix()
        _matrix_data_values = list()
        for i in reversed(range(2, m.Count)):
            m.DeleteColumn(i)

        for r in m:
            for c in r:
                if c.Count != 0:
                    _matrix_data_values.append(c[0].Value)
                else:
                    _matrix_data_values.append("")
            _matrix_data_values.append(
                str((r[1][0].GetNumericValue() - r[0][0].GetNumericValue()) \
                    * 100))

        v4_2_support.ColumnDifference(0, 1, Matrix=m)
        _labels = x.get_data_values()

        self.assertEqual(_labels, _matrix_data_values)
        print "test_ColumnDifference = ", _matrix_data_values

    def test_RenumberSigTests(self):

        m, x = make_matrix()
        self._addStatsTestsToMatrix(m)
        v4_2_support.RenumberSigTests(Matrix=m)

        self.assertEqual(m[0][0].SigTestResult,
                         m.TopAxis.DataMembers[1].MemberSigTestHeading)
        heading = m.TopAxis.DataMembers[1].MemberSigTestHeading
        print "test_RenumberSigTests ", m[0][0].SigTestResult, heading             

    def test_TopNSummary_2(self):

        m, x = make_matrix()
        _labels = [r.Member.Label for r in m]
        _labels.append("Top 2")
        v4_2_support.TopNSummary(2, Matrix=m)
        _matrix_labels = x.get_series_labels()

        self.assertEqual(_labels, _matrix_labels)
        print "test_TopNSummary_2 = ", _matrix_labels

    def test_TopNSummary_3(self):

        m, x = make_matrix()
        _labels = [r.Member.Label for r in m]
        _labels.append("Top 3")
        v4_2_support.TopNSummary(3, Matrix=m)
        _matrix_labels = x.get_series_labels()
        
        self.assertEqual(_labels, _matrix_labels)
        print "test_TopNSummary_3 = ", _matrix_labels

    def test_NumberDownbreaks_dot(self):

        m, x = make_matrix()
        delimiter = "."
        _labels = [str(r.Member.DataIndex + 1) +
                   str(delimiter) + r.Member.Label for r in m]
        v4_2_support.NumberDownbreaks(delimiter, Matrix=m)
        _matrix_labels = x.get_series_labels()

        self.assertEqual(_labels, _matrix_labels)
        print "test_NumberDownbreaks_dot = ", _matrix_labels

    def test_NumberDownbreaks_blank(self):

        m, x = make_matrix()
        delimiter = ""

        _labels = [str(r.Member.DataIndex + 1) +
                   str(delimiter) + r.Member.Label for r in m]

        v4_2_support.NumberDownbreaks(delimiter, Matrix=m)

        _matrix_labels = x.get_series_labels()

        self.assertEqual(_labels, _matrix_labels)

        print "test_NumberDownbreaks_blank = ", _matrix_labels

    def test_NumberDownbreaks_slash(self):

        m, x = make_matrix()
        delimiter = "/"
        _labels = [str(r.Member.DataIndex + 1) +
                   str(delimiter) + r.Member.Label for r in m]
        v4_2_support.NumberDownbreaks(delimiter, Matrix=m)
        _matrix_labels = x.get_series_labels()

        self.assertEqual(_labels, _matrix_labels)
        print "test_NumberDownbreaks_slash = ", _matrix_labels

    def test_GetCsvVal(self):
        
        from System.IO import Path

        my_dir = Path.GetDirectoryName(__file__) # relative to the module file    
        file = my_dir + "\\transformations\\utils\\file_name.txt"
        x = v4_2_support.GetCsvVal(file, "myRow 1")
        self.assertEqual(x, ['Strongly Agree'])
        print "test_GetCSVVal = ", x

    def test_InsertColumn(self):

        m, x = make_matrix()
        _labels = [c.TopMember.Label for c in m[0]]
        _labels.insert(2, "new column 2")
        v4_2_support.InsertColumn(2, label="new column 2", Matrix=m)
        _matrix_labels = x.get_category_labels()

        self.assertEqual(_labels, _matrix_labels)
        print "test_InsertColumn", _matrix_labels

    def test_insert_category_too_big(self):

        m, x = make_matrix()
        _labels = [c.TopMember.Label for c in m[0]]
        v4_2_support.InsertColumn(40, label="this will fail", Matrix=m)
        _matrix_labels = x.get_category_labels()

        self.assertEqual(_labels, _matrix_labels)
        print "test_InsertColumn_too_big", _matrix_labels

    def test_InsertRow(self):

        m, x = make_matrix()
        _labels = [r.Member.Label for r in m]
        _labels.insert(2, "new row 2")
        v4_2_support.InsertRow(2, label="new row 2", Matrix=m)
        _matrix_labels = x.get_series_labels()

        self.assertEqual(_labels, _matrix_labels)
        print "test_InsertRow", _matrix_labels

    def test_InsertRow_too_big(self):

        m, x = make_matrix()
        _labels = [r.Member.Label for r in m]
        v4_2_support.InsertRow(40, label="this will fail", Matrix=m)
        _matrix_labels = x.get_series_labels()
        
        self.assertEqual(_labels, _matrix_labels)
        print "test_InsertRow_too_big", _matrix_labels

    # TODO These grid/merge scripts do not truly test the functions as the
    # selected table doesn't contain grid slices.
    # They are more fully tested in the manual pptx diff test.

    def test_UngroupRows(self):

        m, x = make_matrix()
        _labels = [r.Member.Label for r in m]
        v4_2_support.UngroupRows(Matrix=m)
        _matrix_labels = x.get_series_labels()

        self.assertEqual(_labels, _matrix_labels)
        print "test_UngroupRows = ", _matrix_labels

    def test_MergeRowsByLabel(self):

        m, x = make_matrix()
        _labels = [r.Member.Label for r in m]
        v4_2_support.MergeRowsByLabel(Matrix=m)
        _matrix_labels = x.get_series_labels()

        self.assertEqual(_labels, _matrix_labels)
        print "test_MergeRowsByLabel = ", _matrix_labels

    def test_MergeColumnsByLabel(self):

        m, x = make_matrix()
        _labels = [c.TopMember.Label for c in m[0] if
                   c.TopMember.Label != "Base"]
        v4_2_support.MergeColumnsByLabel(Matrix=m)
        _matrix_labels = x.get_category_labels()

        self.assertEqual(_labels, _matrix_labels)
        print "test_MergeColumnsByLabel = ", _matrix_labels

    def test_NumberStatementsInMatrix(self):

        m, x = make_matrix()
        delimiter = ". "
        _labels = [str(r.Member.DataIndex + 1) +
                   str(delimiter) + r.Member.Label for r in m]
        v4_2_support.NumberStatementsInMatrix(Matrix=m)
        _matrix_labels = x.get_series_labels()

        self.assertEqual(_labels, _matrix_labels)
        print "test_NumberStatementsInMatrix = ", _matrix_labels

    def test_SetMatrixLabelToStatement(self):
        
        m, x = make_matrix()
        _label = m[1].Member.Label
        v4_2_support.SetMatrixLabelToStatement(2, Matrix=m)

        self.assertEqual(_label, m.Label)
        print "test_SetMatrixLabelToStatement = ", m.Label


if __name__ == "__main__":

    unittest.main()
