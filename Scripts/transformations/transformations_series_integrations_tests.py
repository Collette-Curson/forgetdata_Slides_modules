'''
Updated 14th Jan 2016
@author: ccurson


###SERIES MODULE TESTS

This set of regression tests will test all of the functions within the
"series" module of the transformations package installed with Slides.

This class is to be used for other data formats, eg pandas, so run these without the 
matrixfuncs.py to generate the Matrix from a List.

Also to be run using Matrix created using Slides.

See $RepSuite\Releases\4.3\Forgetdata\Libraries\Lib\forgetdata\Scripts\transformations package.

'''

########Variables that can be reset when running this test###############
use_test_data = True

#Real data only used when use_test_data == False. 
import os
mtd_filepath = os.path.abspath(os.path.join('utils\\Master Demo 2010.mtd'))
table_selected = 0 # table within mtd file used for tests when use_test_data==False

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

#import os, sys
#lib_path = os.path.abspath(os.path.join('..','utils'))   #relative path to transformations\utils\
#sys.path.append(lib_path)
#print sys.path

import utils.utilities as utilities
import utils.matrixfuncs as matrixfuncs

def make_matrix():
    """make a matrix either from test_matrix or by connecting to Slides."""
    import transformations as tr  #this imports series, categories, data, text, pptx_data
        
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
        
    x=tr.MatrixManipulator(m)
    #utilities.print_matrix(m)
    #print ""
    return m,x

