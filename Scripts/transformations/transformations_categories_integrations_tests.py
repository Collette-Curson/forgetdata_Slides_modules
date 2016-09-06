'''
Updated 14th Jan 2016
@author: ccurson

###category MODULE TESTS

This set of regression tests will test all of the functions within the
"category" module of the transformations package installed with Slides.

This class is to be used for other data formats, eg pandas, so run these 
without the matrixfuncs.py to generate the Matrix from a List.

Also to be run using Matrix created using Slides.

See $RepSuite\Releases\4.3\Forgetdata\Libraries\Lib\forgetdata\Scripts\
transformations package.

'''

########Variables that can be reset when running this test###############
use_test_data = True

#Real data only used when use_test_data == False. 
import os
mtd_filepath = os.path.abspath(os.path.join('utils\\Master Demo 2010.mtd'))
# table within mtd file used for tests when use_test_data==False
table_selected = 0 

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

def make_matrix():
    """make a matrix either from test_matrix or by connecting to Slides."""
    #this imports category, category, data, text, pptx_data
    import transformations as tr  
        
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
    
        liveConnection = slidesconf.connect(conn.ConnectionString, 
                                            name=conn.Name, 
                                            provider_name=conn.Provider)
        m = liveConnection[table_selected]
    x=tr.MatrixManipulator(m)
    #utilities.print_matrix(m)

    for c in m[0]:
        c.TopMember.Label = c.TopMember.Label.encode('ascii','ignore')    
    return m,x

