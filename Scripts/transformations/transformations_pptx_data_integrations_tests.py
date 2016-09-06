'''
Updated 26th Jan 2016
@author: ccurson


###pptx_data MODULE TESTS

This set of regression tests will test all of the functions within the
"pptx_data" module of the transformations package installed with Slides.

This class is to be used for other data formats, eg pandas, so run these without the 
matrixfuncs.py to generate the Matrix from a List.

Also to be run using Matrix created using Slides.

See $RepSuite\Releases\4.3\Forgetdata\Libraries\Lib\forgetdata\Scripts\transformations package.

'''

########Variables that can be reset when running this test###############
use_test_data = False

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

import utils.matrixfuncs as matrixfuncs
import utils.utilities as utilities

def _make_matrix():
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
    
    
   
        
    #########################################################
    #Start of regression tests for transformations package  #
    #########################################################
    '''
    TODO once the module can run in version 4.3. or later
    
    def test_append_matrix_data_to_prefill_matrix(self):
    def print_powerpoint_table_data(self):
    def print_powerpoint_chart_data(self):
    
    '''        
#import sys
#sys.modules["globals"] = object()
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']

    unittest.main()