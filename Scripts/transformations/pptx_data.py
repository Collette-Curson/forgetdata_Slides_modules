"""Provides basic matrix manipulation functions for use within data
transformations.

Updated Jan 2016
@author: ccurson

"""

__version__ = '4.3.0'   
from functools import wraps

class PowerPointDataManipulator():
    r"""Class for manipulating PowerPoint data. 
    
    Imported into MatrixManipulator in __init__.py within transformations package
    
    This class is designed to manipulate or view data that was present in the 
    PowerPoint file, prior to a fill from Slides!
    For example if you have existing wave data, and wish to merge new data into 
    the existing table or chart.
    "PreFillMatrix" is available from within Slides UI and contains the 
    underlying chart or table data in the PowerPoint shape before any Slides! 
    selection is applied. 
    
    Examples:
    >>> import pptx_data as Pptx_data
    >>> import utils.matrixfuncs as matrixfuncs
    >>> m = matrixfuncs.create_test_matrix()
    >>> prefill_matrix = matrixfuncs.create_test_matrix()## TODO update this
    >>> Shape = "shape"  ## TODO update this
    >>> _my_class = Pptx_data.PowerPointDataManipulator(prefill_matrix,m, Shape)
    
    """
    
    def __init__(self, prefill_matrix, matrix, Shape):
        self.data = prefill_matrix
        self.matrix = matrix
        self.shape = Shape
    
    def wrap_matrix_logger(func):
        @wraps(func)
        def func_wrapper(self, *args):
            # Return the class with a matrix parameter
            
            matrix = self.matrix
            return func(self, matrix, logger, args)
        return func_wrapper
    
    def wrap_prefill_matrix(func):
        @wraps(func)
        def func_wrapper(self, *args):
            # Return the class with a matrix parameter
            
            prefill_matrix = self.data
            return func(self, prefill_matrix, args)
        return func_wrapper
        
    def wrap_shape(func):
        @wraps(func)
        def func_wrapper(self, *args):
            # Return the class with a matrix parameter
            
            shape = self.shape
            return func(self, shape, logger, args)
        return func_wrapper
       
    '''
    # TODO THIS IS UNTESTED!!
    # Test this - This is 4.3 code, which requires core.py to be read on 
    # start up of Slides, and also for this to run:
    # from Forgetdata.Slides.PowerPointHandler import PowerPointScripting
    @wrap_matrix
    @wrap_prefill_matrix
    def append_matrix_data_to_prefill_matrix(self, prefill_matrix, matrix, logger, *args):
        """Use the `PreFillMatrix` and then append any new data from the selected Matrix to this,
        and then override the Matrix with this data.

        This function can be used when you have tracking data where the original
        wave data is not store in the Slides! data format, eg it only exists in
        PowerPoint.

        'PreFillMatrix' is generated from the underlying Chart/Table in PowerPoint,
        before any selections are applied.

        """

        #Make a set for the prefill_matrix and also matrix containing a set of lists of rowlabel, col label, cell values.
        prefill_set = ((r.Member.Label, c.TopMember) for r in self.data for c in self.data[0])
        matrix_set = ((r.Member.Label, c.TopMember) for r in self.matrix for c in self.matrix[0])
        
        prefill_rows_set = (r.Member.Label for r in self.data)
        matrix_rows_set = (r.Member.Label for r in self.matrix)
        prefill_cols_set = (c.TopMember.Label for c in self.data[0])
        matrix_cols_set = (c.TopMember.Label for c in self.matrix[0])
        
        matching_cells = prefill_set.intersection(matrix_set)
        matching_rows = prefill_rows_set.intersection(matrix_rows_set)
        matching_cols = prefill_cols_set.intersection(matrix_cols_set)
        
        
        if  matching_rows.__len__() > 0:  
            
            for _lst in (matrix_rows_set - matching_rows):
                newRow = self.data.InsertBlankRowAfter(self.data.SideAxis.DataMembers[self.data.Count-1]," ", _lst)
                Log.Info ("Inserting a new row for: " + _lst)
                #for each col in the new row, add a cellitem
                for col in newRow:
                    col.AddValue(str(""),None)
                
                row_num = [r.Member.DataIndex for r in self.matrix if _lst == r.Member.Label]
                row = self.matrix[row_num[0]]    
                
                #For each cell in this new row, if the column label matches, insert the data from Matrix into PreFillMatrix
                #if it doesn't match, then insert a new column, and add the label and the data value to the new column.
                for item in row:
                    if item.TopMember.Label in matching_cols:
                        colnum = [c.TopMember.DataIndex for c in self.data[0] if item.TopMember.Label == c.TopMember.Label][0]
                        self.data[colnum].AddValue(item[0].Value,None)
                    else:
                        newcol = self.data.InsertBlankColumnAfter(self.data.TopAxis.DataMembers[self.data.TopAxis.DataMembers.Count-1]," ",item.TopMember.Label)
                        self.data[row_num][self.data.TopAxis.DataMembers.Count-1].TopMember.Label = item.TopMember.Label
                        self.data[row_num][self.data.TopAxis.DataMembers.Count-1].AddValue(item[0].Value,None)
                        
                        for row in newcol:
                            if row.Count < 1: 
                                row.AddValue(str(""),None)       

        for i in range(0,Matrix.Count-1):
            Matrix.DeleteRow(Matrix.Count-1-i)

        for i in range(0,self.data.Count):
            newRow = self.matrix.InsertBlankRowAfter(self.matrix.SideAxis.DataMembers[i]," ",self.data.SideAxis.DataMembers[i].Label)
            for j in range(0, self.data.TopAxis.DataMembers.Count):
                self.matrix[i+1][j].AddValue(self.data[i][j][0].Clone())
        self.matrix.DeleteRow(0)
        
    @wrap_shape
    def print_powerpoint_table_data(self, shape, logger, *args):
        """A debugging function for printing out the contents of a PowerPoint Table."""
        rows = list()
        for row in range(2, shape.Table.Rows.Count+1):
            rows.append([shape.Table.Cell(row,col).Shape.TextFrame.TextRange.Text for col in range(1,shape.Table.Columns.Count+1)])
        col_labels = [shape.Table.Cell(1,col).Shape.TextFrame.TextRange.Text for col in range(1,shape.Table.Columns.Count+1)]
        logger(col_labels)
        logger(rows)
    
    @wrap_shape
    def print_powerpoint_chart_data(self, shape, logger, *args):
        """A debugging function for printing out the contents of a PowerPoint Chart."""
        rows = list()
        rows.append([(shape.Chart.SeriesCollection(row).Name, shape.Chart.SeriesCollection(row).Values[i]) for i in range(1,shape.Chart.SeriesCollection(1).XValues.Count) for row in range(1,shape.Chart.SeriesCollection().Count)]) 
        col_labels = list()
        colLabels.append([shape.Chart.SeriesCollection(1).XValues[i] for col in shape.Chart.SeriesCollection(1).XValues])
        logger(rows)
        logger(col_labels)
        
        row_labels = list()
        vals=list()
        col_labels = list()

        cols = shape.Chart.SeriesCollection(1).XValues.Count
        rows =  shape.Chart.SeriesCollection().Count
        for row in range(1,rows):
            vals.append([shape.Chart.SeriesCollection(row).Values[i] for i in range(0, cols)])

        row_labels = [(shape.Chart.SeriesCollection(row).Name, vals[row-1]) for row in range(1, shape.Chart.SeriesCollection().Count)] 

        col_labels = [shape.Chart.SeriesCollection(1).XValues[i] for col in shape.Chart.SeriesCollection(1).XValues]

        logger(col_labels)
        logger(row_labels)

    #   End of class
    '''
if __name__ == "__main__":
    import doctest
    doctest.testmod()

