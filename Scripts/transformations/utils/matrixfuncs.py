
def subtractRows(row1,row2,rowAnswer,Matrix=None):


    if(Matrix==None):
        import globals
        Matrix = globals.Matrix

    if(row1 == None or row2 == None or rowAnswer==None):
        raise TypeError

    if(max(row1,row2,rowAnswer) >= Matrix.Count):
        raise IndexError("Not enough rows in matrix")

    rowSrc = Matrix[row1]
    rowAway = Matrix[row2]
    rowTarget = Matrix[rowAnswer]

    # all columns
    columns = Matrix.TopAxis.DataMembers

    for col in columns:
        cellSrc = rowSrc[col]
        cellAway = rowAway[col]
        cellTarget = rowTarget[col]

        if(cellSrc.Count == cellAway.Count):
            for valueIndex in range(0,cellSrc.Count):

                valueTarget = cellSrc[valueIndex].Clone()

                if(valueTarget.NumericValue != None and cellAway[valueIndex].NumericValue != None):
                    valueTarget.NumericValue -= cellAway[valueIndex].NumericValue


                cellTarget.AddValue(valueTarget)

def newMatrix():
    import Forgetdata.Matrix

    topAxis = Forgetdata.Matrix.CAxisMap()
    sideAxis= Forgetdata.Matrix.CAxisMap()
    matrixData = Forgetdata.Matrix.CMatrixData(sideAxis,topAxis)
    matrix = Forgetdata.Matrix.CMatrix(None,matrixData,Forgetdata.Matrix.CHeaderFooter(),Forgetdata.Matrix.CHeaderFooter())
    return matrix

def matrixFromArray(a):
    import Forgetdata.Matrix

    try:
        import System.InvalidOperationException as ioe
    except:
        ioe = Exception

    topAxis = Forgetdata.Matrix.CAxisMap()
    topGroup = topAxis.Groups.AddNew(None,"","")
    sideAxis= Forgetdata.Matrix.CAxisMap()
    sideGroup = sideAxis.Groups.AddNew(None,"","")

    for i,row in enumerate(a):
        sidemember = None
        if(sideAxis.DataMembers.Count <=i):
            sidemember = sideGroup.AddNewMember(str(i),"Row"+str(i),True,False,0)
            try:
                sideAxis.DataMembers.Add(sidemember)
            except ioe:
                if(sidemember.DataIndex <0):
                    sideAxis.DataMembers.Add.Overloads[type(sidemember)](sidemember)

        for j,cell in enumerate(row):

            topmember = None
            if (topAxis.DataMembers.Count <=j ):
                topmember = topGroup.AddNewMember(str(j),"Col"+str(j),True,False,0)
                try:
                    topAxis.DataMembers.Add(topmember)
                except ioe:
                    if(topmember.DataIndex <0):
                        topAxis.DataMembers.Add.Overloads[type(topmember)](topmember)

    matrixData = Forgetdata.Matrix.CMatrixData(sideAxis,topAxis)
    matrix = Forgetdata.Matrix.CMatrix(None,matrixData,Forgetdata.Matrix.CHeaderFooter(),Forgetdata.Matrix.CHeaderFooter())

    for i, row in enumerate(a):
        for j,cell in enumerate(row):
            if (cell != None):
                matrix[i][j].AddValue(str(cell),None)
    return matrix

