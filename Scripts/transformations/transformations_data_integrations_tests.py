'''
Updated 14th Jan 2016
@author: ccurson


###data MODULE TESTS

This set of regression tests will test all of the functions within the
"data" module of the transformations package installed with Slides.

This class is to be used for other data formats, eg pandas, so run these without the 
matrixfuncs.py to generate the Matrix from a List.

Also to be run using Matrix created using Slides.

See $RepSuite\Releases\4.3\Forgetdata\Libraries\Lib\forgetdata\Scripts\transformations package.

'''
#import matrixfuncs

########Variables that can be reset when running this test###############
use_test_data = False

#Real data only used when use_test_data == False. 
import os
mtd_filepath = os.path.abspath(os.path.join('utils\\Master Demo 2010.mtd'))

table_selected = 0 # table within mtd file used for tests when use_test_data==False
#table_selected = 86 # table within mtd file used for tests when use_test_data==False

if use_test_data == True:
    print ""
    print "This regression test is run using TEST DATA"
    print ""
else:
    print ""
    print "This regression test is run using SLIDES! DATA"
    print ""
#########################################################################

from unittest import (TestCase, main)
import utils.matrixfuncs as matrixfuncs
import utils.utilities as utilities

def _make_matrix(table_selected=0):
    """make a matrix either from test_matrix or by connecting to Slides."""
    import transformations as tr  #this imports category, category, data, text, pptx_data
        
    if use_test_data == True:
        #make a teste matrix using create_test_matrix
        m = matrixfuncs.create_test_matrix()
    else:  
        #make a matrix by connecting to Slides! and connecting to a data table.
        import utils.slidesconf as slidesconf
            
        from Forgetdata.Matrix import ConnectionDefinition
        conn = ConnectionDefinition()
        conn.ConnectionString = mtd_filepath #set at top of file
        conn.Name =  "Test"
        conn.Provider =  "SPSS MTD File"
        liveConnection = slidesconf.connect(conn.ConnectionString,name=conn.Name,provider_name=conn.Provider)
        m = liveConnection[table_selected]
        
        print "connected table: ", m.Label    
    x=tr.MatrixManipulator(m)
    #utilities.print_matrix(m)
    #print ""
    
    for c in m[0]:
        c.TopMember.Label = c.TopMember.Label.encode('ascii','ignore')
    return m,x

