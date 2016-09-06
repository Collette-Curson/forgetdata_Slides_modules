import os,sys
import code

class ActionRunner:
    class modulefinder():
        def find_module(self,modulename,path=None):
            if(modulename=="transformations"):
                return self
            elif(modulename=="shapes"):
                return self

        def load_module(self,name,path=None):  #name, file, pathname, description
            import importlib
            import code
            import imp
 
            txt= str(name) + ".py"
            
            ##This works from ipy
            ##===================
            ##pathx=os.path.pardir + r"\Scripts\ "[:-1] + txt
            ##return imp.load_module(name,open(pathx),txt,(".py","U",1))
            
            ##This works from PowerPoint
            ##==========================
            return imp.load_module(name,open(sys.path[0] + r"\Lib\forgetdata\Scripts\transformations.py"),"transformations.py",(".py","U",1))
             
    def __init__(self):
        sys.meta_path.append(ActionRunner.modulefinder())
        
    def RunAction(self, scriptText, scope):
        funccode = compile(scriptText,"", 'exec') 
        myscope = dict()
        myscope.update(scope)
        from Forgetdata.Slides.PowerPointHandler import PowerPointScripting
        from globals import Matrix
        
        #Set a series of global variables for use within the Transformation and and After Fill.
        
        myscope["Shape"] = PowerPointScripting.ActiveShape   # Shape = Active Shape
        myscope["Slide"] = PowerPointScripting.ActiveSlide # Slide = Active Slide
        myscope["Presentation"] = PowerPointScripting.ActivePresentation  #Ppt = The current PowerPoint presentation
        myscope["__package__"] = "forgetdata.slides.embedded.presentation" +".slide" + str(PowerPointScripting.ActiveSlide.SlideNumber) + ".shape" + str(PowerPointScripting.ActiveShape.Id) #forgetdata.slides.embedded.presentation.slide1.shape4, for example
        myscope["__file__"] = PowerPointScripting.ActivePresentation.FullName #__doc__ = fill path to the current Pptx file.
        myscope["Application"]=PowerPointScripting #pptApplication = PowerPoint (this would give you access to other open pptx files).
        
        #The following will create a Matrix, called "MatrixClone" and set it to contain the same Query as the original Matrix.
        #This is for use for global values such as Total/top 2/ bottom 2/ mean scores, which are sometimes needed within the After Fill, but need to be deleted from Matrix.
        myscope["MatrixClone"] = cloneMatrix(Matrix)
        
        #The following will create a  Matrix, called "PreFillMatrix" and set the current underlying values from the chart/table into it.
        #This might be used to append new data to the end of existing tables data, for example in Tracking projects where the past data is not stored in suitable format for Slides!
        Shape = PowerPointScripting.ActiveShape
        matrix=newMatrix(Shape)
        matrix=addToMatrix(Shape,matrix)
        myscope["PreFillMatrix"] = matrix

        #The following will set the Shape settings for the Shape onto a global variable called FillerSettings.
        import api
        shapeLink = api.GetShapeLink(Shape)
        myscope["FillerSettings"] = shapeLink.FillerProperties
        
        #Set all values to None so that all objects are released.
        for myvals in myscope:
            myvals = None
        
        exec(funccode,globals(),myscope)
        
def cloneMatrix(val): 
    try:
        import System.Xml
    except:
        import clr 
        clr.AddReference("System.Xml")
    from System.Xml.Serialization import XmlSerializer

    ser = XmlSerializer(val.GetType())
    import System.IO
    stream = System.IO.MemoryStream()
    ser.Serialize(stream,val)
    stream.Seek(0, System.IO.SeekOrigin.Begin)
    matrix = ser.Deserialize(stream)
    stream.Close()
    return matrix

def cloneMatrixInto(val,target):

    try:
        import System.Xml
    except:
        import clr 
        clr.AddReference("System.Xml")
    from System.Xml.Serialization import XmlSerializer

    ser = XmlSerializer(val.GetType())
    import System.IO
    stream = System.IO.MemoryStream()
    ser.Serialize(stream,val)
    stream.Seek(0, System.IO.SeekOrigin.Begin)
    System.Xml.XmlReader r = System.Xml.XmlReader(stream);
    target.ReadXml(r);
    stream.Close()
    return target
def newMatrix(Shape):  
    #Create a new Matrix containing a top and side group, and one member in each.
    from Forgetdata import Matrix
    topAxis = Matrix.CAxisMap()
    sideAxis= Matrix.CAxisMap()
    matrixData = Matrix.CMatrixData(sideAxis,topAxis)
    matrix = Matrix.CMatrix(None,matrixData,Matrix.CHeaderFooter(),Matrix.CHeaderFooter())
    return matrix
    
