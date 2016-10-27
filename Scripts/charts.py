"""Provides a series of functions which will run against Chart shapes within
PowerPoint, after the Chart Shape has been filled.

"""
from cPickle import HIGHEST_PROTOCOL

__version__ = '4.3.0'

def set_colors_on_chart(Chart, Matrix, fileName=None):
    """Assign a specific color to each brand within a column, bar, pie, line
    chart, based upon values in an input text file.

    This function is often used when a chart has been sorted as the display
    order will be updated between refreshes of data.
    
    :param Chart: Chart shape
    :param Matrix: Matrix associated with the Chart
    :param fileName: path and file containing the brands and colours to be used
                   for the chart series.

    The script expects an input file to be passed as a parameter, or else will
    use "colors.txt" in the same folder as the pptx file, and contains the
    following format:

    "Brand Name",Red,Green,Blue.

    Example:
    
    | colors.txt contains:
    |
    | "Brand name 1",0,154,130
    | "Brand name 2",0,131,190
    | "Brand name 3",154,158,31
    | "Brand name 4",170,22,62
    | 
    | set_colors_on_chart(Chart, Matrix, colors.txt)
            
    """

    from globals import Log
    from shapes import RGB

    def _make_color_dict_for_series():
        """Return a dictionary of colours to set on chart based on Series"""

        def _get_csv_value(label):
            """Return the RGB value for the label from csv txt file."""

            import _csv
            global _f
            _f = _csv.reader(open(fileName, "r"))
            for _row in _f:
                if(label == _row[0]):
                    _r = int(_row[1])
                    _g = int(_row[2])
                    _b = int(_row[3])
                    return str(RGB(_r, _g, _b))
            return

        _colors = dict()

        try:
            _series_count = Chart.SeriesCollection().Count
        except:
            try: # unit tests where chart has come from python-pptx
                _series_count = chart.series.__len__()
            except:
                _series_count = 0
                
        if _series_count > 1:  # This is a multi series chart

            # for each brand column, look up the csv file, return the RGB value
            for _item in Matrix.SideAxis.DataMembers:
                if _get_csv_value(_item.Label) is not None:
                    _colors[_item.Label] = _get_csv_value(_item.Label)
                else:
                    Log.Info("There is no color match for label " + _item.Label)
        else:  # This is a single series chart, eg pie.

            # for each brand column, look up the csv file, return the RGB value
            for _item in Matrix.TopAxis.DataMembers:
                if _get_csv_value(_item.Label) is not None:
                    _colors[_item.Label] = _get_csv_value(_item.Label)
                else:
                    try:
                        Log.Info("There is no color match for label " + _item.Label)
                    except:
                        print "There is no color match for label " + _item.Label
        try:
            Log.Info("Brands and colors: " + str(_colors))
        except:
            print "Brands and colors: " + str(_colors)

        return _colors

    def _set_colours():
        """Set the colour onto the chart"""
        
        _series_collections = Chart.SeriesCollection()
        
        # pie chart - one series
        if _series_collections.Count == 1:
            _xVals = Chart.SeriesCollection(1).XValues
            _matching = [_item for _item in _xVals if _item in _color_dict.keys()]
            _series = _series_collections(1)
            counter = 1
            for _item in _xVals:
                if _item in _matching:
                    _point = _series.Points(counter)
                    _format = _point.Format
                    _fill = _format.Fill
                    _fill.Visible = 1
                    _foreColor = _fill.ForeColor
                    _foreColor.RGB = int(_color_dict[_item])
                    _point.Border.Color = int(_color_dict[_item])
                counter += 1
        else:
            # Loop through SeriesCollection
            for _iSeries in range(1, _series_collections.Count + 1):
                _series = _series_collections.Item(_iSeries)
                _xVals = _series.XValues
                if _series.Name in _color_dict.keys():

                    # This is a multi series chart. Colour entire series.
                    _format = _series.Format
                    _fill = _format.Fill
                    _fill.Visible = 1
                    _foreColor = _fill.ForeColor
                    # bar
                    _foreColor.RGB = int(_color_dict[_series.Name])
                    # line
                    _col = _color_dict[_series.Name]
                    try:
                        _series.MarkerBackgroundColor = int(_col)
                        _series.MarkerForegroundColor = int(_col)
                    except:
                        pass
                    _series.Border.Color = int(_col)

        Log.Info("Updated colours for chart")

    if (fileName is None):
        fileName = colors.txt

    _color_dict = _make_color_dict_for_series()
    _set_colours()