class Test(TestCase):
    """Class for unit testing category module from the transformations package.
    m is a matrix created from a list of lists or is a Slides Matrix - defined by 
    
    """
    
    def _addStatsHeadersToMatrix(self,m):
        """This will add stats test headers into the Matrix."""
        
        atoz = "JKLMNOPQRSTUVWXYZABCDEFGHI"
        counter=0
        for col in m.TopAxis.DataMembers:
            if counter < 26:
                logicalletter = str(atoz[counter])
                col.MemberSigTestHeading = logicalletter
                counter += 1
            else: counter = 0

    def _addStatsTestsToMatrix(self,m):
        """This will add stats test headers and results into the Matrix."""
        
        #add stat letters to columns
        self._addStatsHeadersToMatrix(m)

        #add stat results to cells
        for row in m:
            for cell in row:
                #set the stat result to be the same as the next column's stat heading
                try:
                    cell.SigTestResult = m.TopAxis.DataMembers[cell.TopMember.DataIndex+1].MemberSigTestHeading
                except:
                    cell.SigTestResult = m.TopAxis.DataMembers[0].MemberSigTestHeading
                cell.AddValue(cell.SigTestResult,None)

    #########################################################
    #Start of regression tests for transformations package  #
    #########################################################
                
    def test_get_data_values(self):
        m,x =  _make_matrix()
        _matrix_data_values = list()
        for r in m:
            for c in r:
                if c.Count != 0:
                    _matrix_data_values.append(c[0].Value)
                else:
                    _matrix_data_values.append("")
        _data_values = x.get_data_values()
        self.assertEqual(_data_values,_matrix_data_values)
        print "test_get_data_values = ", _matrix_data_values
        
    def test_get_data_values_failure(self):
        m,x =  _make_matrix()
        _matrix_data_values = list()
        for r in m:
            for c in r:
                if c.Count != 0:
                    _matrix_data_values.append(c[0].Value)
                else:
                    _matrix_data_values.append("")
        m[0][0].RemoveValueAt(0)
        _data_values = x.get_data_values()
        with self.assertRaises(AssertionError): 
            self.assertEqual(_data_values,_matrix_data_values)
        print "test_get_data_values_failure = ", _matrix_data_values
    
    def test_get_base_row_values(self):
        m,x =  _make_matrix()
        if use_test_data == True:
            m[0].Member.Label = "Base"
        _base_labels = ["Base", "Total"]
        _labels = x.get_base_row_values()
        _tmp = [str(c[0].Value) for r in m for c in r if r.Member.Label in _base_labels]
        _matrix_labels = ", ".join(_tmp)
        self.assertEqual(_labels,_matrix_labels)
        print "test_get_base_row_values = ", _matrix_labels
        
    def test_get_base_row_values_failure(self):
        m,x =  _make_matrix()
        if use_test_data == True:
            m[0].Member.Label = "Base"
        _base_labels = ["Base", "Total"]
        _tmp = [str(c[0].Value) for r in m for c in r if r.Member.Label in _base_labels]
        _matrix_labels = ", ".join(_tmp)
        #introduce error scenario
        m[0][0].RemoveValueAt(0)
        with self.assertRaisesRegexp(Exception, 'Index was out of range'):
            _labels = x.get_base_row_values()
            self.assertEqual(_labels,_matrix_labels)
        print "test_get_base_row_values_failure = ", _matrix_labels
                
    def test_get_base_column_values(self):
        m,x =  _make_matrix()
        if use_test_data == True:
            m[0][0].TopMember.Label = "Base"
        _base_labels = ["Base", "Total"]
        _tmp = [str(c[0].Value) for r in m for c in r if c.TopMember.Label in _base_labels]
        _matrix_labels = ", ".join(_tmp)
        _labels = x.get_base_column_values()
        self.assertEqual(_labels,_matrix_labels)
        print "test_get_base_column_values = ", _matrix_labels
        
    def test_get_base_column_values_failure(self):
        m,x =  _make_matrix()
        if use_test_data == True:
            m[0][0].TopMember.Label = "Base"
        _base_labels = ["Base", "Total"]
        _tmp = [str(c[0].Value) for r in m for c in r if c.TopMember.Label in _base_labels]
        _matrix_labels = ", ".join(_tmp)
        #introduce error scenario
        m[0][0].RemoveValueAt(0)        
        with self.assertRaisesRegexp(Exception, 'Index was out of range'):
            _labels = x.get_base_column_values()
            self.assertEqual(_labels,_matrix_labels)
        print "test_get_base_column_values_failure = ", _matrix_labels

    def test_get_dict_cell_values(self):
        m,x =  _make_matrix()
        _matrix_dict = dict()
        for r in m:
            row_dict = dict()
            for c in r:
                vals=list()
                for v in c:
                    vals.append(v.Value)
                row_dict[c.TopMember.Label + " " + str(c.TopMember.Group.SortIndex)] = vals
            _matrix_dict[r.Member.Label + " " + str(r.Member.Group.SortIndex)] = row_dict
        _labels = x.get_dict_cell_values()
        side_label = m[0].Member.Label + " " + str(m[0].Member.Group.SortIndex)
        top_label = m[0][0].TopMember.Label + " " + str(m[0][0].TopMember.Group.SortIndex)
        self.assertEqual(_labels[side_label][top_label], _matrix_dict[side_label][top_label])
        print "test_get_dict_cell_values",_labels[side_label][top_label],  _matrix_dict[side_label][top_label]
        
    def test_get_dict_cell_values_failure(self):
        m,x =  _make_matrix()
        _matrix_dict = dict()
        for r in m:
            row_dict = dict()
            for c in r:
                vals=list()
                for v in c:
                    vals.append(v.Value)
                row_dict[c.TopMember.Label + " " + str(c.TopMember.Group.SortIndex)] = vals
            _matrix_dict[r.Member.Label + " " + str(m[0].Member.Group.SortIndex)] = row_dict        
        for r in m:
            for c in r:
                c.AddValue("10%",None)
        _labels = x.get_dict_cell_values()
        side_label = m[0].Member.Label + " " + str(m[0].Member.Group.SortIndex)
        top_label = m[0][0].TopMember.Label + " " + str(m[0][0].TopMember.Group.SortIndex)
        with self.assertRaises(AssertionError): 
            self.assertEqual(_labels[side_label][top_label], _matrix_dict[side_label][top_label])
        print "test_get_dict_cell_values_failure",_labels[side_label][top_label],  _matrix_dict[side_label][top_label]
        
    def test_set_data_formatted_labels_default(self):
        m,x =  _make_matrix()
        _matrix_labels = [c[0].Value for r in m for c in r]
        x.set_data_formatted_labels()
        _labels = x.get_data_values()
        self.assertEqual(_labels,_matrix_labels)
        print "test_set_data_formatted_labels_default = ", _matrix_labels
    
    def test_set_data_formatted_labels_side_top(self):
        m,x =  _make_matrix()
        _matrix_labels = [c[0].Value + " " + c.SideMember.Label if c[0].GetNumericValue() is not None else "-" for r in m for c in r]
        x.set_data_formatted_labels(cell_format = "{0[0].Value} {0.SideMember.Label}")
        _labels = x.get_data_values()
        self.assertEqual(_labels,_matrix_labels)
        print "test_set_data_formatted_labels_side_top = ", _matrix_labels
    
    def test_set_data_formatted_labels_bad(self):
        m,x =  _make_matrix()
        _matrix_labels = [c[0].Value + " - " + c.SideMember.Group.Label + " : " + c.SideMember.Label if c[0].GetNumericValue() is not None else "-" for r in m for c in r]
        with self.assertRaisesRegexp(AttributeError, 'CDataCell'):
            x.set_data_formatted_labels(cell_format = "{0[0].Value} - {0.Group.Label} : {0.Label}")
            _labels = x.get_data_values()   
            self.assertEqual(_labels,_matrix_labels)
        print "test_set_data_formatted_labels_bad = AttributeError: 'CDataCell' does not contain 'Group'"
    
    def test_category_difference(self):
        m,x =  _make_matrix()
        a=1
        b=2
        x.category_difference(a,b)
        shift = m[0][b][0].GetNumericValue() - m[0][a][0].GetNumericValue()
        shift_compare = str(int(shift))
        self.assertEqual(m[0][b+1][0].Value, shift_compare)
        print "test_category_difference = -2, ", shift_compare
        
    def test_category_difference_failure(self):
        m,x =  _make_matrix()
        a=1
        b=2
        shift = m[0][b][0].GetNumericValue() - m[0][a][0].GetNumericValue()
        shift_compare = str(int(shift))
        #introduce failure
        m[0][b].RemoveValueAt(0)
        x.category_difference(a,b)
        with self.assertRaises(AssertionError):
            self.assertEqual(m[0][b+1][0].Value, shift_compare)
        print "test_category_difference_failure = -2, ", shift_compare
    
    def test_renumber_sig_tests(self):
        m,x = _make_matrix()
        self._addStatsTestsToMatrix(m)
        x.renumber_sig_tests()
        self.assertEqual(m[0][0].SigTestResult, m.TopAxis.DataMembers[1].MemberSigTestHeading)
        print "test_renumber_sig_tests ", m[0][0].SigTestResult, m.TopAxis.DataMembers[1].MemberSigTestHeading
        
    def test_renumber_sig_tests_remove_column(self):
        m,x = _make_matrix()
        self._addStatsTestsToMatrix(m)
        m.DeleteColumn(0)
        x.renumber_sig_tests()
        self.assertEqual(m[0][0].SigTestResult, m.TopAxis.DataMembers[1].MemberSigTestHeading)
        print "test_renumber_sig_tests_remove_column ", m[0][0].SigTestResult, m.TopAxis.DataMembers[1].MemberSigTestHeading
    
    def test_renumber_sig_tests_too_many_cols(self):
        m,x = _make_matrix()
        #_cols=m.TopAxis.DataMembers
        for i in range(0,32): #generate lots of columns
            newcol=m.InsertBlankColumnAfter(m.TopAxis.DataMembers[0],"test","test")
        
        self._addStatsTestsToMatrix(m)
        with self.assertRaisesRegexp(Exception, 'index out of range'):
            x.renumber_sig_tests()
        print "test_renumber_sig_tests_too_many_cols - should not match: ", m[0][0].SigTestResult, m.TopAxis.DataMembers[1].MemberSigTestHeading
    
    def test_renumber_sig_tests_no_stats_results_found(self):
        m,x = _make_matrix()   
        self._addStatsHeadersToMatrix(m) 
        x.renumber_sig_tests(True)
        self.assertEqual(m[0][0].SigTestResult, "")
        print "test_renumber_sig_tests_no_stats_results_found (blank) ", m[0][0].SigTestResult
                    
    def test_renumber_sig_tests_no_stats(self):
        m,x = _make_matrix()    
        x.renumber_sig_tests(True)
        self.assertEqual(m[0][0].SigTestResult, "")
        print "test_renumber_sig_tests_no_stats (blank) ", m[0][0].SigTestResult
     
    def test_convert_significance_results_to_arrows(self):
        m,x = _make_matrix()
        self._addStatsTestsToMatrix(m)
        x.convert_significance_results_to_arrows()
        utilities.print_matrix(m)
        self.assertEqual(m[0][0].SigTestResult, u'\xea')
        print "test_convert_significance_results_to_arrows ", m[0][0].SigTestResult
        
    def test_convert_significance_results_to_arrows_no_stats_results_found(self):
        m,x = _make_matrix()
        self._addStatsHeadersToMatrix(m)
        x.convert_significance_results_to_arrows()
        self.assertEqual(m[0][0].SigTestResult, u'')
        print "test_convert_significance_results_to_arrows_no_stats_results_found (blank)", m[0][0].SigTestResult
        
    def test_convert_significance_results_to_arrows_no_stats(self):
        m,x = _make_matrix()
        x.convert_significance_results_to_arrows()
        self.assertEqual(m[0][0].SigTestResult, u'')
        print "test_convert_significance_results_to_arrows_no_stats (blank): ", m[0][0].SigTestResult    
    
    def test_clone_matrix(self):
        m,x = _make_matrix()
        clone_matrix = x.clone_matrix()
        _data_values = x.get_data_values()
        _labels = x.get_series_labels() 
        _matrix_data_values = list()
        for r in m:
            for c in r:
                if c.Count != 0:
                    _matrix_data_values.append(c[0].Value)
                else:
                    _matrix_data_values.append("")
        _matrix_labels = [row.Member.Label for row in m]
        self.assertEqual(_labels,_matrix_labels)
        print "test_clone_matrix (labels) = ", _matrix_labels
        self.assertEqual(_data_values,_matrix_data_values)
        print "test_clone_matrix (data)= ", _matrix_data_values
    
    #TODO These grid/merge scripts do not truly test the functions as the 
    #selected table doesn't contain grid slices.
    #They are more fully tested in the manual pptx diff test.
    def test_make_series_from_grid_slices(self):
        m,x = _make_matrix()
        _labels = [r.Member.Label for r in m]
        x.make_series_from_grid_slices()
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_make_series_from_grid_slices = ", _matrix_labels
    
    def test_merge_series_by_label(self):
        m,x = _make_matrix()
        _labels = [r.Member.Label for r in m]
        x.merge_series_by_label()
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_merge_series_by_label = ", _matrix_labels
    
    def test_merge_categories_by_label(self):
        m,x = _make_matrix()
        #remove multiple Base columns if concatenated
        _labels = [c.TopMember.Label for c in m[0] if 
                   c.TopMember.Label != "Base"]
        #Add one single Base, if Base existed.
        if m[0][0].TopMember.Label == "Base": 
            _labels.insert(0, "Base")
            
        x.merge_categories_by_label()
        _matrix_labels = x.get_category_labels()
        
        self.assertEqual(_labels,_matrix_labels)
        print "test_merge_categories_by_label = ", _matrix_labels

    
if __name__ == "__main__":
    unittest.main()