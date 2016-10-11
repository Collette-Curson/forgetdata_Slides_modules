import array
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


def make_fake_matrix(arr):
    """Make a matrix without using clr or any Matrix Objects.
    This is needed for doctest to pass when readthedocs is building.
    
    """
    
    class Container(object):
        
        def Label(self):
            return str()
        
        def Name(self):
            return self.Label
        
        def __str__(self):
            return self.Label
         
        def __repr__(self):
            return self.Label
        
        def GetNumericValue(self):
            return self.NumericValue
        
        def DataIndex(self):
            pass
        
    class MyStringContainer(object):
        
        def Label(self):
            return str()
        
        def Left(self):
            pass
        
        def Right(self):
            pass
        
        def Center(self):
            pass
        
        def __str__(self):
            return self.Label
        
        def __repr__(self):
            return self.Label
        
        pass 
    
    class MyList(list):
        
        def Label(self):
            return str()

        def __str__(self):
            return self.Label
        
        def Name(self):
            return self.Label
        
        #def __repr__(self):
        #    return self.Label
        
        def Name(self):
            return str()
        
        def Count(self):
            pass
    
        def Add(self,a):
            member = Container()
            member.Label = a
            return member
        
        def AddNewMember(self,a,b,c,d,e):
            member = Container()
            member.Label = a          
            return member
        
        def Group(self):
            return MyList()
        
        def TopAxis(self):
            return Container()
        
        def SideAxis(self):
            return Container()
        
        def AddNew(self,a,b,c):
            return MyList()
        
        def SwitchRows(self,a,b):
            sorted_list = sorted([a,b])
            min = sorted_list[0]
            max = sorted_list[1]
            
            self.insert(max, self[min])
            self.insert(min, self[max+1])
            self.pop(min+1)
            self.pop(max+1) 
            
        
        def SwitchColumns(self,a,b):
            sorted_list = sorted([a,b])
            min = sorted_list[0]
            max = sorted_list[1]
            
            self.TopAxis.DataMembers.insert(max, self.TopAxis.DataMembers[min])
            self.TopAxis.DataMembers.insert(min, self.TopAxis.DataMembers[max+1])
            self.TopAxis.DataMembers.pop(min + 1)
            self.TopAxis.DataMembers.pop(max + 1)
            
            for i in range(0, self.__len__()):
                self[i].insert(max, self[i][min])
                self[i].insert(min, self[i][max+1])
                self[i].pop(min+1)
                self[i].pop(max+1)
                
        def DeleteRow(self, val):            
            self.pop(val)
            
        def DeleteColumn(self, val):
            self.TopAxis.DataMembers.pop(val)
            for i in range(0, self.__len__()):
                self[i].pop(val)
           
            
        def InsertBlankRowAfter(self,a,b,c):
            '''self.SideAxis.DataMembers.insert(a.DataIndex, c)
            self.insert(a.DataIndex, c)
            '''
            pass
        
        def InsertBlankColumnAfter(self,a,b,c):
            '''
            self.TopAxis.DataMembers.insert(a.DataIndex,c)
            for i in range(0,self.Count):
                self[i].insert(a.DataIndex, c)
                self[i][a.DataIndex+1]=MyList()
                self[i][a.DataIndex+1].append(Container())
            return a.DataIndex +1
            '''
            pass
        
        def RemoveValueAt(self,a):
            pass
        
        def __str__(self):
            return self.Label
        
        def AddValue(self,a,b):
            pass
        
        pass
    
    matrix = MyList()
    
    rows = arr.__len__()
    cols = arr[0].__len__()
    cellitems = 1 
    
    matrix.SideAxis = Container()
    matrix.SideAxis.DataMembers = MyList()    
    matrix.SideAxis.DataMembers.Count = rows
    
    matrix.SideAxis.Groups = MyList()
    matrix.SideAxis.Groups.append(Container())
    matrix.SideAxis.Groups.Count = 1
    
    for i in range(0, rows):
        matrix.Count = rows
        matrix.SideAxis.DataMembers.append(Container())
        matrix.SideAxis.DataMembers[i].Label = str()
        matrix.SideAxis.DataMembers[i].Group = matrix.SideAxis.Groups[0]
        matrix.SideAxis.DataMembers[i].Group.Label = str()
        matrix.SideAxis.DataMembers[i].MemberSigTestHeading = str()
    
    matrix.TopAxis = Container()  
    matrix.TopAxis.DataMembers = MyList()
    matrix.TopAxis.DataMembers.Count = cols
    
    
    matrix.TopAxis.Groups = MyList()
    matrix.TopAxis.Groups.append(Container())
    matrix.TopAxis.Groups.Count = 1
    
    for j in range(0, cols):        
        matrix.TopAxis.DataMembers.append(MyList())
        matrix.TopAxis.DataMembers[j].Label = str()
        matrix.TopAxis.DataMembers[j].Group = matrix.TopAxis.Groups[0]
        matrix.TopAxis.DataMembers[j].Group.Label = str()
        matrix.TopAxis.DataMembers[j].MemberSigTestHeading = str()
        
    for i in range(0, rows): # rows
        matrix.append(MyList())
        #matrix[i] = MyList()
        matrix[i].Member = matrix.SideAxis.DataMembers[i]
        
        matrix[i].TopAxis = matrix.TopAxis
        matrix[i].TopAxis.DataMembers = matrix.TopAxis.DataMembers
        #matrix[i].Member.Label = str()
        matrix[i].Member.DataIndex = i
        matrix[i].Member.IndentLevel = 0
        matrix[i].Member.Group = matrix.SideAxis.Groups[0]
        matrix[i].Member.Group.Label = matrix.SideAxis.DataMembers[i].Group.Label
        
        for j in range(0, cols): # columns
            matrix[i].append(MyList()) # appeand for each col
            #matrix[i][j] = matrix[i].TopAxis.DataMembers[j]
            #matrix[i][j].Count = cols
            matrix[i][j].TopMember = matrix.TopAxis.DataMembers[j] # Container()
            #matrix[i][j].TopMember.Label = matrix.TopAxis.DataMembers[j].Label
            
            matrix[i][j].TopMember.DataIndex = j
            matrix[i][j].TopMember.IndentLevel = 0
            matrix[i][j].TopMember.Group = matrix.TopAxis.Groups[0] #MyList()
            #matrix[i][j].TopMember.Group.Label = matrix.TopAxis.DataMembers[j].Group.Label
            matrix[i][j].SideMember = matrix.SideAxis.DataMembers[i] #Container()
            #matrix[i][j].SideMember.Label = matrix.SideAxis.DataMembers[i].Label
            matrix[i][j].SideMember.Group =  matrix.SideAxis.Groups[0] #MyList()
            #matrix[i][j].SideMember.Group.Label = matrix.SideAxis.DataMembers[i].Group.Label
            matrix[i][j].SigTestResult = str()
            
            matrix[i][j].append(Container())
            
    for i in range(0, rows): # rows
        for j in range(0, cols): # columns
            # 1 cell item
            
            matrix[i][j][0].Count = 1
            matrix[i][j][0].Value = unicode(arr[i][j])
            matrix[i][j][0].Label = str(arr[i][j])
            #matrix[i][j][k].GetNumericValue()
            matrix[i][j][0].NumericValue = float(str(arr[i][j]))
            #matrix[i][j][k].FormatString() = "0"

    matrix.Header = MyStringContainer() 
    matrix.Footer = MyStringContainer()
    
    return matrix
    
