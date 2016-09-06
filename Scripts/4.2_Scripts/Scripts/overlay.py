def TopNStackedColumnAlign(shapeToAlign,chartName, categoryNumber,topN):

   
    chart = shapeToAlign.Parent.Shapes.Item(chartName)

    numSeries = chart.Chart.SeriesCollection().Count
    if(numSeries < topN):
        return
    numCategories = chart.Chart.SeriesCollection(numSeries).Points().Count
    if(numCategories < categoryNumber):
        return
    
    shapeToAlign.Left = chart.Chart.PlotArea.InsideLeft + categoryNumber * chart.Chart.PlotArea.InsideWidth / numCategories
    
    shapeToAlign.Top = chart.Top - chart.Chart.PlotArea.Top
    
    shapeToAlign.Width = chart.Chart.PlotArea.InsideWidth / numCategories - chart.Chart.ChartGroups(1).GapWidth/2
 

def TopNStackedBarAlign(shapeToAlign,chartName, categoryNumber, topN):
    chart = shapeToAlign.Parent.Shapes.Item(chartName)
    
    numSeries = chart.Chart.SeriesCollection().Count
    if(numSeries < topN):
        return
    numCategories = chart.Chart.SeriesCollection(numSeries).Points().Count
    if(numCategories < categoryNumber):
        return
    
    shapeToAlign.Left = chart.Left + chart.Chart.PlotArea.InsideLeft + categoryNumber * chart.Chart.PlotArea.InsideWidth / numCategories
    
    shapeToAlign.Top = chart.Chart.SeriesCollection(numSeries).Points(categoryNumber).Top + chart.Top
    
    shapeToAlign.Height = chart.Chart.SeriesCollection(numSeries).Points(categoryNumber).Height + chart.Chart.SeriesCollection(numSeries - topN +1).Points(categoryNumber).Height    
    
def GenerateOverlayAxisLabels():
    
    from globals import *
    from Microsoft.Office.Interop.PowerPoint import XlAxisType
    from Microsoft.Office.Interop.PowerPoint import XlAxisGroup
    
    
   
    
    if(Chart.SeriesCollection().Count == 0):
        return
    
    axis = Chart.Axes(XlAxisType.xlCategory)
    
    categories = Chart.SeriesCollection(1).XValues
    #categories = axis.CategoryNames
    
    chartShape = Chart.Parent
    
    slide = chartShape.Parent

    templateAxisLabelName = chartShape.Name + "AL"
    
    heightPerLabel = Chart.PlotArea.InsideHeight / categories.Count
    firstCategoryPosition = chartShape.Top + Chart.ChartArea.Top + Chart.PlotArea.InsideTop
    leftPosition = chartShape.Left + Chart.ChartArea.Left + Chart.PlotArea.InsideLeft
    
    
    for iPoint in range(0,categories.Count):
        axisLabelName = templateAxisLabelName + str(iPoint)
        labelShape = FindShape(slide.Shapes,axisLabelName)
        
        
        
         # assume a normal ordering of bottom to top
        top = 0
        if(axis.ReversePlotOrder):
            top = firstCategoryPosition + iPoint * heightPerLabel
        else:
            pointRelPos = categories.Count - (iPoint +1)            
            top = firstCategoryPosition + pointRelPos * heightPerLabel
        
        if(labelShape == None):
            labelShape = slide.Shapes.AddTextbox(1,45,top,leftPosition-45,heightPerLabel)
            labelShape.Name = axisLabelName
            labelShape.TextFrame.AutoSize = 0 # do not autosize
            labelShape.TextFrame.VerticalAnchor = 3 #Middle
            labelShape.TextFrame.TextRange.ParagraphFormat.AlignMent = 3 #right
        else:
            labelShape.Top = top
            
        labelShape.TextFrame.TextRange.Text = categories[iPoint]
        
    for ibox in range(categories.Count, 1000):
        axisLabelName = templateAxisLabelName + str(ibox)
        labelShape =FindShape(slide.Shapes,axisLabelName)
        if(labelShape != None):
            labelShape.Delete()
        else:
            break

