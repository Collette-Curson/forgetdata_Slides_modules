def ShapeOverLastDataPoint(shapeToAlign,chartName):

# Place a text shape over the last data points on a line chart, and line it up with the highest and lowest score in that week.

# First of all we will move the existing shape to line up with the last data points.
    chart = shapeToAlign.Parent.Shapes.Item(chartName)
   
    numSeries = chart.Chart.SeriesCollection().Count
    numCategories = chart.Chart.SeriesCollection(numSeries).Points().Count

    shapeToAlign.Left = chart.Left + chart.Chart.PlotArea.InsideLeft + (numCategories-1) * chart.Chart.PlotArea.InsideWidth / (numCategories) 

# Next we will find the highest and lowest data points in the last data points per series, and set the shape Top and Height accordingly.

    highest=0
    lowest=1000

    series = chart.Chart.SeriesCollection().Count
    for hPoint in range(1,series):
        ser=chart.Chart.SeriesCollection(hPoint)
        pt=ser.Points(numCategories)    #last data point for each series.

        if (highest < ser.Values[numCategories]):  #set highest to highest last data point.  
            highest =ser.Values[numCategories]
            high = hPoint

        if (lowest > ser.Values[numCategories]):   #set lowest to lowest last data point.
            lowest = ser.Values[numCategories]
            low = hPoint

# Next we will set the Top and Height for the shape so that the shape sits over the scores for the highest and lowest for the last data points in each series.

    shapeToAlign.Top =  (chart.Top + chart.Chart.PlotArea.InsideTop) + ((chart.Chart.PlotArea.Height/chart.Chart.Axes(2).MaximumScale)*(chart.Chart.Axes(2).MaximumScale-highest))
    bottom=(chart.Top + chart.Chart.PlotArea.InsideTop) + ((chart.Chart.PlotArea.Height/chart.Chart.Axes(2).MaximumScale)*(chart.Chart.Axes(2).MaximumScale-lowest))
    shapeToAlign.Height =  bottom-shapeToAlign.Top
