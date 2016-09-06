"""

Provides basic sorting functions for use within data transformations. 


"""
__version__ = '4.3.0'

def SortRows(byColumn=0,usingCellValue=0,descending=True,Matrix=None):
    '''
    Sorts the rows in the active matrix (e.g. :class:`globals.Matrix`) 
    numerically. 
    
    :param byColumn: Use the values in this column to determine the sort order of the rows.

    :param usingCellValue: When there are multiple values within a cell use this
            to control which value row within each cell is used for sorting
            (zero-based)
    :param descending: Determines the order in which the values should be
            sorted. 
    '''
    if(Matrix==None):
        import globals
        Matrix = globals.Matrix
   
    if(Matrix == None or Matrix.Count < 2):
        return;

    if(Matrix.TopAxis.DataMembers.Count <= byColumn):
        globals.trace("SortRows cannot sort by column " + str(byColumn));
        return; 

    for A in range(0,Matrix.Count):
        for B in range(0,Matrix.Count):
            if(A==B):
                continue; #do not compare rows against eachother

            valA = Matrix[A][byColumn][usingCellValue].NumericValue if Matrix[A][byColumn].Count > usingCellValue else None;
            valB = Matrix[B][byColumn][usingCellValue].NumericValue if Matrix[B][byColumn].Count > usingCellValue else None;
            
            if(descending):
                if valB < valA:
                    Matrix.SwitchRows(A,B)
            else:
                if valA < valB:
                    Matrix.SwitchRows(A,B)


def SortColumns(byRow=0,usingCellValue=0,descending=True,Matrix=None):
    """
    Sorts the columns in the active matrix (e.g. :class:`globals.Matrix`) 
    numerically. 
    
    :param byRow: Use the values in this row to determine the sort order of the 
            columns.
    :param usingCellValue: When there are multiple values within a cell use this
            to control which value row within each cell is used for sorting
            (zero-based)
    :param descending: Determines the order in which the values should be
            sorted. 
    """
    if Matrix is None:
        import globals
        Matrix = globals.Matrix

    if(Matrix == None or Matrix.TopAxis.DataMembers.Count < 2):
        return;

    if(Matrix.Count <= byRow):
        globals.trace("SortColumns cannot sort by row" + str(byRow));
        return; 


    for A in range(0,Matrix.TopAxis.DataMembers.Count):
        for B in range(0,Matrix.TopAxis.DataMembers.Count):
            if(A==B):
                continue; #do not compare rows against eachother

            valA = Matrix[byRow][A][usingCellValue].NumericValue if Matrix[byRow][A].Count > usingCellValue else None;
            valB = Matrix[byRow][B][usingCellValue].NumericValue if Matrix[byRow][B].Count > usingCellValue else None;

            if(descending):
                if valB < valA:
                    Matrix.SwitchColumns(A,B)
            else:
                if valA < valB:
                    Matrix.SwitchColumns(A,B)