class Test(TestCase):
    """Class for unit testing series module from the transformations package.
    m is a matrix created from a list of lists or is a Slides Matrix -
    defined by make_matrix() 
    
    """
    
    #########################################################
    #Start of regression tests for transformations package  #
    #########################################################
    
    
    def test_get_series_labels(self):
        m,x =  make_matrix()
        _matrix_labels =[row.Member.Label for row in m]
        _labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_get_series_labels = ", _matrix_labels
    
    def test_get_series_group_labels(self): 
        m,x =  make_matrix()
        _matrix_group_labels =[grp.Label for grp in m.SideAxis.Groups]
        _labels = x.get_series_group_labels()
        self.assertEqual(_labels,_matrix_group_labels)
        print "test_get_series_group_labels = ", _matrix_group_labels
    
    def test_get_series_labels_formatted(self):        
        m,x =  make_matrix()
        from labels.format_labels import FormatSettings
        settings = FormatSettings(label_format="{0.SideMember.Label} (n = {0[0].Value})")
        _labels =  [settings.label_format(r[0]) if r[0].Count > 0 else "" for r in m]
        _matrix_labels = [row.Member.Label + " (n = " + str(row[0][0].Value)  + ")" for row in m]
        self.assertEqual(_labels,_matrix_labels)
        print "test_get_series_labels_formatted = ", _matrix_labels
    
    def test_get_series_labels_failure(self):
        m,x =  make_matrix()
        _matrix_labels = [row.Member.Label for row in m]
        #add failure scenario to matrix
        m.DeleteRow(0)
        _labels = x.get_series_labels()
        with self.assertRaises(AssertionError): 
            self.assertEqual(_labels, _matrix_labels)
        print "test_get_series_labels_failure - row0 missing:"
        utilities.print_matrix(m)
    
    def test_get_series_base_summary(self):
        m,x =  make_matrix()
        _labels = x.get_series_base_summary()
        _lst_matrix_labels = [r.Member.Label + ": " + r[0][0].Value for r in m]
        _matrix_labels =  ", ".join(_lst_matrix_labels)
        self.assertEqual(_labels,_matrix_labels)
        print "test_get_series_base_summary = ", _matrix_labels
    
    def test_get_series_base_summary_wrong_column_failure(self):
        m,x =  make_matrix()
        _labels = x.get_series_base_summary()
        _lst_matrix_labels = [r.Member.Label + ": " + r[1][0].Value for r in m]
        _matrix_labels =  ", ".join(_lst_matrix_labels)
        with self.assertRaises(AssertionError): 
            self.assertEqual(_labels,_matrix_labels)
        print "test_get_series_base_summary_wrong_column_failure = ", _labels, "-", _matrix_labels
    
    def test_get_series_base_summary_bad_cell_value_failure(self):
        m,x =  make_matrix()
        _labels = x.get_series_base_summary()
        with self.assertRaisesRegexp(Exception, 'Index was out of range'):
            _lst_matrix_labels = [r.Member.Label + ": " + r[0][1].Value for r in m]
            _matrix_labels =  ", ".join(_lst_matrix_labels)
            self.assertEqual(_labels,_matrix_labels)
        print "test_get_series_base_summary_bad_cell_value_failure = ", _labels
    
    def test_get_series_base_summary_missing_cell_value_failure(self):
        m,x =  make_matrix()
        _lst_matrix_labels = [r.Member.Label + ": " + r[0][0].Value for r in m]
        _matrix_labels =  ", ".join(_lst_matrix_labels)
        #make error scenario    
        m[0][0].RemoveValueAt(0)
        with self.assertRaisesRegexp(Exception, 'Index was out of range'):
            _labels = x.get_series_base_summary()
            self.assertEqual(_labels,_matrix_labels)
        print "test_get_series_base_summary_missing_cell_value_failure = ", _matrix_labels
    
    def test_set_series_base_summary(self):
        m,x =  make_matrix()
        _matrix_labels = [r.Member.Label + " (n=" + r[0][0].Value + ")" for r in m]
        x.set_series_base_summary()
        _labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_set_series_base_summary = ", _matrix_labels
    
    def test_set_series_formatted_labels_default(self):
        m,x =  make_matrix()
        _matrix_labels = [r.Member.Label for r in m]
        x.set_series_formatted_labels()
        _labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_set_series_formatted_labels_default = ", _matrix_labels
    
    def test_set_series_formatted_labels_incl_group(self):
        m,x =  make_matrix()
        _matrix_labels = [r.Member.Group.Label + " :: " + r.Member.Label for r in m]       
        x.set_series_formatted_labels(label_format = "{0.SideMember.Group.Label} :: {0.SideMember.Label}")
        _labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_set_series_formatted_labels_incl_group = ", _matrix_labels
    
    def test_set_series_formatted_labels_bad(self):
        m,x =  make_matrix()
        _matrix_labels = [r.Member.Group.Label + " :: " + r.Member.Label for r in m]
        with self.assertRaisesRegexp(AttributeError, 'CDataCell'):
            x.set_series_formatted_labels(label_format = "{0.Group.Label} :: {0.Label}")
            _labels = x.get_series_labels()
            self.assertEqual(_labels,_matrix_labels)
        print "test_set_series_formatted_labels_bad = AttributeError: 'CDataCell' object has no attribute 'Group'"
        
    def test_set_series_groups_formatted_labels_default(self):
        m,x =  make_matrix()
        _matrix_group_labels = [r.Label for r in m.SideAxis.Groups]
        x.set_series_groups_formatted_labels()
        _labels = x.get_series_group_labels()
        self.assertEqual(_labels,_matrix_group_labels)
        print "test_set_series_groups_formatted_labels_default = ", _matrix_group_labels
        
    def test_set_series_groups_formatted_labels_incl_sort_index(self):
        m,x =  make_matrix()
        _matrix_group_labels = [grp.Label + " :: " + str(grp.SortIndex) for grp in m.SideAxis.Groups]   
        #reset matrix as group labels have been set above.
        m,x =  make_matrix()
        x.set_series_groups_formatted_labels(label_format = "{0.Label} :: {0.SortIndex}")
        _labels = x.get_series_group_labels()
        self.assertEqual(_labels,_matrix_group_labels)
        print "test_set_series_groups_formatted_labels_incl_side_labels = ", _matrix_group_labels
        
    def test_set_series_groups_formatted_labels_bad(self):
        m,x =  make_matrix()
        _matrix_labels = [r.Member.Group.Label + " :: " + r.Member.Label for r in m]
        with self.assertRaisesRegexp(AttributeError, 'CMemberGroup'):
            x.set_series_groups_formatted_labels(label_format = "{0.Group.Label} :: {0.Label}")
            _labels = x.get_series_group_labels()
            self.assertEqual(_labels,_matrix_labels)
        print "test_set_series_groups_formatted_labels_bad = AttributeError: 'CMemberGroup' object has no attribute 'Group'"
            
    def test_number_series(self):
        m,x =  make_matrix()
        _labels = [str(r.Member.DataIndex+1) + ". " +  r.Member.Label for r in m]
        x.number_series(". ")
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_number_series('. ') = ", _matrix_labels
    
    def test_number_series_no_delimeter(self):
        m,x =  make_matrix()
        _labels = [str(r.Member.DataIndex+1) + " " + r.Member.Label for r in m]
        x.number_series()
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_number_series_no_delimeter() = ", _matrix_labels

    def test_number_series_other_delimeter(self):
        m,x =  make_matrix()
        _labels = [str(r.Member.DataIndex+1) + "/ " + r.Member.Label for r in m]
        x.number_series("/ ")
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_number_series_other_delimeter('/ ') = ", _matrix_labels
    
    def test_number_series_bad_delimeter(self):
        m,x =  make_matrix()
        X=None
        _labels = [str(r.Member.DataIndex+1) + "X " + r.Member.Label for r in m]
        with self.assertRaisesRegexp(TypeError, 'cannot concatenate'):
            x.number_series(X)
            _matrix_labels = x.get_series_labels()
            self.assertEqual(_labels,_matrix_labels)
        print "test_number_series_bad_delimeter(X) = ", _labels
        
    def test_del_base_series(self):
        m,x =  make_matrix()
        bases=["Base"]
        _labels = [r.Member.Label for r in m if r.Member.Label not in bases]
        x.del_base_series()
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_del_base_series  = ", _labels
    
    def test_del_base_series_with_base_list(self):
        m,x =  make_matrix()
        bases=["Base","Total"]
        _labels = [r.Member.Label for r in m if r.Member.Label not in bases]
        x.del_base_series(bases)
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_del_base_series_with_base_list  = ", _labels
    
    def test_del_base_series_with_base(self):
        m,x =  make_matrix()
        m[2].Member.Label = "This is a Base"
        _labels = [r.Member.Label for r in m if "Base" != r.Member.Label] 
        x.del_base_series()
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_del_base_series_with_base (Base not detected) = ", _labels  
    
    #Testing del_series
    def test_del_series(self):
        m,x =  make_matrix()
        if use_test_data == True:
            _lst = ["myRow 1","myRow 2"]
        else:
            _lst = ["Strongly Agree","Somewhat Agree"]
        _labels = [r.Member.Label for r in m if r.Member.Label not in _lst]        
        x.del_series(_lst)
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_del_series", _matrix_labels

     
    def test_del_series_no_values(self):
        m,x =  make_matrix()
        _lst = []
        _labels = [r.Member.Label for r in m if r.Member.Label not in _lst]
        x.del_series(_lst)
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_del_series_no_values", _matrix_labels

    
    def test_del_series_not_list(self):
        m,x =  make_matrix()
        if use_test_data == True:
            _lst = "myRow 1"
        else:
            _lst = "Strongly Agree"
        _labels = [r.Member.Label for r in m if r.Member.Label != _lst]        
        x.del_series(_lst)
        _matrix_labels = x.get_series_labels()
        with self.assertRaises(AssertionError): 
            self.assertEqual(_labels, _matrix_labels)
        print "test_del_series_not_list", _matrix_labels
        
    def test_del_series_bad_values(self):
        m,x =  make_matrix()
        _lst = ["myRow ddd"]
        _labels = [r.Member.Label for r in m if r.Member.Label not in _lst]
        x.del_series(_lst)
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_del_series_bad_values", _matrix_labels
    
    def test_del_series_by_index(self):
        m,x =  make_matrix()
        _lst = [1,2]
        _labels = [r.Member.Label for r in m if r.Member.DataIndex not in _lst]
        x.del_series(_lst)
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)        
        print "test_del_series_by_index", _matrix_labels
        
    
    def test_del_series_mixed_bad_values(self):
        m,x =  make_matrix()
        _lst = ["a", "b", 3]
        _labels = [r.Member.Label for r in m if r.Member.Label not in _lst]
        if _labels.__len__() == m.Count: 
            _labels = [r.Member.Label for r in m if r.Member.DataIndex not in _lst]
        x.del_series(_lst)
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)  
        print "test_del_series_mixed_bad_values", _matrix_labels
    
    def test_del_series_mixed_values(self):
        m,x =  make_matrix()
        if use_test_data == True:
            _lst = ["myRow 3", 0, 4]
        else: 
            _lst = ["Strongly Agree", 0, 4]
        _labels = [r.Member.Label for r in m if r.Member.Label not in _lst]
        if _labels.__len__() == m.Count: 
            _labels = [r.Member.Label for r in m if r.Member.DataIndex not in _lst]
        x.del_series(_lst)
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)  
        print "test_del_series_mixed_values", _matrix_labels        
            
    def test_del_series_by_index_bad_values(self):
        m,x =  make_matrix()
        _lst = [-1, 5]
        _labels = [r.Member.Label for r in m if r.Member.DataIndex not in _lst]
        x.del_series(_lst)
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)  
        print "test_del_series_by_index_bad_values", _matrix_labels
    
    #Testing select_series

    def test_select_series(self):
        m,x =  make_matrix()
        if use_test_data == True:
            _lst = ["myRow 1","myRow 2"]
        else:
            _lst = ["Strongly Agree","Somewhat Agree"]
        _labels = [r.Member.Label for r in m if r.Member.Label in _lst]

        x.select_series(_lst)
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels) 
        print "test_select_series", _matrix_labels
    
    def test_select_series_no_values(self):
        m,x =  make_matrix()
        _lst = []
        _labels = [r.Member.Label for r in m if r.Member.Label in _lst]
        x.select_series(_lst)
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels) 
        print "test_select_series_no_values", _matrix_labels
        
    def test_select_series_bad_value(self):
        m,x =  make_matrix()
        _lst = ['myRow ddd']
        _labels = [r.Member.Label for r in m if r.Member.Label in _lst]

        x.select_series(_lst)
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels) 
        print "test_select_series_bad_value", _matrix_labels

    def test_select_series_by_index(self):
        m,x =  make_matrix()
        _lst = [1,3]
        _labels = [r.Member.Label for r in m if r.Member.DataIndex in _lst]
        x.select_series(_lst)
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels) 
        print "test_select_series_by_index", _matrix_labels

    def test_select_series_by_index_bad_values(self):
        m,x =  make_matrix()
        _lst = [1,5]
        _labels = [r.Member.Label for r in m if r.Member.DataIndex in _lst]
        x.select_series(_lst)
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels) 
        print "test_select_series_by_index_bad_values", _matrix_labels
    
    def test_select_series_by_label_bad_values(self):
        m,x =  make_matrix()       
        if use_test_data == True:
            _lst = ["myRow 0", "myRow 4", "myRow 9"]
        else:
            _lst = ["myRow 0", "Strongly Agree", "myRow 9"]            
        _labels = [r.Member.Label for r in m if r.Member.Label in _lst]
        x.select_series(_lst)
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels) 
        print "test_select_series_by_label_bad_values", _matrix_labels
    
    def test_select_series_mixed_bad_values(self):
        m,x =  make_matrix()
        _lst = ["a", "b", 3]
        _labels = [r.Member.Label for r in m if r.Member.Label in _lst]
        if _labels.__len__() == 0: 
            _labels = [r.Member.Label for r in m if r.Member.DataIndex  in _lst]
        x.select_series(_lst)
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)  
        print "test_select_series_mixed_bad_values", _matrix_labels
    
    def test_select_series_mixed_values(self):
        m,x =  make_matrix() 
        if use_test_data == True:
            _lst = ["myRow 3", 0, 4]
        else:
            _lst = ["Strongly Agree", 0, 4]
        _labels = [r.Member.Label for r in m if r.Member.Label in _lst]
        if _labels.__len__() == 0: 
            _labels = [r.Member.Label for r in m if r.Member.DataIndex  in _lst]
        x.select_series(_lst)
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)  
        print "test_select_series_mixed_values", _matrix_labels        
            
    def test_select_series_by_index_bad_values(self):
        m,x =  make_matrix()
        _lst = [-1, 5]
        _labels = [r.Member.Label for r in m if r.Member.DataIndex in _lst]
        x.select_series(_lst)
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)  
        print "test_select_series_by_index_bad_values", _matrix_labels
    
     
    def test_insert_gap_between_series_groups(self):
        m,x =  make_matrix()
        #update Matrix to include multiple groups
        sideGroup=m.SideAxis.Groups.AddNew(None,"newgroup","newgroup")
        newMember = sideGroup.AddNewMember("abc","abc",True,False,0)
        
        ###TODO Write a bug as this behaves differently in IronPython vs Python.
        try: # IronPython
            m.SideAxis.DataMembers.Add(newMember)
        except: # Python
            pass
            #This line is not needed to be run for Python
            #m.TopAxis.DataMembers.Add.Overloads[type(newMember)](newMember) 
        
        for col in m[5]:
            col.AddValue("10%",None)
        m.SideAxis.DataMembers[5].Label = "New Label"
        x.insert_gap_between_series_groups()
        _matrix_labels = x.get_series_labels()
        self.assertFalse(False,"testInsertGapBetweenGroups Failed")
        print "test_insert_gap_between_series_groups", _matrix_labels
        
    def test_insert_gap_between_series_groups_one_group(self):
        m,x =  make_matrix()
        x.insert_gap_between_series_groups()
        self.assertFalse(False,"test_insert_gap_between_series_groups_one_group Failed")
        _matrix_labels = x.get_series_labels()
        print "test_insert_gap_between_series_groups_one_group", _matrix_labels
        
    def test_insert_topN_into_series(self):
        m,x =  make_matrix()
        _matrix_labels = [r.Member.Label for r in m]
        _matrix_labels.insert(0, "Top 2")
        x.insert_topN_into_series(2)
        _labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)  
        _matrix_labels = x.get_series_labels()
        print "test_insert_topN_into_series", _matrix_labels
    
    def test_insert_series(self):
        m,x =  make_matrix()
        _matrix_labels = [r.Member.Label for r in m]
        _matrix_labels.insert(4,"my new series")
        x.insert_series(row_number = 4, label = "my new series")
        _labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)  
        print "test_insert_series", _matrix_labels
    
    def test_insert_series_too_big(self):
        m,x =  make_matrix()
        _labels = [r.Member.Label for r in m]
        x.insert_series(row_number = 20, label = "this will fail")
        _matrix_labels = x.get_series_labels()
        self.assertEqual(_labels,_matrix_labels)  
        print "test_insert_series", _matrix_labels
                                  
#import sys
#sys.modules["globals"] = object()
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()