def convert_glyphs_to_color_wingdings(Chart, Matrix=None):
    r"""Convert your significant results into up and down arrows within the
    chart.

    :param Chart: Chart shape
    
    Used in conjunction with a script which sets the significant results to
    display the correct character values, chr(0xE9), chr(0xEA).
    
    For example, convert_significance_results_to_arrows() in
    "transformations\\data.py".

    """

    if Matrix is None:
        from globals import Matrix
    from globals import Log
    from shapes import RGB

    _series_collections = Chart.SeriesCollection()

    _significanceChars = [chr(0xE9), chr(0xEA)]
    for _iSeries in range(1, _series_collections.Count + 1):  # rows in Table

        _series = _series_collections.Item(_iSeries)  # rows in Table
        _xVals = _series.XValues  # columns
        _pointNumber = 1
        for _item in Matrix.TopAxis.DataMembers:  # columns
            _pt = _series_collections(_iSeries).Points(_pointNumber)
            _DataLabel = _pt.DataLabel.Text
            i = 1
            for character in _DataLabel:
                for sig in _significanceChars:
                    if sig == character:
                        _char = _pt.DataLabel.Characters(i, 1)
                        _char.Font.Name = "Wingdings"
                        _char.Font.Color = RGB(255, 255, 255)
                i += 1
            _pointNumber += 1
    Log.Info("Updated arrows to Wingdings")
    

def make_topN_shapes_on_chart(Chart, Matrix, list_of_topN_scores):
    """Make and align TopN text shapes within the chart to the top or side of
    each category column or bar, within a clustered or stacked chart.
    
    The topN text shape will be placed outside the top or side of the plot area, 
    within the chart shape.  
    
    :param Chart: Chart shape
    :param Matrix: Matrix associated with the Chart
    :param list_of_topN_scores: the Top N scores from either within the Matrix,
                                or calculated from existing rows of the Matrix.

    For example:
    
    | list_of_topN_scores = ['10.3%', '12.5%', '8.7%', '29.6%', '22.2%', '30.0%']
    | charts.make_topN_shapes_on_chart(Chart, Matrix, list_of_topN_scores)
    
    """
    
    def _del_topN_shapes():
        """Find all topN shapes on the Chart, and delete them so that old data
        will not be found after refresh

        """

        from shapes import find_shape

        for i in range(0,100):
            _shape_name = "TopN " + str(i)
            _shape = find_shape(Chart.Shapes, _shape_name)
            if _shape:
                _shape.Delete()

    _del_topN_shapes()
    _number_series = Chart.SeriesCollection().Count
    _number_categories = Chart.SeriesCollection(_number_series).Points().Count
    _axis = Chart.Axes(1)
    
    def _make_and_align_topN_shape(shape_name, column_number, topN_score):
        """Align TopN text shapes within the chart to the top of each category 
        column or bar within a clustered or stacked chart.

        :param shape_name: text shape on the chart
        :param column_number: which shape to move
        :param topN: the TopN value for that column

        This function assumes that the shape_name exists, and they are moved one 
        at a time using a script. For example:
    
        | list_of_topN_scores = ['10.3%', '12.5%', '8.7%', '29.6%', '22.2%', '30.0%']
        | for i in range(1,Matrix.TopAxis.DataMembers.Count + 1):
        |     shape_name = "Rectangle " + str(i)
        |     charts.align_topN_shape(shape_name, i,list_of_topN_scores[i])
      
        """

        def _make_topN_shape(shape_name):
            """Make the text shape for the Top N score"""
            
            _shape = Chart.Shapes.AddTextbox(1,45,0,10,10)
            _shape.Name = shape_name
            _shape.TextFrame.AutoSize = 0 # do not autosize
            _shape.TextFrame.VerticalAnchor = 3 #Middle
            _shape.TextFrame.TextRange.ParagraphFormat.AlignMent = 2
            _shape.TextFrame.TextRange.Text = topN_score
            return _shape        
        
        def _move_topN_shape(_shape):
            """Move shape to the correct location on the Chart"""
            
            #column clustered or stacked
            _column_list = [51, 52, 53]
            _bar_list = [57, 58, 59]
            if Chart.ChartType in _column_list: 
                _shape.Width = Chart.PlotArea.InsideWidth / _number_categories
                _shape.Height = Chart.PlotArea.Height / _number_series
                _shape.Top =    Chart.PlotArea.Top - _shape.Height
                
                if _axis.ReversePlotOrder:
                    _shape.Left =  Chart.ChartArea.Left + Chart.PlotArea.InsideLeft + (_number_categories - column_number+1) * _shape.Width
                else: 
                    _shape.Left =  Chart.ChartArea.Left + Chart.PlotArea.InsideLeft + (column_number) * _shape.Width

            # bar clustered or stacked
            elif Chart.ChartType in _bar_list: 
                _shape.Height = Chart.PlotArea.InsideHeight / _number_categories 
                _shape.Left = Chart.PlotArea.Left + Chart.PlotArea.Width
                _shape.Width = Chart.PlotArea.Width / _number_series
                if _axis.ReversePlotOrder:
                    _shape.Top =  Chart.PlotArea.InsideTop + Chart.ChartArea.Top + ((column_number) * _shape.Height)
                else:
                    _shape.Top =  Chart.PlotArea.InsideTop + Chart.ChartArea.Top + ((_number_categories - column_number-1) * _shape.Height )
            else:
                print str(Chart.ChartType) + ": Cannot add TopN to this chart type"

        #exit if the column number is > number of categories.
        if(_number_categories < column_number+1):
            return
        #move the new shape to the correct position on the chart. 
        _move_topN_shape(_make_topN_shape(shape_name))    

    for col in Matrix[0]:
        _index = col.TopMember.DataIndex
        _make_and_align_topN_shape("TopN " + str(_index), _index, 
                            list_of_topN_scores[_index])

