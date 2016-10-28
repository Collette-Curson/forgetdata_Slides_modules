"""Provides backwards compatibility support for modules that were 
released with Slides 4.2. 

"""

#from Transformations.sorting module
def SortRows(byColumn = 0, usingCellValue = 0, descending = True, Matrix = None):
    """Adding Backwards compatibility support for v4.2 script
    
    Support for sorting rows using transformations.sorting.sort_rows()
    
    Note: after 4.2 sorting within Nets has been added, and therefore this will
    give a different result if nets are found.
    
    """
    
    if Matrix == None:
        from globals import Matrix 
    import transformations as tr
    
    cl = tr.MatrixManipulator(Matrix)
    cl.sort_rows(by_column = byColumn, using_cell_value = usingCellValue, descending = descending)

def SortColumns(byRow = 0, usingCellValue = 0, descending = True, Matrix = None):
    """Adding Backwards compatibility support for v4.2 script
    
    Support for sorting rows using transformations.sorting.sort_columns()
    
    Note: after 4.2 sorting within Nets has been added, and therefore this will
    give a different result if nets are found.
    
    """
    
    if Matrix == None:
        from globals import Matrix 
    import transformations as tr
    
    cl = tr.MatrixManipulator(Matrix)
    cl.sort_columns(by_row = byRow, using_cell_value = usingCellValue, descending = descending)

#end of Transformations.sorting module
#from Transformations.base_summaries Module

def BaseSummaryToSeriesHeadings(Matrix=None):
    """Adding Backwards compatibility support for v4.2 script
    
    Use transformations.series.set_series_base_summary()
    
    """
    
    if Matrix == None:
        from globals import Matrix 
    import transformations as tr
    
    x = tr.MatrixManipulator(Matrix)
    x.set_series_base_summary()
    

def BaseSummaryToCategoryHeadings(Matrix=None):
    """Adding Backwards compatibility support for v4.2 script
    
    Use transformations.categories.set_category_base_summary()
    
    """
    
    if Matrix == None:
        from globals import Matrix 
    import transformations as tr
    
    x = tr.MatrixManipulator(Matrix)
    x.set_category_base_summary()
    
def BaseSummaryToTableRows(Matrix=None):
    """Adding Backwards compatibility support for v4.2 script
    
    Use transformations.labels.format_labels

    """
    
    if Matrix == None:
        from globals import Matrix     
    from transformations.labels.format_labels import FormatSettings
    
    settings = FormatSettings(label_format="(n={0[0].Value})")
    for r in Matrix:
        r.Member.Label = settings.label_format(r[0]) if r[0].Count > 0 else ""    
    #Matrix.DeleteColumn(0)

#end of Transformations.base_summaries module
#from Transformations.compute.py

def ColumnDifference(x,y,Matrix=None):
    """Adding Backwards compatibility support for v4.2 script
    
    Use transformations.data.category_difference()
    
    """
    
    if Matrix == None:
        from globals import Matrix 
    import transformations as tr
    
    m = tr.MatrixManipulator(Matrix)
    m.category_difference(x,y)
    
    #4.2 script calculates diff as a number, not as percentage. 
    for r in Matrix:
        r[y+1][0].Value = str(r[y+1][0].GetNumericValue() * 100)
        #r[y+1][0].FormatString = "0"

def RenumberSigTests(Matrix = None):
    """Adding Backwards compatibility support for v4.2 script
    
    Use transformations.data.renumber_sig_tests()
    
    """
    
    if Matrix == None:
        from globals import Matrix 
    import transformations as tr
    
    m = tr.MatrixManipulator(Matrix)
    m.renumber_sig_tests() 
    
def TopNSummary(N, Matrix = None):
    """Adding Backwards compatibility support for v4.2 script
    
    Use transformations.series.insert_topN_into_series(N)
    
    """
    
    if Matrix == None:
        from globals import Matrix 
    import transformations as tr
    from transformations.utils.logger import logger
    
    #do not run if N too big.
    if (Matrix.Count < N):
        logger("Not enough rows in table to insert a Top " + str(N) + " series")
        return

    m = tr.MatrixManipulator(Matrix) 
    m.insert_topN_into_series(N)
    
    #v4.2 script inserted the row into a different position, 
    #This is placeing the inserted row at the end of the Matrix.
    newRow = Matrix.InsertBlankRowAfter(Matrix.SideAxis.DataMembers[Matrix.Count-1], "TopN", "Top " + str(N))
    Matrix.SwitchRows(0, Matrix.Count-1)
    Matrix.DeleteRow(0)
    
def NumberDownbreaks(delimiter, Matrix = None):
    """Adding Backwards compatibility support for v4.2 script
    
    Use transformations.series.number_series()
    
    """
    
    if Matrix == None:
        from globals import Matrix 
    import transformations as tr
    
    x = tr.MatrixManipulator(Matrix)
    x.number_series(delimiter)    

#end of Transformations.compute module
#from Transformations.csvvalues.py    