def addToMatrix(Shape,matrix):
    #Add a top group and side group, and add a new member on top/side
    if matrix.TopAxis.Groups.Count == 0: 
        matrix.TopAxis.Groups.AddNew(None,"","")
        newMember = matrix.TopAxis.Groups[0].AddNewMember(str(1),"",True,False)
        matrix.TopAxis.DataMembers.Add(newMember)
    if matrix.SideAxis.Groups.Count == 0: 
        matrix.SideAxis.Groups.AddNew(None,"","")
        newMember = matrix.SideAxis.Groups[0].AddNewMember(str(1),"",True,False)
        matrix.SideAxis.DataMembers.Add(newMember)

    #Add the necessary number of rows/columns based on the underlying Ppt shape.
    #If Shape is Chart
    if Shape.HasChart==-1:  #  shape is a chart 
        makeRowsAndColumns(matrix,Shape.Chart.SeriesCollection().Count,Shape.Chart.SeriesCollection(1).XValues.Count)  
        addRowsColumnsAndDataValues(matrix,Shape)
    #If Shape is Table           
    if Shape.HasTable ==-1: #  shape is a Table 
        makeRowsAndColumns(matrix,Shape.Table.Rows.Count-1,Shape.Table.Columns.Count-1)  # Number of Rows/Columns -1 for tables to allow for Labels.
        addRowsColumnsAndDataValues(matrix,Shape)
    #If Text Shape
    if Shape.HasTextFrame ==-1:  #  shape is a Text Shape.
        matrix.Label=Shape.TextFrame.TextRange.Text
    return matrix
    
def makeRowsAndColumns(matrix,numRows,numColumns):
    #Make the number of rows and columns needed for the PreFillMatrix, based on the underlying Data Table from the Chart or Table.
    for i in range(1, numRows):   #insert the number of rows needed
        matrix.InsertBlankRowAfter(matrix.SideAxis.DataMembers[0],"","Y Values")
    for i in range(1, numColumns):#insert the number of columns needed 
        matrix.InsertBlankColumnAfter(matrix.TopAxis.DataMembers[0],"","X Values")

def addRowsColumnsAndDataValues(matrix,Shape):
    j=0
    for row in matrix:
        i=0
        for col in row:
            #Set where to get the column/row labels and values from for Charts/Tables.
            if Shape.HasChart==-1: 
                columnLabel=Shape.Chart.SeriesCollection(1).XValues[i]
                rowLabel=Shape.Chart.SeriesCollection(j+1).Name
                value=Shape.Chart.SeriesCollection(j+1).Values[i]
            if Shape.HasTable ==-1: 
                columnLabel=Shape.Table.Cell(1,i+2).Shape.TextFrame.TextRange.Text
                rowLabel=cell=Shape.Table.Cell(j+2,1).Shape.TextFrame.TextRange.Text
                value=str(Shape.Table.Cell(j+2,i+2).Shape.TextFrame.TextRange.Text)
                    
            #Set the row/column labels and values into the matrix.
            col.TopMember.Label = columnLabel # Set the column headings to the category labels.
            matrix[j][i].AddValue("") #Create an item in the cell, and then add the values from the underlying table to this cell.
            #Use.NumericValue for Charts and .Value for Tables.  
            if Shape.HasChart ==-1:
                try:
                    matrix[j][i][0].NumericValue =value # values from Chart  
                except:
                    pass
            if Shape.HasTable ==-1:
                try:
                    matrix[j][i][0].Value =value # values from Table   
                except:
                    pass
            #format the data to match the underlying NumberFormat from the Axis.
            #  if data labels are present, use them to determine the format.
            if Shape.HasChart ==-1:
                if Shape.Chart.SeriesCollection(j+1).HasDataLabels == True:
                    try:
                        matrix[j][i][0].FormatString = Shape.Chart.SeriesCollection(j+1).Points(i+1).DataLabel.NumberFormat
                    except:
                        pass
                #  if not, then use the TickLabels from the underlying axis (primary/Secondary), and if neither present, then present the NumericValue.
                else:
                    try:
                        if Shape.Chart.SeriesCollection(j+1).AxisGroup ==2:
                            matrix[j][i][0].FormatString =  Shape.Chart.Axes(2,2).TickLabels.NumberFormat  # this formats the secondary axis  (Chart.Axes(xlValue,xlSecondary)
                        else:
                            matrix[j][i][0].FormatString =  Shape.Chart.Axes(2,1).TickLabels.NumberFormat  # this formats the primary axis (Chart.Axes(xlValue,xlPrimary)
                    except:
                        pass
            i+=1
        row.Member.Label = rowLabel  # series
        j+=1
    #Set the Group and Matrix Labels 
    try:
        matrix.Label = Shape.Chart.ChartTitle.Text
    except:
        pass
    try:
        matrix.TopAxis.Groups[0].Label = Shape.Chart.Axes(1).AxisTitle.Text
    except:
        pass
    try:
        matrix.SideAxis.Groups[0].Label = Shape.Chart.Axes(2).AxisTitle.Text
    except:
        pass 

if __name__ == '__main__':
    ar = ActionRunner()
        