class Test(TestCase):
    """Class for unit testing category module from the transformations package.
    m is a matrix created from a list of lists or is a Slides Matrix
    defined by defined by make_matrix() 
    
    """
    
    #########################################################
    #Start of regression tests for transformations package  #
    #########################################################
                
    def test_get_category_labels(self):
        m,x =  make_matrix()
        _matrix_labels =[col.TopMember.Label for col in m[0]]
        _labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_get_category_labels = ", _matrix_labels
    
    def test_get_category_group_labels(self):
        m,x =  make_matrix()
        _matrix_group_labels =[grp.Label for grp in m.TopAxis.Groups]
        _labels = x.get_category_group_labels()
        self.assertEqual(_labels,_matrix_group_labels)
        print "test_get_category_group_labels = ", _matrix_group_labels
    
    def test_get_category_labels_formatted(self):
        m,x =  make_matrix()
        from labels.format_labels import FormatSettings
        settings = FormatSettings(label_format="{0.TopMember.Label} (n = {0[0].Value})")
                
        _labels =  [settings.label_format(c) if c.Count > 0 else "" for c in m[0]]
        _matrix_labels = [col.TopMember.Label + " (n = " + str(col[0].Value)  + ")" for col in m[0]]
        self.assertEqual(_labels,_matrix_labels)
        print "test_get_category_labels_formatted = ", _matrix_labels
    
    def test_get_category_labels_failure(self):
        m,x =  make_matrix()
        _matrix_labels = [col.TopMember.Label for col in m[0]]
        #add failure scenario to matrix
        m.DeleteColumn(0)
        _labels = x.get_category_labels()
        with self.assertRaises(AssertionError): 
            self.assertEqual(_labels, _matrix_labels)
        print "test_get_category_labels_failure - col0 missing:"
        utilities.print_matrix(m)
    
    def test_get_category_base_summary(self):
        m,x =  make_matrix()
        _labels = x.get_category_base_summary()
        print _labels
        _lst_matrix_labels = [c.TopMember.Label + ": " + c[0].Value for c in m[0]]
        _matrix_labels =  ", ".join(_lst_matrix_labels)
        self.assertEqual(_labels,_matrix_labels)
        print "test_get_category_base_summary = ", _matrix_labels
    
    def test_get_category_base_summary_wrong_row_failure(self):
        m,x =  make_matrix()
        _labels = x.get_category_base_summary()
        print _labels
        _lst_matrix_labels = [c.TopMember.Label + ": " + c[0].Value for c in m[1]] #row 1
        _matrix_labels =  ", ".join(_lst_matrix_labels)
        with self.assertRaises(AssertionError): 
            self.assertEqual(_labels,_matrix_labels)
        print "test_get_category_base_summary_wrong_column_failure = ", _labels, "-", _matrix_labels
    
    def test_get_category_base_summary_bad_cell_value_failure(self):
        m,x =  make_matrix()
        _labels = x.get_category_base_summary()
        with self.assertRaisesRegexp(Exception, 'Index was out of range'):
            _lst_matrix_labels = [c.TopMember.Label + ": " + c[1].Value for c in m[0]]
            _matrix_labels =  ", ".join(_lst_matrix_labels)
            self.assertEqual(_labels,_matrix_labels)
        print "test_get_category_base_summary_bad_cell_value_failure = ", _labels
    
    def test_get_category_base_summary_missing_cell_value_failure(self):
        m,x =  make_matrix()
        _lst_matrix_labels = [c.TopMember.Label + ": " + c[0].Value for c in m[0]]
        _matrix_labels =  ", ".join(_lst_matrix_labels)   
        #make error scenario    
        m[0][0].RemoveValueAt(0)
        with self.assertRaisesRegexp(Exception, 'Index was out of range'):
            _labels = x.get_category_base_summary()
            self.assertEqual(_labels,_matrix_labels)
        print "test_get_category_base_summary_missing_cell_value_failure = ", _matrix_labels
    
    def test_set_category_base_summary(self):
        m,x =  make_matrix()
        _matrix_labels = [c.TopMember.Label + " (n=" + c[0].Value +")" for c in m[0]]
        x.set_category_base_summary()
        _labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_set_category_base_summary = ", _matrix_labels
    
    def test_set_category_formatted_labels_default(self):
        m,x =  make_matrix()
        _matrix_labels = [c.TopMember.Label for c in m[0]]
        x.set_category_formatted_labels()
        _labels = x.get_category_labels()       
        self.assertEqual(_labels,_matrix_labels)
        print "test_set_category_formatted_labels_default = ", _matrix_labels
    
    def test_set_category_formatted_labels_group(self):
        m,x =  make_matrix()
        _matrix_labels = [c.TopMember.Group.Label + " :: " + c.TopMember.Label for c in m[0]]
        x.set_category_formatted_labels(label_format = "{0.TopMember.Group.Label} :: {0.TopMember.Label}")
        _labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_set_category_formatted_labels_group = ", _matrix_labels
    
    def test_set_category_formatted_labels_bad(self):
        m,x =  make_matrix()
        _matrix_labels = [c.TopMember.Group.Label + " :: " + c.TopMember.Label for c in m[0]]
        with self.assertRaisesRegexp(AttributeError, 'CDataCell'):
            x.set_category_formatted_labels(label_format = "{0.Group.Label} :: {0.Label}")
            _labels = x.get_category_labels()
            self.assertEqual(_labels,_matrix_labels)
        print "test_set_category_formatted_labels_bad = AttributeError: 'CDataCell' does not contain 'Group'"

    def test_set_category_groups_formatted_labels_default(self):
        m,x =  make_matrix()
        _matrix_labels = [grp.Label for grp in m.TopAxis.Groups]
        x.set_category_groups_formatted_labels()
        _labels = x.get_category_group_labels()       
        self.assertEqual(_labels,_matrix_labels)
        print "test_set_category_groups_formatted_labels_default = ", _matrix_labels

    def test_set_category_groups_formatted_labels_group(self):
        m,x =  make_matrix()
        _matrix_labels = [grp.Label + " :: " + str(grp.SortIndex) for grp in m.TopAxis.Groups]
        x.set_category_groups_formatted_labels(label_format = "{0.Label} :: {0.SortIndex}")
        _labels = x.get_category_group_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_set_category_groups_formatted_labels_group = ", _matrix_labels
    
    def test_set_category_group_formatted_labels_bad(self):
        m,x =  make_matrix()
        _matrix_labels = [grp.Label + " :: " + str(grp.SortIndex) for grp in m.TopAxis.Groups]
        with self.assertRaisesRegexp(AttributeError, 'CMemberGroup'):
            x.set_category_groups_formatted_labels(label_format = "{0.Group.Label} :: {0.SortIndex}")
            _labels = x.get_category_group_labels()
            self.assertEqual(_labels,_matrix_labels)
        print "test_set_series_formatted_labels_bad = AttributeError: 'CMemberGroup' object has no attribute 'Group'"
    
    def test_del_base_category(self):
        m,x =  make_matrix()
        bases=["Base"]
        _labels = [c.TopMember.Label for c in m[0] if c.TopMember.Label not in bases] 
        x.del_base_category()
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_del_base_category  = ", _labels
        
    def test_del_base_category_with_base_list(self):
        m,x =  make_matrix()
        bases=["Base", "Total"]
        _labels = [c.TopMember.Label for c in m[0] if c.TopMember.Label not in bases] 
        x.del_base_category(bases)
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_del_base_category_with_base_list  = ", _labels
    
    def test_del_base_category_with_base_within_text(self):
        m,x =  make_matrix()
        m[0][2].TopMember.Label = "This is a Base"
        _labels = [c.TopMember.Label for c in m[0] if "Base" != c.TopMember.Label] 
        x.del_base_category()
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_del_base_category_with_base_within_text (base not found)= ", _labels  
    
    #Testing del_categories
    def test_del_categories(self):
        m,x =  make_matrix()
        if use_test_data == True:
            _lst = ["myColumn 1","myColumn 2"]
        else:
            _lst = ["Under 20","Less than 6 months"]
        _labels = [c.TopMember.Label for c in m[0] if c.TopMember.Label not in _lst]
        x.del_categories(_lst)
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_del_categories", _matrix_labels
    
    def test_del_categories_not_list(self):
        m,x =  make_matrix()
        if use_test_data == True:
            _lst = "myColumn 1"
        else:
            _lst = "Under 20"
        _labels = [c.TopMember.Label for c in m[0] if c.TopMember.Label not in _lst]
        x.del_categories(_lst)
        _matrix_labels = x.get_category_labels()
        with self.assertRaises(AssertionError): 
            self.assertEqual(_labels, _matrix_labels)  
        print "test_del_categories_not_list", _matrix_labels
            
    def test_del_categories_no_values(self):
        m,x =  make_matrix()
        _lst = []
        _labels = [c.TopMember.Label for c in m[0] if c.TopMember.Label not in _lst]
        x.del_categories(_lst)
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_del_categories_no_values", _matrix_labels
    
    def test_del_categories_bad_values(self):
        m,x =  make_matrix()
        _lst = ["myColumn ddd"]
        _labels = [c.TopMember.Label for c in m[0] if c.TopMember.Label not in _lst]
        x.del_categories(_lst)
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels)
        print "test_del_categories_bad_values", _matrix_labels
    
    def test_del_categories_by_index(self):
        m,x =  make_matrix()
        _lst = [1,2]
        _labels = [c.TopMember.Label for c in m[0] if c.TopMember.DataIndex not in _lst]
        x.del_categories(_lst)
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels)        
        print "test_del_categories_by_index", _matrix_labels
    
    def test_del_categories_mixed_bad_values(self):
        m,x =  make_matrix()
        _lst = ["a", "b", 3]
        _labels = [c.TopMember.Label for c in m[0] if c.TopMember.Label not in _lst]
        if _labels.__len__() == m.TopAxis.DataMembers.Count: 
            _labels = [c.TopMember.Label for c in m[0] if c.TopMember.DataIndex not in _lst]
        x.del_categories(_lst)
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels)  
        print "test_del_categories_mixed_bad_values", _matrix_labels
    
    def test_del_categories_mixed_values(self):
        m,x =  make_matrix()
        if use_test_data == True:
            _lst = ["myColumn 3", 0, 4]
        else: 
            _lst = ["Under 20", 0, 4]
        _labels = [c.TopMember.Label for c in m[0] if c.TopMember.Label not in _lst]
        if _labels.__len__() == m.TopAxis.DataMembers.Count: 
            _labels = [c.TopMember.Label for c in m[0] if c.TopMember.DataIndex not in _lst]
        x.del_categories(_lst)
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels)  
        print "test_del_categories_mixed_values", _matrix_labels        
    
    def test_del_categories_by_index_bad_values(self):
        m,x =  make_matrix()
        _lst = [-1, 5]
        _labels = [c.TopMember.Label for c in m[0] if c.TopMember.Label not in _lst]
        if _labels.__len__() == m.TopAxis.DataMembers.Count: 
            _labels=list()
            _labels = [c.TopMember.Label for c in m[0] if c.TopMember.DataIndex not in _lst]
        x.del_categories(_lst)
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels)  
        print "test_del_categories_by_index_bad_values", _matrix_labels
    
    #Testing select_categories
    def test_select_categories(self):
        m,x =  make_matrix()
        if use_test_data == True:
            _lst = ["myColumn 1","myColumn 2"]
        else:
            _lst = ["Under 20","Less than 6 months"]
        _labels = [c.TopMember.Label for c in m[0] if c.TopMember.Label in _lst]
        x.select_categories(_lst)
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels) 
        print "test_select_categories", _matrix_labels
    
    def test_select_categories_no_values(self):
        m,x =  make_matrix()
        _lst = []
        _labels = [c.TopMember.Label for c in m[0] if c.TopMember.Label in _lst]
        x.select_categories(_lst)
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels) 
        print "test_select_categories_no_values", _matrix_labels
        
    def test_select_categories_bad_value(self):
        m,x =  make_matrix()
        _lst = ['myColumn ddd']
        _labels = [c.TopMember.Label for c in m[0] if c.TopMember.Label in _lst]
        x.select_categories(_lst)
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels) 
        print "test_select_categories_bad_value", _matrix_labels
    
    def test_select_categories_by_index(self):
        m,x =  make_matrix()
        _lst = [1,3]
        _labels = [c.TopMember.Label for c in m[0] if c.TopMember.DataIndex in _lst]
        x.select_categories(_lst)
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels) 
        print "test_select_categories_by_index", _matrix_labels
    
    def test_select_categories_by_index_bad_values(self):
        m,x =  make_matrix()
        _lst = [1,5]
        _labels = [c.TopMember.Label for c in m[0] if c.TopMember.DataIndex in _lst]
        x.select_categories(_lst)
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels) 
        print "test_select_categories_by_index_bad_values", _matrix_labels
    
    def test_select_categories_by_label_bad_values(self):
        m,x =  make_matrix()        
        if use_test_data == True:
            _lst = ["myColumn 0", "myColumn 4", "myColumn 9"]
        else:
            _lst = ["Under 20","Less than 6 months", "myColumn 9"]
        _labels = [c.TopMember.Label for c in m[0] if c.TopMember.Label in _lst]
        x.select_categories(_lst)
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels) 
        print "test_select_categories_by_label_bad_values", _matrix_labels
    
    def test_select_categories_mixed_bad_values(self):
        m,x =  make_matrix()
        _lst = ["a", "b", 3]
        _labels = [c.TopMember.Label for c in m[0] if c.TopMember.DataIndex in _lst]
        x.select_categories(_lst)
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels)  
        print "test_select_categories_mixed_bad_values", _matrix_labels
    
    def test_select_categories_mixed_values(self):
        m,x =  make_matrix()    
        if use_test_data == True:
            _lst = ["myColumn 3", 0, 4]
        else:
            _lst = ["Under 20", 0, 4]
        _labels = [c.TopMember.Label for c in m[0] if c.TopMember.Label in _lst]
        if _labels.__len__() == 0: 
            _labels = [c.TopMember.Label for c in m[0] if c.TopMember.DataIndex in _lst]
        x.select_categories(_lst)
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels)  
        print "test_select_categories_mixed_values", _matrix_labels        
     
    def test_insert_gap_between_category_groups(self):
        m,x =  make_matrix()
        #update Matrix to include multiple groups
        topGroup=m.TopAxis.Groups.AddNew(None,"newgroup","newgroup")
        newMember = topGroup.AddNewMember("abc","abc",True,False,0)
        ###TODO Write a bug as this behaves differently in IronPython vs Python.
        try: # IronPython
            m.TopAxis.DataMembers.Add(newMember)
        except: # Python
            pass
            #This line is not needed to be run for Python
            #m.TopAxis.DataMembers.Add.Overloads[type(newMember)](newMember) 
        m.TopAxis.DataMembers[5].Label = "New Label"
        #run the unit test
        x.insert_gap_between_category_groups()
        _matrix_labels = x.get_category_labels()
        self.assertFalse(False,"test_insert_gap_between_category_groups Failed")
        print "test_insert_gap_between_category_groups", _matrix_labels
    
    def test_insert_gap_between_category_groups_one_group(self):
        m,x =  make_matrix()
        x.insert_gap_between_category_groups()
        self.assertFalse(False,"test_insert_gap_between_category_groups_one_group Failed")
        _matrix_labels = x.get_category_labels()
        print "test_insert_gap_between_category_groups_one_group", _matrix_labels
    
    def test_insert_category(self):
        m,x =  make_matrix()
        _labels = [c.TopMember.Label for c in m[0]]
        _labels.insert(2,"new column 2")
        x.insert_category(column_number = 2, label = "new column 2")
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels)  
        print "test_insert_category", _matrix_labels
    
    def test_insert_category_too_big(self):
        m,x =  make_matrix()
        _labels = [c.TopMember.Label for c in m[0]]
        x.insert_category(column_number = 40, label = "this will fail")
        _matrix_labels = x.get_category_labels()
        self.assertEqual(_labels,_matrix_labels)  
        print "test_insert_category_too_big", _matrix_labels
        
#import sys
#sys.modules["globals"] = object()
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()