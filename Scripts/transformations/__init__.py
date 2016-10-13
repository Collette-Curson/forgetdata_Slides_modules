"""Provides a class which merges the series/categories/data and pptx_data
modules into one class called MatrixManipulator.

"""

import utils.slidesconf as slidesconf

from series import MatrixSeriesManipulator as Series
from categories import MatrixCategoryManipulator as Categories
from data import MatrixDataManipulator as Data
from pptx_data import PowerPointDataManipulator as PptxData

__version__ = '4.3.0'

class MatrixManipulator(Series, Categories, Data, PptxData):
    r"""Class for manipulating labels or values from the series, categories,
    or data values of a matrix, or PowerPoint Chart or Table.
    
    This class will import all of the functions from the classes in the parameters list.  
    It is called with a matrix parameter.
    
    Example:
    
    _my_class = MatrixManipulator(Matrix)

    Examples:
    
    >>> import utils.matrixfuncs as matrixfuncs
    >>> m = matrixfuncs.create_test_matrix()
    >>> _my_class = MatrixManipulator(m)
    >>> print _my_class.get_series_labels()  #taken from series module
    [u'myRow 0', u'myRow 1', u'myRow 2', u'myRow 3', u'myRow 4']
    >>> print _my_class.get_category_labels() #taken from categories module
    [u'myColumn 0', u'myColumn 1', u'myColumn 2', u'myColumn 3', u'myColumn 4']
    >>> print _my_class.get_series_base_summary() 
    myRow 0: 101, myRow 1: 6, myRow 2: 1, myRow 3: 100, myRow 4: 5
    >>> print _my_class.get_category_base_summary()
    myColumn 0: 101, myColumn 1: 20, myColumn 2: 330, myColumn 3: 102, myColumn 4: 51
    >>> _my_class.get_data_values() #taken from data module
    [u'101', u'20', u'330', u'102', u'51', u'6', u'7', u'108', u'9', u'10', u'1', u'102', u'3', u'4', u'5', u'100', u'10', u'12', u'13', u'14', u'5', u'6', u'7', u'8', u'109']
    
    """
    
    def __init__(self, matrix):
        """Functions for formatting labels or data cells"""
        self.matrix = matrix
    

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
"""
To run this package using Python:
=================================
C:\ python 

import transformations as tr
import tr.utils.matrixfuncs as matrixfuncs
m=matrixfuncs.create_test_matrix()
x=tr.MatrixManipulator(m)

To run doctest, using a command prompt, go to:
==============================================

cd C:\Projects\RepSuite\Releases\4.3\Forgetdata\Libraries\Lib\forgetdata\Scripts>
>python transformations\series.py
>python transformations\categories.py
>python transformations\data.py
>python transformations\sorting.py
>python transformations\__init__.py

To run using PowerPoint:
========================

import transformations as tr
myClass = tr.MatrixManipulator(Matrix)

#format row/series labels:
from labels.format_labels import FormatSettings
settings = FormatSettings(label_format="{0.SideMember.Label} (n = {0[0].Value})")
        
for r in Matrix:
    r.Member.Label = settings.label_format(r[0]) if r[0].Count > 0 else ""

#format column/category labels:
from labels.format_labels import FormatSettings
settings = FormatSettings(label_format="{0.TopMember.Label} (n = {0[0].Value})")
        
for c in Matrix[0]:
    c.TopMember.Label = settings.label_format(r[0]) if r[0].Count > 0 else ""

myClass.insert_gap_between_series_groups()
myClass.insert_gap_between_category_groups()
print myClass.get_series_labels()
print myClass.get_category_labels()

myClass.sort_rows()
print myClass.get_series_labels()
print myClass.get_category_labels()
"""