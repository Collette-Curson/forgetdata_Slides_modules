
def NumberStatementsInMatrix():
    from globals import *
    
    # summarize the base scores from the first column into the row headings
    i=0
    for row in Matrix:
        i=i+1
        row.Member.Label = str(i)+  ". " + row.Member.Label


def SetMatrixLabelToStatement(whichstatement):
    from globals import *
    Matrix.Label = Matrix.SideAxis.Groups[0][whichstatement-1].ToString()
