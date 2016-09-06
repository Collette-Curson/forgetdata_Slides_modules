""" 
    Provides additional merging features
"""

__version__ = '4.3.0'

def MergeRowsByLabel():
    '''
    Merges the rows in the active matrix (e.g. :class:`globals.Matrix`) 
    by their labels. 

    For example, if you have a matrix as follows::

        _______|January|Februar|  March|  April|    May|   June|
        Brand 1|      2|      3|      4|       |       |       |
        Brand 1|       |       |       |      1|      2|      3|

    this will merge to::
    
        _______|January|Februar|  March|  April|    May|   June|
        Brand 1|      2|      3|      4|      1|      2|      2|

    '''
    from globals import Matrix

    dictRows = dict()
    rowsToDelete = []
    for row in Matrix:
        if(dictRows.has_key(row.Member.Label)):
            targetrow = dictRows[row.Member.Label]

            for cell in row:
                targetcell=targetrow[cell.TopMember]
                for value in cell:
                    clone = value.Clone()
                    targetcell.AddValue(clone)
            rowsToDelete.append(row.Member.DataIndex)
        else:
            dictRows[row.Member.Label] = row

    # clear up by deleting the merged rows out
    rowsToDelete.reverse()
    for rowIndex in rowsToDelete:
        Matrix.DeleteRow(rowIndex)

def MergeColumnsByLabel():
    '''
    Merges the columns in the active matrix (e.g. :class:`globals.Matrix`) 
    by their labels. 

    For example, if you have a matrix as follows::

        _______|January|Februar|  March|January|Februar|  March|
        Brand 1|      2|      3|      4|       |       |       |
        Brand 2|       |       |       |      1|      2|      3|

    this will merge to::
    
        _______|January|Februar|  March|
        Brand 1|      2|      3|      4|
        Brand 2|      1|      2|      2|

    '''
    from globals import Matrix

    dictCols = dict()
    colsToDelete = []
    for col in Matrix.TopAxis.DataMembers:
        if(dictCols.has_key(col.Label)):
            targetcol = dictCols[col.Label]

            for row in Matrix:
                cell = row[col]
                targetcell = row[targetcol]
                for value in cell:
                    clone = value.Clone()
                    targetcell.AddValue(clone)
            colsToDelete.append(col.DataIndex)

        else:
            dictCols[col.Label] = col

    colsToDelete.reverse()
    for colIndex in colsToDelete:
        Matrix.DeleteColumn(colIndex)