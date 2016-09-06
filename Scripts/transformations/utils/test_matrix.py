def create_matrix():
###This function is used throughout to generate a matrix containing data
    a = [[4,20,33,102,51],
           [6,7,108,9,10],
           [1,102,3,4,5],
           [100,10,12,13,14],
           [5,6,7,8,109]]

    import matrixfuncs
    
    Matrix = matrixfuncs.matrixFromArray(a)

    for row in Matrix:
        row.Member.Label = "myRow " + str(row.Member.DataIndex)
        row.Member.Group.Label = "myRowGroup " + str(row.Member.DataIndex)

    for col in range(0, Matrix.TopAxis.DataMembers.Count):
        Matrix.TopAxis.DataMembers[col].Label = "myColumn " + str(col)
        Matrix.TopAxis.DataMembers[col].Group.Label = "myColumnGroup " + str(col)
    Matrix.Header.Left = "Header Left"
    Matrix.Header.Right = "Header Right"
    Matrix.Footer.Left = "Footer Left"
    Matrix.Footer.Right = "Footer Right"
    Matrix.Label = "Matrix Label"
    return Matrix

def add_dummy_stats_tests_to_matrix(Matrix):
    ###This will add stats test headers and results into the Matrix.
        #add stat letters to columns
        atoz = "JKLMNOPQRSTUVWXYZABCDEFGHI"
        counter=0

        for col in Matrix.TopAxis.DataMembers:
            if counter < 26:
                logicalletter = str(atoz[counter])
                col.MemberSigTestHeading = logicalletter
                counter += 1
            else: counter = 0

        #add stat results to cells
        for row in Matrix:
            for cell in row:
                #set the stat result to be the same as the next column's stat heading
                try:
                    cell.SigTestResult = Matrix.TopAxis.DataMembers[cell.TopMember.DataIndex+1].MemberSigTestHeading
                except:
                    cell.SigTestResult = Matrix.TopAxis.DataMembers[0].MemberSigTestHeading
                cell.AddValue(cell.SigTestResult,None)

def printThisMatrix(Matrix):
###This function is used for printing the resulting matrix.
    import matrixfuncs
    matrixfuncs.printMatrix(Matrix,colWidth=20,maxWidth=80)
    try:
        print "Matrix Label = ", Matrix.Label
        print "SideGroup0  Label = ", Matrix.SideAxis.Groups[0].Label
        print "TopGroup0 Label = ", Matrix.TopAxis.Groups[0].Label
        print "Header Left = ", Matrix.Header.Left
        print "Header Right = ", Matrix.Header.Right
        print "Footer Left = ", Matrix.Footer.Left
        print "Footer Right = ", Matrix.Footer.Right
        print "\n"
    except:
        pass