def matrixFromArray2(a):
    import Forgetdata.Matrix


    topAxis = Forgetdata.Matrix.CAxisMap()
    topGroup = topAxis.Groups.AddNew(None,"","")
    sideAxis= Forgetdata.Matrix.CAxisMap()
    sideGroup = sideAxis.Groups.AddNew(None,"","")

    for i,row in enumerate(a):
        sidemember = None
        if(sideAxis.DataMembers.Count <=i):
            sidemember = sideGroup.AddNewMember(str(i),"Row"+str(i),True,False,0)
            sideAxis.DataMembers.Add(sidemember)

        for j,cell in enumerate(row):

            topmember = None
            if (topAxis.DataMembers.Count <=j ):
                topmember = topGroup.AddNewMember(str(j),"Col"+str(j),True,False)
                topAxis.DataMembers.Add(topmember)

    matrixData = Forgetdata.Matrix.CMatrixData(sideAxis,topAxis)
    matrix = Forgetdata.Matrix.CMatrix(None,matrixData,Forgetdata.Matrix.CHeaderFooter(),Forgetdata.Matrix.CHeaderFooter())

    for i, row in enumerate(a):
        for j,cell in enumerate(row):
            if (cell != None):
                matrix[i][j].AddValue(str(cell))
    return matrix

def loadArrayToMatrix(matrix,a):
    if matrix.TopAxis.Groups.Count == 0: matrix.TopAxis.Groups.AddNew(None,"","")
    if matrix.SideAxis.Groups.Count == 0: matrix.SideAxis.Groups.AddNew(None,"","")
    for i, row in enumerate(a):
        if i >= matrix.SideAxis.DataMembers.Count:
            if (i > 0): sideGroup = matrix.SideAxis.DataMembers[i-1].Group
            else: sideGroup = matrix.SideAxis.Groups[0]
            matrix.SideAxis.DataMembers.Add(sideGroup.AddNewMember(str(i),"",True,False))
        for j, cell in enumerate(row):
            if(matrix.TopAxis.DataMembers.Count <= j):
                if(j > 0): topGroup = matrix.TopAxis.DataMembers[j-1].Group
                else: topGroup = matrix.TopAxis.Groups[0]
                matrix.TopAxis.DataMembers.Add(topGroup.AddNewMember(str(j),"",True,False))
            matrix[i][j].AddValue(str(cell))

def createBlankMatrix(topAxis = None,sideAxis = None):
    import Forgetdata.Matrix
    if topAxis is None:
        topAxis = Forgetdata.Matrix.CAxisMap()
    if sideAxis is None:
        sideAxis = Forgetdata.Matrix.CAxisMap()

    return Forgetdata.Matrix.CMatrix(Forgetdata.Matrix.CMeasureList(),
                                     Forgetdata.Matrix.CMatrixData(
                                        sideAxis,
                                        topAxis,
                                     ),
                                     Forgetdata.Matrix.CHeaderFooter(),
                                     Forgetdata.Matrix.CHeaderFooter())
    printMatrix()

def printMatrix(matrix,colWidth=11,maxWidth=80):

    print ""
    if matrix.Name:
        print "Name : " + "%.60s" % matrix.Name
    if matrix.Label:
        print "Label : " + "%.60s" % matrix.Name


    colFmtWidth=colWidth - 1

    stringFmt = "%" + str(colFmtWidth) + "." + str(colFmtWidth) + "s"
    header = ("X" * colFmtWidth) + "|"

    for top in matrix.TopAxis.DataMembers:
        if top.MemberSigTestHeading != "":
            stat = " (" + top.MemberSigTestHeading + ")"
        else:
            stat = ""
        header += stringFmt % ( top.Label ) + stat + "|"

    print header

    desiredWidth= (matrix.TopAxis.DataMembers.Count +1) * colWidth
    if(desiredWidth > maxWidth):
        print "=" * maxWidth
    else:
        print "=" * desiredWidth


    for row in matrix:

        strRow = stringFmt % row.Member.Label +  "|"

        for cell in row:
            if cell.SigTestResult != "":
                statResult = " (" + cell.SigTestResult + ")"
            else:
                statResult = ""
            if(cell.Count == 0):
                strRow +=stringFmt % ""
            else:
                strRow += stringFmt % str(cell[0]) + statResult
            strRow +="|"
        print (strRow)
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
    print ""

def create_test_matrix():
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

def add_dummy_stats_tests_to_test_matrix(Matrix):
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
