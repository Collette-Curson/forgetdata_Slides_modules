'''
Updated 17th November 2016
@author: ccurson


###data MODULE TESTS

This set of regression tests will test all of the functions within the
"auto_fill_matrix" module installed with Slides.

This class is to be used for other data formats, eg pandas, so if slidesconf.py
cannot be imported, ie slides not present, then it will create a test matrix
using make_fake_matrix.py from matrixfuncs.

Also to be run using Matrix created using Slides.

See $RepSuite\Releases\4.3\Forgetdata\Libraries\Lib\forgetdata\Scripts\transformations package.

'''

########Variables that can be reset when running this test###############
use_test_data = True

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
import utils.utilities as utilities
import utils.matrixfuncs as matrixfuncs

def _make_matrix(table_selected=0):
    """make a matrix either from test_matrix or by connecting to Slides."""
    import transformations as tr  #this imports category, category, data, text, pptx_data
    import transformations.auto_fill_matrix as autofill
        
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
    fill = autofill.FillMatrix(m)
    
    for c in m[0]:
        c.TopMember.Label = c.TopMember.Label.encode('ascii','ignore')
    return m,x

class Test(TestCase):
    """Class for unit testing category module from the transformations package.
    m is a matrix created from a list of lists or is a Slides Matrix - defined by 
    
    """    
        
    #########################################################
    #Start of regression tests for transformations package  #
    #########################################################
       
    def test_auto_fill_rows_default(self):
        m,fill = _make_matrix()
        
        _matrix_labels = self._sorting_order_rows(m, by_column =_sort_col, using_cell_value = 0)
        fill.auto_fill_matrix()
        _labels = self._get_labels_from_m_rows(m, by_column = _sort_col)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_rows_default", _labels
        #utilities.print_matrix(m)
        
    
    def test_sort_rows_by_column(self):
        m,x = _make_matrix()
        _sort_col = 2
        _matrix_labels = self._sorting_order_rows(m, by_column =_sort_col, using_cell_value = 0)
        x.sort_rows(by_column =_sort_col)
        _labels = self._get_labels_from_m_rows(m, by_column =_sort_col)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_rows_by_column", _labels            
    
    def test_sort_rows_by_column_invalid(self):
        m,x = _make_matrix()
        _sort_col = 100
        with self.assertRaisesRegexp(IndexError, 'index out of range'):
            x.sort_rows(by_column=_sort_col)
        print "test_sort_rows_by_column_invalid", "_sort_col = ", _sort_col
    
    def test_sort_rows_using_cell_value(self):
        m,x = _make_matrix()
        _using_cell_value = 0
        _matrix_labels = self._sorting_order_rows(m, by_column = 0, using_cell_value = _using_cell_value)
        x.sort_rows(using_cell_value = _using_cell_value)
        _labels = self._get_labels_from_m_rows(m, using_cell_value = _using_cell_value)    
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))        
        print "test_sort_rows_using_cell_value", _labels
        
    def test_sort_rows_using_cell_value_invalid(self):
        m,x = _make_matrix()
        _using_cell_value = 3
        with self.assertRaisesRegexp(IndexError, 'index out of range'):
            x.sort_rows(using_cell_value = _using_cell_value)            
        print "test_sort_rows_using_cell_value_invalid", "_using_cell_value = ", _using_cell_value
            
    def test_sort_rows_descending(self):
        m,x = _make_matrix()
        _descending = True
        _matrix_labels = self._sorting_order_rows(m, descending = _descending)
        x.sort_rows(descending = _descending)
        _labels = self._get_labels_from_m_rows(m, descending = _descending)        
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_rows_descending", _labels
            
    def test_sort_rows_ascending(self):    
        m,x = _make_matrix()
        _descending = False
        _matrix_labels = self._sorting_order_rows(m, descending = _descending)
        x.sort_rows(descending = _descending)
        _labels = self._get_labels_from_m_rows(m, descending = _descending)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_rows_ascending", _labels        
    
    def test_sort_rows_file_name(self):
        m,x = _make_matrix()
        _file_name = "utils\\file_name.txt"
        _matrix_labels = self._sorting_order_rows(m, file_name = _file_name)
        x.sort_rows(file_name = _file_name)
        _labels = self._get_labels_from_m_rows(m, file_name = _file_name)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_rows_file_name", _labels        
    
    def test_sort_rows_filename_invalid(self):
        m,x = _make_matrix()
        _file_name = "file_name.txt"
        _matrix_labels = self._sorting_order_rows(m, file_name = _file_name)
        x.sort_rows(file_name = _file_name)
        _labels = self._get_labels_from_m_rows(m, file_name = _file_name)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_rows_filename_invalid", _labels        
    
    def test_sort_rows_filename_blank(self):
        m,x = _make_matrix()
        _file_name = "utils\\file_name_blank.txt"
        _matrix_labels = self._sorting_order_rows(m, file_name = _file_name)
        x.sort_rows(file_name = _file_name)
        _labels = self._get_labels_from_m_rows(m, file_name = _file_name)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))        
        print "test_sort_rows_filename_blank", _labels            
    
    def test_sort_rows_with_client_name_first(self):
        m,x = _make_matrix()
        if use_test_data == True:
            _client_name = "myRow 2"
        else:
            _client_name = "Somewhat Agree"
        x.sort_rows(client_name = _client_name)
        _matrix_labels = self._sorting_order_rows(m, by_column = 0, using_cell_value = 0, descending = True, file_name = None, client_name = _client_name)
        _labels = self._get_labels_from_m_rows(m, client_name = _client_name)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))        
        print "test_sort_rows_with_client_name_first", _labels        
    
    def test_sort_rows_with_client_name_first_invalid(self):
        m,x = _make_matrix()
        _client_name = "XXX"
        x.sort_rows(client_name = _client_name)
        _matrix_labels = self._sorting_order_rows(m, by_column = 0, using_cell_value = 0, descending = True, file_name = None, client_name = _client_name)
        _labels = self._get_labels_from_m_rows(m, client_name = _client_name)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))      
        print "test_sort_rows_with_client_name_first_invalid", _labels 
    
    def test_sort_rows_with_all_options(self):
        m,x = _make_matrix()
        _by_column = 2
        _using_cell_value = 0
        _descending = False
        _file_name = "utils\\file_name.txt"
        if use_test_data == True:
            _client_name = "myRow 2"
        else:
            _client_name = "Somewhat Agree"
        _matrix_labels = self._sorting_order_rows(m, by_column = _by_column, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        x.sort_rows(by_column = _by_column, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        _labels = self._get_labels_from_m_rows(m, by_column = _by_column, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        utilities.print_matrix(m)
        print "_labels", _labels
        print "_matrix_labels", _matrix_labels
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_rows_with_all_options", _labels 
        
    #add tests for sort rows with nets
    def test_sort_rows_nets_default(self):
        global mtd_filepath
        mtd_filepath = os.path.abspath(os.path.join('utils\\SmokeTest_v3.mtd'))
        
        table_selected = 86 

        print ""
        print "This regression test is run using DATA Containing Nets"
        print ""

        m,x = _make_matrix(table_selected=table_selected)
        _sort_col = 0
        _using_cell_value = 0
        _descending = True
        _file_name = None
        _client_name = None
        _matrix_labels = self._sorting_order_rows(m, by_column =_sort_col, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        x.sort_rows(m, by_column =_sort_col, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        _labels = self._get_labels_from_m_rows(m, by_column = _sort_col, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        #print "test_sort_rows_default", _labels
        #print "_matrix_labels", _matrix_labels
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_rows_nets_default", _labels 
        #utilities.print_matrix(m)
        
    def test_sort_rows_nets_bycolumn_ascending(self):
        global mtd_filepath
        mtd_filepath = os.path.abspath(os.path.join('utils\\SmokeTest_v3.mtd'))
        
        table_selected = 86 

        print ""
        print "This regression test is run using DATA Containing Nets"
        print ""

        m,x = _make_matrix(table_selected=table_selected)
        _sort_col = 1
        _using_cell_value = 0
        _descending = False
        _file_name = None
        _client_name = None
        _matrix_labels = self._sorting_order_rows(m, by_column =_sort_col, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        x.sort_rows(m, by_column =_sort_col, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        _labels = self._get_labels_from_m_rows(m, by_column = _sort_col, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        #print "test_sort_rows_default", _labels
        #print "_matrix_labels", _matrix_labels
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_rows_nets_bycolumn_ascending", _labels 
        utilities.print_matrix(m)
            
    def test_sort_rows_nets_file_name(self):
        global mtd_filepath
        mtd_filepath = os.path.abspath(os.path.join('utils\\SmokeTest_v3.mtd'))
        
        table_selected = 86 

        print ""
        print "This regression test is run using DATA Containing Nets"
        print ""

        m,x = _make_matrix(table_selected=table_selected)
        _sort_col = 0
        _using_cell_value = 0
        _descending = True
        _file_name = "utils\\filename.txt"
        _client_name = None
        _matrix_labels = self._sorting_order_rows(m, by_column =_sort_col, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        x.sort_rows(m, by_column =_sort_col, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        _labels = self._get_labels_from_m_rows(m, by_column = _sort_col, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        #print "test_sort_rows_default", _labels
        #print "_matrix_labels", _matrix_labels
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_rows_nets_file_name", _labels 
        utilities.print_matrix(m)

    def test_sort_rows_nets_client_name(self):
        global mtd_filepath
        mtd_filepath = os.path.abspath(os.path.join('utils\\SmokeTest_v3.mtd'))
        
        table_selected = 86 

        print ""
        print "This regression test is run using DATA Containing Nets"
        print ""

        m,x = _make_matrix(table_selected=table_selected)
        _sort_col = 0
        _using_cell_value = 0
        _descending = True
        _file_name = None
        _client_name = "No opinion (3)"
        _matrix_labels = self._sorting_order_rows(m, by_column =_sort_col, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        x.sort_rows(m, by_column =_sort_col, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        _labels = self._get_labels_from_m_rows(m, by_column = _sort_col, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        #print "test_sort_rows_default", _labels
        #print "_matrix_labels", _matrix_labels
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_rows_nets_client_name", _labels 
        utilities.print_matrix(m)
        
    #end of nets tests
    
    def test_sort_columns_default(self):
        m,x = _make_matrix()
        _sort_row = 0
        x.sort_columns()
        _matrix_labels = self._sorting_order_columns(m, by_row =_sort_row)
        _labels = self._get_labels_from_m_columns(m, by_row =_sort_row)        
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_columns_default", _labels
    
    def test_sort_columns_by_row(self):
        m,x = _make_matrix()
        _sort_row = 2
        x.sort_columns(by_row =_sort_row)
        _matrix_labels = self._sorting_order_columns(m, by_row =_sort_row)
        _labels = self._get_labels_from_m_columns(m, by_row =_sort_row)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_columns_by_row", _labels            
    
    def test_sort_columns_by_row_invalid(self):
        m,x = _make_matrix()
        _sort_row = 100
        with self.assertRaisesRegexp(IndexError, 'index out of range'):
            x.sort_columns(by_row=_sort_row)
        print "test_sort_columns_by_row_invalid", "_sort_row = ", _sort_row
    
    def test_sort_columns_using_cell_value(self):
        m,x = _make_matrix()
        _using_cell_value = 0
        x.sort_columns(using_cell_value = _using_cell_value)
        _matrix_labels = self._sorting_order_columns(m, using_cell_value = _using_cell_value)
        _labels = self._get_labels_from_m_columns(m, using_cell_value = _using_cell_value)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_columns_using_cell_value", _labels
        
    def test_sort_columns_using_cell_value_invalid(self):
        m,x = _make_matrix()
        _using_cell_value = 3
        with self.assertRaisesRegexp(IndexError, 'index out of range'):
            x.sort_columns(using_cell_value = _using_cell_value)
        print "test_sort_columns_using_cell_value_invalid", "_using_cell_value = ", _using_cell_value
            
    def test_sort_columns_descending(self):
        m,x = _make_matrix()
        _descending = True
        x.sort_columns(descending = _descending)
        _matrix_labels = self._sorting_order_columns(m, descending = _descending)
        _labels = self._get_labels_from_m_columns(m, descending = _descending)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_columns_descending", _labels
           
    def test_sort_columns_ascending(self):    
        m,x = _make_matrix()
        utilities.print_matrix(m)
        _descending = False
        x.sort_columns(descending = _descending)
        _matrix_labels = self._sorting_order_columns(m, descending = _descending)
        _labels = self._get_labels_from_m_columns(m, descending = _descending)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_columns_ascending", _labels
    
    def test_sort_columns_file_name(self):
        m,x = _make_matrix()
        _file_name = "utils\\file_name.txt"
        x.sort_columns(file_name = _file_name)
        _matrix_labels = self._sorting_order_columns(m, file_name = _file_name)
        _labels = self._get_labels_from_m_columns(m, file_name = _file_name)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_columns_file_name", _labels        
    
    def test_sort_columns_filename_invalid(self):
        m,x = _make_matrix()
        _file_name = "file_name.txt"
        x.sort_columns(file_name = _file_name)
        _matrix_labels = self._sorting_order_columns(m, file_name = _file_name)
        _labels = self._get_labels_from_m_columns(m, file_name = _file_name)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))        
        print "test_sort_columns_filename_invalid", _labels        
    
    def test_sort_columns_filename_blank(self):
        m,x = _make_matrix()
        _file_name = "utils\\file_name_blank.txt"
        x.sort_columns(file_name = _file_name)
        _matrix_labels = self._sorting_order_columns(m, file_name = _file_name)
        _labels = self._get_labels_from_m_columns(m, file_name = _file_name)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))        
        print "test_sort_columns_filename_blank", _labels        
    
    def test_sort_columns_with_client_name_first(self):
        m,x = _make_matrix()
        if use_test_data == True:
            _client_name = "myColumn 2"
        else:
            _client_name = "Male"
        x.sort_columns(client_name =_client_name)
        _matrix_labels = self._sorting_order_columns(m, by_row = 0, using_cell_value = 0, descending = True, file_name = None, client_name = _client_name)
        _labels = self._get_labels_from_m_columns(m, client_name = _client_name)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))        
        print "test_sort_columns_with_client_name_first", _labels        
    
    def test_sort_columns_with_client_name_first_invalid(self):
        m,x = _make_matrix()
        _client_name = "XXX"
        x.sort_columns(client_name =_client_name)
        _matrix_labels = self._sorting_order_columns(m, by_row = 0, using_cell_value = 0, descending = True, file_name = None, client_name = _client_name)
        _labels = self._get_labels_from_m_columns(m, client_name = _client_name)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))        
        print "test_sort_columns_with_client_name_first_invalid", _labels 
    
    def test_sort_columns_with_all_options(self):
        m,x = _make_matrix()
        _by_row = 2
        _using_cell_value = 0
        _descending = False
        _file_name = "utils\\file_name.txt"
        if use_test_data == True:
            _client_name = "myColumn 2"
        else:
            _client_name = "Male"
        _matrix_labels = self._sorting_order_columns(m, by_row = _by_row, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        x.sort_columns(by_row = _by_row, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        _labels = self._get_labels_from_m_columns(m, by_row = _by_row, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_columns_with_all_options", _labels  
    
    #add tests for sort columns with nets (note these columns do not contain nets!)
    def test_sort_columns_nets_default(self):
        global mtd_filepath
        mtd_filepath = os.path.abspath(os.path.join('utils\\SmokeTest_v3.mtd'))
        
        table_selected = 86 

        print ""
        print "This regression test is run using DATA Containing Nets"
        print ""

        m,x = _make_matrix(table_selected=table_selected)
        _sort_row = 0
        _using_cell_value = 0
        _descending = True
        _file_name = None
        _client_name = None
        _matrix_labels = self._sorting_order_columns(m, by_row =_sort_row, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        x.sort_columns(m, by_row =_sort_row, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        _labels = self._get_labels_from_m_columns(m, by_row =_sort_row, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_columns_nets_default", _labels 
        utilities.print_matrix(m)
        
    def test_sort_columns_nets_bycolumn_ascending(self):
        global mtd_filepath
        mtd_filepath = os.path.abspath(os.path.join('utils\\SmokeTest_v3.mtd'))
        
        table_selected = 86 

        print ""
        print "This regression test is run using DATA Containing Nets"
        print ""

        m,x = _make_matrix(table_selected=table_selected)
        _sort_row = 4
        _using_cell_value = 0
        _descending = False
        _file_name = None
        _client_name = None
        _matrix_labels = self._sorting_order_columns(m, by_row = _sort_row, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        x.sort_columns(m, by_row = _sort_row, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        _labels = self._get_labels_from_m_columns(m, by_row = _sort_row, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_columns_nets_bycolumn_ascending", _labels 
        utilities.print_matrix(m)
            
    def test_sort_columns_nets_file_name(self):
        global mtd_filepath
        mtd_filepath = os.path.abspath(os.path.join('utils\\SmokeTest_v3.mtd'))
        
        table_selected = 86 

        print ""
        print "This regression test is run using DATA Containing Nets"
        print ""

        m,x = _make_matrix(table_selected=table_selected)
        _sort_row = 0
        _using_cell_value = 0
        _descending = True
        _file_name = "utils\\filename.txt"
        _client_name = None
        _matrix_labels = self._sorting_order_columns(m, by_row =_sort_row, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        x.sort_columns(m, by_row =_sort_row, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        _labels = self._get_labels_from_m_columns(m, by_row =_sort_row, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        print "test_sort_columns_default", _labels
        print "_matrix_labels", _matrix_labels
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_columns_nets_file_name", _labels 
        utilities.print_matrix(m)

    def test_sort_columns_nets_client_name(self):
        global mtd_filepath
        mtd_filepath = os.path.abspath(os.path.join('utils\\SmokeTest_v3.mtd'))
        
        table_selected = 86 

        print ""
        print "This regression test is run using DATA Containing Nets"
        print ""

        m,x = _make_matrix(table_selected=table_selected)
        _sort_row = 0
        _using_cell_value = 0
        _descending = True
        _file_name = None
        _client_name = "25-34 years"
        _matrix_labels = self._sorting_order_columns(m, by_row =_sort_row, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        x.sort_columns(m, by_row =_sort_row, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        _labels = self._get_labels_from_m_columns(m, by_row =_sort_row, using_cell_value = _using_cell_value, descending = _descending, file_name = _file_name, client_name = _client_name)
        #print "test_sort_columns_default", _labels
        #print "_matrix_labels", _matrix_labels
        self.assertTrue(_labels.difference(_matrix_labels)  == set([]))
        print "test_sort_rows_nets_client_name", _labels 
        utilities.print_matrix(m)
        
    #end of nets tests
    
if __name__ == "__main__":
    unittest.main()