def GetCsvVal(file, name):
    """Adding Backwards compatibility support for v4.2 script
    
    Use transformations.utils.utilities.read_comma_separated_file(_file_name,val)
    
    """
    
    from transformations.utils.utilities import read_comma_separated_file
    
    return read_comma_separated_file(file,name)

#end of Transformations.csvvalues module    
#from Transformations.manipulate.py

def InsertColumn(colIndex, name = "", label = "", Matrix = None):
    """Adding Backwards compatibility support for v4.2 script
    
    Use transformations.categories.insert_category()
    
    """
    
    if Matrix == None:
        from globals import Matrix 
    import transformations as tr
    x = tr.MatrixManipulator(Matrix)
    x.insert_category(column_number = colIndex, label = label)    

def InsertRow(rowIndex, name = "", label = "", Matrix = None):
    """Adding Backwards compatibility support for v4.2 script
    
    Use transformations.series.insert_series()
    
    """
    
    if Matrix == None:
        from globals import Matrix 
    import transformations as tr
    
    x = tr.MatrixManipulator(Matrix)
    x.insert_series(row_number = rowIndex, label = label)
    
''' 
# InsertColumn was duplicated in 4.3., so this one is commented out
def InsertColumn(colIndex, name = "", label = "", Matrix = None):
    """Adding Backwards compatibility support for v4.2 script
    
    Use transformations.categories.insert_category()
    
    """
    
    if Matrix == None:
        from globals import Matrix 
    import transformations as tr
    
    x = tr.MatrixManipulator(Matrix)
    x.insert_category(col_number = colIndex, label = label)
'''

def UngroupRows(Matrix = None):
    """Adding Backwards compatibility support for v4.2 script
    
    Use transformations.data.make_series_from_grid_slices()
    
    """
    
    if Matrix == None:
        from globals import Matrix 
    import transformations as tr
    
    x = tr.MatrixManipulator(Matrix)
    x.make_series_from_grid_slices()
        
#end of Transformations.manipulate module
#from Transformations.merge module

def MergeRowsByLabel(Matrix = None):
    """Adding Backwards compatibility support for v4.2 script
    
    Use transformations.data.merge_series_by_label()
    
    """
    
    if Matrix == None:
        from globals import Matrix 
    import transformations as tr
    
    x = tr.MatrixManipulator(Matrix)
    x.merge_series_by_label()
    
def MergeColumnsByLabel(Matrix = None):
    """Adding Backwards compatibility support for v4.2 script
    
    Use transformations.data.merge_categories_by_label()
    
    """
    
    if Matrix == None:
        from globals import Matrix 
    import transformations as tr
    
    x = tr.MatrixManipulator(Matrix)
    x.merge_categories_by_label()
    
#end of Transformations.merge module    
#from Transformations.numberstatements module

def NumberStatementsInMatrix(Matrix = None):
    """Adding Backwards compatibility support for v4.2 script
    
    Use transformations.series.number_series()
    
    """
    
    if Matrix == None:
        from globals import Matrix 
    import transformations as tr
    
    x = tr.MatrixManipulator(Matrix)
    x.number_series(". ")
    
def SetMatrixLabelToStatement(whichstatement, Matrix = None):
    """Adding Backwards compatibility support for v4.2 script"""
    
    if Matrix == None:
        from globals import Matrix 
    Matrix.Label = Matrix[whichstatement-1].Member.Label
    
#end of Transformations.numberstatements module

#from Transformations.backgrounds module

def SetBgImageAndSize(fileName, Shape = None):
    """Adding Backwards compatibility support for v4.2 script"""
    
    from texts import set_bg_image_and_size
    
    set_bg_image_and_size(fileName, Shape)
    
def GetPptImageSize(fileName, Shape = None):
    """Adding Backwards compatibility support for v4.2 script"""   
    
    from texts import _get_ppt_image_size

    return _get_ppt_image_size(fileName, Shape)

def SetBgImage(fileName, Shape = None):
    """Adding Backwards compatibility support for v4.2 script"""
    
    from texts import set_bg_image
    
    set_bg_image(fileName, Shape)
    
def SetBgPictureCenter(Shape,fileName):
    """Adding Backwards compatibility support for v4.2 script"""
    
    from texts import set_bg_picture_center_tile
    
    set_bg_picture_center_tile(fileName, Shape)
    
def SetBackgroundColor(Shape,red,green,blue):
    """Adding Backwards compatibility support for v4.2 script"""
    
    from shapes import set_background_color
    
    set_background_color(Shape,red,green,blue)
    
def RGB(r,g,b):
    """Adding Backwards compatibility support for v4.2 script"""
    
    from shapes import RGB as RGB2
    
    return RGB2(r,g,b)

def FindShape(Shapes, shape_name):
    """Adding Backwards compatibility support for v4.2 script"""
    
    from shapes import find_shape
    
    return find_shape(Shapes, shape_name)

#end of Transformations.backgrounds module
#from of overlay module