def add_axis_labels_to_bar_chart(Chart = None):
    """On a Bar chart, generate text shapes within the Chart shape, to the left
    of the plot area, and place the labels of the axis within these shapes.
    This enables more formatting within the labels, for example,
    left/right/center justification.
    
    :param Chart: Chart shape, default = None
    
    """
    if Chart is None:
        from globals import Chart
    
    from Microsoft.Office.Interop.PowerPoint import XlAxisType
    from Microsoft.Office.Interop.PowerPoint import XlAxisGroup
    from shapes import find_shape
    
    if(Chart.SeriesCollection().Count == 0):
        return
    
    _axis = Chart.Axes(XlAxisType.xlCategory)
    _categories = Chart.SeriesCollection(1).XValues
    _template_axis_name = Chart.Name + "AL"  
    
    _height_per_label = Chart.PlotArea.InsideHeight / _categories.Count
    _first_category_position = Chart.PlotArea.InsideTop 
    _left_position = Chart.ChartArea.Left
    _width = Chart.PlotArea.InsideLeft - _left_position
    
    for i in range(0,_categories.Count):
        _axis_label_name = _template_axis_name + str(i)
        _shape = find_shape(Chart.Shapes, _axis_label_name)
        
        # assume a normal ordering of bottom to top
        _top = 0
        if(_axis.ReversePlotOrder):
            _top = _first_category_position + i * _height_per_label
        else:
            point_relative_position = _categories.Count - (i +1)            
            _top = _first_category_position + point_relative_position * _height_per_label
        
        
        if(_shape == None):
            # make new shape, AddTextbox(Orientation, Left, Top, Width, Height)
            _shape = Chart.Shapes.AddTextbox(1, _left_position, _top, _width, _height_per_label)
            _shape.Name = _axis_label_name
        else:
            # move existing shape.
            _shape.Left = _left_position
            _shape.Top = _top
            _shape.Width = _width
            _shape.Height = _height_per_label
        # format shape and set text
        _shape.TextFrame.AutoSize = 0 # do not autosize
        _shape.TextFrame.VerticalAnchor = 3 #Middle
        _shape.TextFrame.TextRange.ParagraphFormat.AlignMent = 3 #right
        _shape.TextFrame.TextRange.Text = _categories[i]
    
    #delete any additional shapes from previous refresh.
    for ibox in range(_categories.Count, 1000):
        _axis_label_name = _template_axis_name + str(ibox)
        _shape = find_shape(Chart.Shapes, _axis_label_name)
        if(_shape != None):
            _shape.Delete()
        else:
            break
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