def GenerateOverlayAxisLabels2():
    
    from globals import *
    from Microsoft.Office.Interop.PowerPoint import XlAxisType
    from Microsoft.Office.Interop.PowerPoint import XlAxisGroup
    
    
   
    
    if(Chart.SeriesCollection().Count == 0):
        return
    
    axis = Chart.Axes(XlAxisType.xlCategory)
    
    categories = Chart.SeriesCollection(1).XValues
    #categories = axis.CategoryNames
    
    chartShape = Chart.Parent
    
    slide = chartShape.Parent

    templateAxisLabelName = chartShape.Name + "AL"
    
    heightPerLabel = Chart.PlotArea.InsideHeight / categories.Count
    firstCategoryPosition = chartShape.Top + Chart.ChartArea.Top + Chart.PlotArea.InsideTop
    leftPosition = chartShape.Left + Chart.ChartArea.Left + Chart.PlotArea.InsideLeft
    
    
    for iPoint in range(0,categories.Count):
        axisLabelName = templateAxisLabelName + str(iPoint)
        labelShape = FindShape(slide.Shapes,axisLabelName)
        
        
        
         # assume a normal ordering of bottom to top
        top = 0
        if(axis.ReversePlotOrder):
            top = firstCategoryPosition + iPoint * heightPerLabel
        else:
            pointRelPos = categories.Count - (iPoint +1)            
            top = firstCategoryPosition + pointRelPos * heightPerLabel
        
        if(labelShape == None):
            labelShape = slide.Shapes.AddTextbox(1,45,top,leftPosition-45,heightPerLabel)
            labelShape.Name = axisLabelName
            labelShape.TextFrame.AutoSize = 0 # do not autosize
            labelShape.TextFrame.VerticalAnchor = 3 #Middle
            labelShape.TextFrame.TextRange.ParagraphFormat.AlignMent = 3 #right
        else:
            labelShape.Top = top

        cleanHeaders = Matrix.Header.Center.lstrip()
        headers =cleanHeaders.split("\n")
       
        if iPoint< categories.Count-1:
          headers[iPoint] =headers[iPoint][:-24]    
        else:
          headers[iPoint] =headers[iPoint][:-21]   # remove last 24 characters from text of each line, eg : Level of agreement, remove last 21 characters from text when on last series.

        labelShape.TextFrame.TextRange.Text = headers[iPoint]

    for ibox in range(categories.Count, 1000):
        axisLabelName = templateAxisLabelName + str(ibox)
        labelShape =FindShape(slide.Shapes,axisLabelName)
        if(labelShape != None):
            labelShape.Delete()
        else:
            break

    
def GenerateOverlayNestedAxisLabels(NumberOfInnerLevelCategories):

    from globals import *
    from Microsoft.Office.Interop.PowerPoint import XlAxisType
    from Microsoft.Office.Interop.PowerPoint import XlAxisGroup
    
    if(Chart.SeriesCollection().Count == 0):
        return
    
    axis = Chart.Axes(XlAxisType.xlCategory)
    
    categories = Chart.SeriesCollection(1).XValues
    #categories = axis.CategoryNames
    outercategories = (categories.Count+1)/NumberOfInnerLevelCategories 
    
    chartShape = Chart.Parent
    
    slide = chartShape.Parent

    templateAxisLabelName = chartShape.Name + "ALX"
    
    heightPerLabel = (Chart.PlotArea.InsideHeight/categories.Count) * (categories.Count+1) /outercategories      # calculated for outer category labels.
    heightOfLabel = heightPerLabel *((float(NumberOfInnerLevelCategories)-1)/(float(NumberOfInnerLevelCategories)))    # calculated as height *2/3
    firstCategoryPosition = chartShape.Top + Chart.ChartArea.Top + Chart.PlotArea.InsideTop
    leftPosition = chartShape.Left + Chart.ChartArea.Left 
    try:
        shape = FindShape(slide.Shapes, chartShape.Name + "AL")
        width = leftPosition - shape.Left  
    except:
        width =  100
    
    for iPoint in range(0,outercategories):
        axisLabelName = templateAxisLabelName + str(iPoint)
        labelShape = FindShape(slide.Shapes,axisLabelName)
        
         # assume a normal ordering of bottom to top
        top = 0
        if(axis.ReversePlotOrder):
            top = firstCategoryPosition + iPoint * heightPerLabel
        else:
            pointRelPos = outercategories - (iPoint +1)            
            top = firstCategoryPosition + pointRelPos * heightPerLabel
        
        if(labelShape == None):
            labelShape = slide.Shapes.AddTextbox(1, leftPosition, top, width, heightOfLabel)
            labelShape.Name = axisLabelName
            labelShape.TextFrame.AutoSize = 0 # do not autosize
            labelShape.TextFrame.VerticalAnchor = 3 #Middle
            labelShape.TextFrame.TextRange.ParagraphFormat.AlignMent = 3 #right
        else:
            labelShape.Top = top
           
        labelShape.TextFrame.TextRange.Text = Matrix.TopAxis.Groups[iPoint].Label

    for ibox in range(outercategories, 1000):
        axisLabelName = templateAxisLabelName + str(ibox)
        labelShape =FindShape(slide.Shapes,axisLabelName)
        if(labelShape != None):
            labelShape.Delete()
        else:
            break

def FindShape(Shapes,shapeName):
    if(Shapes == None):
        return None
    
    for shape in Shapes:
        if(shape.Name == shapeName):
            return shape
        
    return None