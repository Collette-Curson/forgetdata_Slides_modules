"""
Provides convenience functions for manipulating a matrix
a matrix.
"""
__version__ = '4.3.0'

def InsertColumn(colIndex,name="",label="", Matrix=None):
    """
    Inserts a blank column at the specified index using the grouping of the next column
    the heading of the added column index is returned.

    :param colIndex: This should be the index of the new column this must be an existing index.
    :param name: The name associated with the new column.
    :param label: The label of the new column. 
    :param Matrix: if specified this is the Matrix that is used, otherwize `globals.Matrix` is used.
    """
    if(Matrix == None):
        from globals import Matrix

    colToInsertBefore = Matrix.TopAxis.DataMembers[colIndex]
    newColumn = Matrix.InsertBlankColumnAfter(colToInsertBefore,name,label)

    Matrix.SwitchColumns(colToInsertBefore.DataIndex,newColumn.DataIndex)
    return Matrix.TopAxis.DataMembers[colIndex]

def InsertRow(rowIndex,name="",label="",Matrix=None):
    """
    Inserts a blank row at the specified index the DataRow of the added row index is returned.

    :param rowIndex: This should be the index of the new column this must be an existing index.
    :param name: The name associated with the new column.
    :param label: The label of the new column. 
    :param Matrix: if specified this is the Matrix that is used, otherwize `globals.Matrix` is used.
    """
    if(Matrix == None):
        from globals import Matrix
    rowToInsertBefore = Matrix[rowIndex].Member

    newRow = Matrix.InsertBlankRowAfter(rowToInsertBefore,name,label)
    Matrix.SwitchRows(rowToInsertBefore.DataIndex,newRow.DataIndex)
    return Matrix[rowIndex]

def UngroupRows():
    """Performs a gridfication of a flat table where you have 
    grid slices appended down the side of the table
    
    Does not work when there is nesting or concatenation on the top
    it would be more complicated.
    """

    from globals import Matrix
    if(Matrix.SideAxis.Groups.Count < 2):
        return #nothing to do

    if(Matrix.TopAxis.Groups.Count > 1):
        raise Exception("The table cannot have nesting or concatenation on the top")
    # replicate the existing top group
    masterTopGroup = Matrix.TopAxis.Groups[0]

    
    masterSideGroup = Matrix.SideAxis.Groups[0]
    for iGrp in range(1,Matrix.SideAxis.Groups.Count):
        #activeGroup means the one we are transferring from side to top
        activeGroup = Matrix.SideAxis.Groups[iGrp]


        #topGroup is the new group we are creating for the top
        topGroup = Matrix.TopAxis.Groups.AddNew(None,activeGroup.Name + "_top",activeGroup.Label)
        for masterMember in masterTopGroup:
            newMember = topGroup.AddNewMember(masterMember.Name,masterMember.Label,masterMember.IsVisible,masterMember.IsSummaryScore)
            Matrix.TopAxis.DataMembers.Add(newMember)

        # transfer any values over
        for member in activeGroup:
            sourceRow = Matrix[member]
            #find the target row in the first group
            for targetMember in masterSideGroup:
                if targetMember.Label == member.Label:
                    targetRow = Matrix[targetMember]
                    
                    for intColOffsetId in range(masterTopGroup.Count):
                        sourceCol = masterTopGroup[intColOffsetId]
                        targetCol = topGroup[intColOffsetId]
                        for val in sourceRow[sourceCol]:
                            targetRow[targetCol].AddValue(val)
    
    masterTopGroup.Label = Matrix.SideAxis.Groups[0].Label
    
    while Matrix.Count > masterSideGroup.Count:
        Matrix.DeleteRow(masterSideGroup.Count)
