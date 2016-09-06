__version__ = "4.2"
def TopNSummary(n):
    from globals import *
    
    # if the table hasn't got enough rows do nothing
    if(Matrix.Count < n):
        return
    
    #col1 = None
    #col2 = None
    #for col in Matrix.TopAxis.DataMembers:
    #    if col.Label == "trifft zu":
    #        col1 = col
    #    elif col.Label == "trifft eher zu":
    #        col2 = col
    #for row in Matrix:
    #    row[newCol].AddValue(str(row[col1][0].GetNumericValue() + row[col2][0].GetNumericValue()))
    
    # insert a blank row after n to hold our values
    newRow = Matrix.InsertBlankRowAfter(Matrix[Matrix.Count-1].Member,"topN","Top " + str(n))
    
    # go across all the columns and sum the values
    for crossbreak in Matrix.TopAxis.DataMembers:
        sumVal = 0
        for rowNum in range(0,n):
            sumVal += Matrix[rowNum][crossbreak][0].GetNumericValue()
        Matrix[Matrix.Count-1][crossbreak].AddValue(str(int( sumVal*100)) + "%")
        
def ColumnDifference(x,y):
    from globals import *
    
    # if the table hasn't got enough columns do nothing
    if(Matrix.TopAxis.DataMembers.Count < y):
        return
   
    # insert a blank row after n to hold our values
    newColumn = Matrix.InsertBlankColumnAfter(Matrix.TopAxis.DataMembers[y],"diff","Shift")
    
    #go down the table and find the difference of y-x and put into the new column
    for row in Matrix:
        print "x ", str(x) 
        valx = row[x][0].GetNumericValue()
        print "valx ", valx
        valy = row[y][0].GetNumericValue()
        valnew =valy-valx
        row[y+1].AddValue(str(valnew*100))
            
def RenumberSigTests():
    from globals import Matrix
    #if(not Matrix.HasColumnTest):
    #    return
    letterMapping = dict()
    atoz = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    counter = 0
    for col in Matrix.TopAxis.DataMembers:
        if(len(col.MemberSigTestHeading) > 0):
            logicalletter = str(atoz[counter])
            letterMapping[col.MemberSigTestHeading] = logicalletter
            col.MemberSigTestHeading = str(logicalletter)
            counter +=1
        
        if(counter >25):
            break
            
    for row in Matrix:
        for cell in row:
            original = cell[cell.Count - 1].Value
            new = str()
            for letter in original:
                if(letterMapping.has_key(letter)):
                    new += letterMapping[letter]
            cell[cell.Count - 1].Value = new
            cell.SigTestResult = new
                    

def NumberDownbreaks(delimiter):
    from globals import *
    for i in range (0, Matrix.SideAxis.DataMembers.Count):
        top = Matrix.SideAxis.DataMembers[i]
        top.Label = str(i + 1) + delimiter + top.Label