def _move_topN_shape(Chart, Shape, column_number):
    """Move shape to the correct location on the Chart"""
    
    from transformations.utils.logger import logger
    
    number_series = Chart.SeriesCollection().Count
    number_categories = Chart.SeriesCollection(number_series).Points().Count
    axis = Chart.Axes(1)
    
    #column clustered or stacked
    _column_list = [51, 52, 53]
    _bar_list = [57, 58, 59]
    if Chart.ChartType in _column_list: 
        Shape.Width = Chart.PlotArea.InsideWidth / number_categories
        Shape.Height = Chart.PlotArea.Height / number_series
        Shape.Top =    Chart.PlotArea.Top - Shape.Height
        
        if axis.ReversePlotOrder:
            Shape.Left =  Chart.ChartArea.Left + Chart.PlotArea.InsideLeft + (number_categories - column_number+1) * Shape.Width
        else: 
            Shape.Left =  Chart.ChartArea.Left + Chart.PlotArea.InsideLeft + (column_number) * Shape.Width

    # bar clustered or stacked
    elif Chart.ChartType in _bar_list: 
        Shape.Height = Chart.PlotArea.InsideHeight / number_categories 
        Shape.Left = Chart.PlotArea.Left + Chart.PlotArea.Width
        Shape.Width = Chart.PlotArea.Width / number_series
        if axis.ReversePlotOrder:
            Shape.Top =  Chart.PlotArea.InsideTop + Chart.ChartArea.Top + ((column_number) * Shape.Height)
        else:
            Shape.Top =  Chart.PlotArea.InsideTop + Chart.ChartArea.Top + ((number_categories - column_number-1) * Shape.Height)
    else:
        logger(str(Chart.ChartType) + ": Cannot add TopN to this chart type")
    
def TopNStackedColumnAlign(shapeToAlign, chartName, categoryNumber, topN):
    """Adding Backwards compatibility support for v4.2 script.
    
    As an alternative, use the following, which can be called once per chart:
    
    charts.make_topN_shapes_on_chart(Chart, Matrix, list_of_topN_scores)
    
    """
    
    shape = FindShape(chartName.Shapes, shapeToAlign)
    if shape:
        _move_topN_shape(chartName, shape, categoryNumber)
        shape.TextFrame.TextRange.Text = topN
    
def TopNStackedBarAlign(shapeToAlign, chartName, categoryNumber, topN):
    """Adding Backwards compatibility support for v4.2 script.
    
    As an alternative, use the following, which can be called once per chart:
    
    charts.make_topN_shapes_on_chart(Chart, Matrix, list_of_topN_scores)
    
    """
     
    shape = FindShape(chartName.Shapes, shapeToAlign)
    if shape:
        _move_topN_shape(chartName, shape, categoryNumber)
        shape.TextFrame.TextRange.Text = topN                                            
            
def GenerateOverlayAxisLabels(Chart = None):
    """Adding Backwards compatibility support for v4.2 script.
    
    NOTE: This script will add the shapes within the chart shape, rather than as
    independent shapes on the slide.
    
    """
    
    if Chart is None:
        from globals import Chart
    
    from charts import add_axis_labels_to_bar_chart
    add_axis_labels_to_bar_chart(Chart)
    

# Support not added for GenerateOverlayAxisLabels2 as this was specific to our
# sample data

# Support not added for GenerateOverlayNestedAxisLabels as it didnt work well as
# a general script. 

#end of overlay module

#from overlaywithlinechart Module

# Support not added for ShapeOverLastDataPoint as it didnt work well as a 
# general script.

#end of overlaywithlinechart module

# from trafficlights module

def SetTrafficLights(greenLimit, yellowLimit, file_name_list = None, Matrix = None):
    """Adding Backwards compatibility support for v4.2 script.
    
    NOTE: This script will add the shapes within the chart shape, rather than as
    independent shapes on the slide.
    
    """
    
    from texts import set_image_based_on_limit
    from System.IO import Path
    
    my_dir = Path.GetDirectoryName(__file__) #relative to the module file
    
    image_path = my_dir + "\\transformations\\utils\\images"
    
    if file_name_list is None:
        file_name_list = [image_path + "\\traffic-light-green.jpg", image_path + "\\traffic-light-yellow.jpg", image_path + "\\traffic-light-red.jpg"]
            
    set_image_based_on_limit(greenLimit, yellowLimit, file_name_list)
    
def SetTrafficLightsFromMatrix(selectrow, selectcolumn, green_limit, 
                               yellow_limit, Table = None, Matrix = None, 
                               image_list = None):
    """Adding Backwards compatibility support for v4.2 script.
    
    This script will update all shapes within the last column of the table, 
    rather than one at a time.
    
    """
    
    if Matrix is None:
        from globals import Matrix
    if Table is None:
        from globals import Table
    if image_list is None:
        from System.IO import Path
        _my_dir = Path.GetDirectoryName(__file__) #relative to the module file
        _image_path = _my_dir + "\\transformations\\utils\\images\\"
        image_list = list()
        image_list.append(_image_path+"\\images\\greenarrow.png")
        image_list.append(_image_path+"\\images\\greyarrow.png")
        image_list.append(_image_path+"\\images\\redarrow.png")
        
    from texts import set_image_in_table_column_based_on_limit
    set_image_in_table_column_based_on_limit(Table, Matrix, image_list, green_limit, yellow_limit) 