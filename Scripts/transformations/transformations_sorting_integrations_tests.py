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
import utils.utilities as utilities
import utils.matrixfuncs as matrixfuncs

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
    
    def _rank_position(self, _lst_incl_cells):
        """Used by sorting functions for testing the order within a table, 
        returns a set as columns can have equal rank, so order cannot be used.
        
        """
        
        counter = 0
        previous_val = 0
        _new_set = set()
        for item in _lst_incl_cells:
            if item != "":
                _val = item.split(" ",1)
                if _val[0] != previous_val:
                    counter += 1
                
                _new_set.add((counter,_val[1]))
                previous_val = _val[0]
        return _new_set
   
    def _sorted_nicely(self,l):
        """Sort numerically, exclude non numeric results from the sort """
        
        import re  
        convert = lambda text: int(text) if text.isdigit() else "" 
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
        
        return sorted(l, key = alphanum_key)
        
    def _sorting_order_rows(self,m, by_column = 0 ,using_cell_value = 0, descending = True, file_name = None, client_name = None):
        """Sort matrix into the sorted order without using sort functions. 
        Get rank position to calculate if the output is correct.
        
        """
            
        def _get_list_without_excluded_items(client_name,_keep_at_end):
            if len(_keep_at_end)> 0:
                return [str(r[by_column][using_cell_value].Value) + " " + str(r.Member.Label) for r in m if not r.Member.Label in _keep_at_end]
            elif client_name is not None:
                return [str(r[by_column][using_cell_value].Value) + " " + str(r.Member.Label) for r in m if  r.Member.Label != client_name]
            else:
                return [str(r[by_column][using_cell_value].Value) + " " + str(r.Member.Label) for r in m]
            
        _keep_at_end = self._get_keep_at_end(file_name)
        
        
        _lst = _get_list_without_excluded_items(client_name,_keep_at_end)
        #reverse the list to make ascending order
        if descending == True:
            _lst_incl_cells = list(reversed(self._sorted_nicely(_lst)))
        else:
            _lst_incl_cells = list(self._sorted_nicely(_lst))
    
        return self._rank_position(_lst_incl_cells)  
    
    def _sorting_order_columns(self, m, by_row = 0, using_cell_value = 0, descending = True, file_name = None, client_name = None):
        """Sort matrix into the sorted order without using sort functions. 
        Get rank position to calculate if the output is correct.
        
        """
            
        def _get_list_without_excluded_items(client_name,_keep_at_end):
            if _keep_at_end != []:
                return [str(c[using_cell_value].Value) + " " + str(c.TopMember.Label) for c in m[by_row] if not c.TopMember.Label in _keep_at_end]
            elif client_name != None:
                return [str(c[using_cell_value].Value) + " " + str(c.TopMember.Label) for c in m[by_row] if c.TopMember.Label != client_name]
            else:
                return [str(c[using_cell_value].Value) + " " + str(c.TopMember.Label) for c in m[by_row]]
        
        _keep_at_end = self._get_keep_at_end(file_name)    
        _lst = _get_list_without_excluded_items(client_name, _keep_at_end)
        
        #reverse the list to make ascending order
        if descending == True:
            _lst_incl_cells = list(reversed(self._sorted_nicely(_lst)))
        else:
            _lst_incl_cells = list(self._sorted_nicely(_lst))
        return self._rank_position(_lst_incl_cells)       
    
    def _get_keep_at_end(self,file_name):
        """Return a list from a csv file."""
        
        from utils.utilities import read_comma_separated_file
        try:
            _keep_at_end = read_comma_separated_file(file_name)
        except:
            raise ("Unable to read _file_name: " +  file_name)
        if _keep_at_end == None:
            _keep_at_end = list()
        return _keep_at_end

    def _get_labels_from_m_rows(self, m, by_column = 0, using_cell_value = 0, descending = True, file_name = None, client_name = None): 
        """Return a list of formated labels with values from matrix"""
                        
        ###note using_cell_value is not implemented as it wasnt working as expected in this line:
        #settings = FormatSettings(label_format="{0[using_cell_value].Value} {0.SideMember.Label}")
        from labels.format_labels import FormatSettings
        settings = FormatSettings(label_format="{0[0].Value} {0.SideMember.Label}")
        if file_name != None:
            _keep_at_end = self._get_keep_at_end(file_name)
            _labels_tmp =  [settings.label_format(r[by_column]) if r[0].Count > 0 and not r.Member.Label in _keep_at_end else "" for r in m]
        elif client_name != None:
            _labels_tmp =  [settings.label_format(r[by_column]) if r[0].Count > 0 and r.Member.Label != client_name else "" for r in m]
        else:
            _labels_tmp =  [settings.label_format(r[by_column]) if r[by_column].Count > 0 else "" for r in m]
        if descending == True:
            return self._rank_position(reversed(self._sorted_nicely(_labels_tmp)))
        else:
            return self._rank_position(self._sorted_nicely(_labels_tmp))
        
    def _get_labels_from_m_columns(self, m, by_row = 0, using_cell_value = 0, descending = True, file_name = None, client_name = None): 
        """Return a list of formated labels with values from matrix"""
                        
        ###note using_cell_value is not implemented as it wasnt working as expected in this line:
        #settings = FormatSettings(label_format="{0[using_cell_value].Value} {0.SideMember.Label}")
        
        from labels.format_labels import FormatSettings
        settings = FormatSettings(label_format="{0[0].Value} {0.TopMember.Label}")
        if file_name != None:
            _keep_at_end = self._get_keep_at_end(file_name)
            _labels_tmp =  [settings.label_format(c) if m[by_row].Count > 0 and not c.TopMember.Label in _keep_at_end else "" for c in m[by_row]]
        elif client_name != None:
            _labels_tmp =  [settings.label_format(c) if m[by_row].Count > 0 and c.TopMember.Label  != client_name else "" for c in m[by_row]]
        else:
            _labels_tmp =  [settings.label_format(c) if m[by_row].Count > 0 else "" for c in m[by_row]]
        if descending == True:
            return self._rank_position(reversed(self._sorted_nicely(_labels_tmp)))
        else:
            return self._rank_position(self._sorted_nicely(_labels_tmp))
        
    #########################################################
    #Start of regression tests for transformations package  #
    #########################################################
       
    def test_sort_rows_default(self):
        m,x = _make_matrix()
        _sort_col = 0
        _matrix_labels = self._sorting_order_rows(m, by_column =_sort_col, using_cell_value = 0)
        x.sort_rows()
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
        _sort_row = 5
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