def create_test_matrix():
###This function is used throughout to generate a matrix containing data
    a = [[101,20,330,102,51],
           [6,7,108,9,10],
           [1,102,3,4,5],
           [100,10,12,13,14],
           [5,6,7,8,109]]

    try:
        #fails #when running doctest via readthedocs.
        import slidesconf
        Matrix = matrixFromArray(a)
        #print "matrixFromArray failed as slidesconf not imported"
    except:
        Matrix = make_fake_matrix(a)
    
    for row in Matrix:
        row.Member.Label = u"myRow " + str(row.Member.DataIndex)
        row.Member.Group.Label = u"myRowGroup " + str(row.Member.DataIndex)
        
    for col in range(0, Matrix.TopAxis.DataMembers.Count):
        Matrix.TopAxis.DataMembers[col].Label = u"myColumn " + str(col)
        Matrix.TopAxis.DataMembers[col].Label
        Matrix.TopAxis.DataMembers[col].Group.Label = u"myColumnGroup " + str(col)
    
    for i in range(0, Matrix.Count):
        for j in range(0, Matrix.TopAxis.DataMembers.Count):
            if Matrix[i][j].TopMember.Label == "":
                Matrix[i][j].TopMember.Label = Matrix.TopAxis.DataMembers[j].Label    
            if Matrix[i][j].TopMember.Group.Label == "":
                Matrix[i][j].TopMember.Group.Label = Matrix.TopAxis.DataMembers[j].Group.Label

            if Matrix.SideAxis.DataMembers[i].Label == "":
                Matrix.SideAxis.DataMembers[i].Label = Matrix[i][j].SideMember.Label
                 
            if Matrix.SideAxis.DataMembers[i].Group.Label == "":
                Matrix.SideAxis.DataMembers[i].Group.Label = Matrix[i][j].SideMember.Group.Label 
    
    
    Matrix.Header.Left = u"Header Left"
    Matrix.Header.Right = u"Header Right"
    Matrix.Footer.Left = u"Footer Left"
    Matrix.Footer.Right = u"Footer Right"
    Matrix.Label = u"Matrix Label"
    Matrix.Name = u"Matrix Label"
    
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
                cell.AddValue(cell.SigTestResult, None)