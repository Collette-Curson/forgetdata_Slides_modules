"""Provides a series of functions which will run against Text shapes within
PowerPoint, after the Text Shape has been filled.

"""

__version__ = '4.3.0'


def set_bg_image_and_size(_image_file_path, Shape=None):
    r"""Set the background of the shape to the image passed in, and resize.

    Example:

    | _image_file_path = "transformations\\utils\\images\\greenarrow.png"
    | set_bg_image_and_size(_image_file_path)

    """

    try:
        if Shape is None:
            from globals import Shape

        # calculate the actual size of the image in points as this is the unit
        # that PowerPoint uses
        size = _get_ppt_image_size(_image_file_path, Shape)

        # set the Background image of this shape to the _image_file_path
        set_bg_image(_image_file_path, Shape)

        # resize the shape to the width and height of the image, 
        # will fail if filling table.
        try:
            Shape.Width = size.Width
            Shape.Height = size.Height
        except:
            pass
        
        # set the text on the shape to blank
        Shape.TextFrame.TextRange.Text = ""

        return True
    except:
        raise


def _get_ppt_image_size(_image_file_path, Shape=None):
    r"""Return the Width and Height in points of the image passed in.

    Used by set_bg_image_and_size().

    Example:

    | _image_file_path = "transformations\\utils\\images\\greenarrow.png"
    | size=_get_ppt_image_size(_image_file_path)
    | print size.Width, size.Height

    """

    import clr
    clr.AddReference("System.Drawing")
    from System.Drawing import Image
    from System.Drawing import SizeF

    _im = Image.FromFile(_image_file_path)

    _size_px = _im.Size
    _vert_dpi = _im.VerticalResolution
    _horz_dpi = _im.HorizontalResolution
    _im.Dispose()

    # calculate the actual size of the image in points as this is the unit
    # that PowerPoint uses
    _width = 72 * float(_size_px.Width) / _horz_dpi
    _height = 72 * float(_size_px.Height) / _vert_dpi

    _size = SizeF(_width, _height)
    return _size


def set_bg_image(_image_file_path, Shape=None):
    r"""Sets the Background image of this shape to the _image_file_path.

    Used by set_bg_image_and_size.

    Example:

    | _image_file_path = "transformations\\utils\\images\\greenarrow.png"
    | set_bg_image(_image_file_path)

    """

    if Shape is None:
        from globals import Shape

    Shape.Fill.UserPicture(_image_file_path)


def set_bg_picture_center_tile(_image_file_path, Shape):
    r"""Centres the Background image within the shape, and tile.

    Rescale the image to the current shape.

    Example:

    | _image_file_path = "transformations\\utils\\images\\greenarrow.png"
    | set_bg_picture_center(Shape,_image_file_path)

    """

    from Microsoft.Office.Core import MsoTriState
    import clr
    clr.AddReference("System.Drawing")

    _pic_size = _get_ppt_image_size(_image_file_path)

    _box_height = Shape.Height
    _box_width = Shape.Width

    # heightScale is proportion of picture compared to box, eg if pic is
    # small, heightScale would be >1 (say 2.5). if pic is large,
    # heightScale would be <1 (say 0.75)
    _height_scale = _box_height / _pic_size.Height
    # widthScale is proportion of picture compared to box, eg if pic is
    # small, widthScale would be >1 (say 1.5). if pic is large,
    # widthScale would be <1 (say 0.50)
    _width_scale = _box_width / _pic_size.Width

    _image_scale = 1  # used if the image is smaller than the shape

    # if the picture proportions are larger than the shape
    if _height_scale < 1 or _width_scale < 1:
        # scale is set to the smaller value, eg 0.5
        _image_scale = min(_height_scale, _width_scale)
        Log.Info("image has been rescaled to fit within the shape")

    # This is used to center the image within the shape, and also tile
    # the image.   Its is a measure in pts.
    _width_calc = (1 - _pic_size.Width * _image_scale / _box_width)
    _height_calc = (1 - _pic_size.Height * _image_scale / _box_height)
    _width_offset = _width_calc / 2 * _box_width
    _height_offset = _height_calc / 2 * _box_height

    Shape.Fill.UserPicture(_image_file_path)
    # set the offset to center the image
    Shape.Fill.TextureOffsetX = _width_offset
    Shape.Fill.TextureOffsetY = _height_offset
    # Set the scale of the image to fit within the Shape.
    Shape.Fill.TextureHorizontalScale = _image_scale
    Shape.Fill.TextureVerticalScale = _image_scale

def set_image_based_on_limit(green_limit, yellow_limit, file_name_list, Matrix = None):    
    r"""Select which image to display based upon limits, for example a traffic 
    light system or up and down arrows.
    
    This should be run per text shape to set the background image and size 
    based on the image selected. 
    
    Example:
    
    | file_name_list = list()
    | file_name_list.append("traffic-light-green.jpg")
    | file_name_list.append("traffic-light-yellow.jpg")
    | file_name_list.append("traffic-light-red.jpg")
    | 
    | texts.set_image_based_on_limit(0.3, 0.2, file_name_list, Matrix)
    
    """
    
    if Matrix is None:
        from globals import Matrix
        
    _green_image = file_name_list[0]
    _yellow_image = file_name_list[1]
    _red_image = file_name_list[2]
    
    _value = Matrix[0][0][0].GetNumericValue()
    _image_to_use = _red_image
    if (_value  >= green_limit):
        _image_to_use = _green_image
    elif (_value >= yellow_limit):
        _image_to_use = _yellow_image
    try:
        set_bg_image_and_size(_image_to_use)
    except:
        # cannot find image, try standard utils\images location
        try:
            from System.IO import Path
            _my_dir = Path.GetDirectoryName(__file__) #relative to the module file
            _image_path = _my_dir + "\\transformations\\utils\\images\\"
            set_bg_image_and_size(_image_path + _image_to_use)
        except:
            raise

def set_image_in_table_column_based_on_limit(Table, Matrix, image_list, green_limit, yellow_limit):
    r"""Within a Table, select which image to display in the last column, based 
    upon limits, for example a traffic light system or up and down arrows.
    
    This should be run per Table, and the background of each cell in the last
    column will be updated to set the background image and size  based on the
    image selected.
    
    Example:
    
    | image_list= ["greenarrow.jpg","greyarrow.jpg","redarrow.jpg"]
    | texts.set_image_in_table_column_based_on_limit(Table, Matrix, image_list, 0.2, 0.1)
    
    """
       
    _green_image = image_list[0] # "\\greenarrow.png"
    _yellow_image = image_list[1] # "\\greyarrow.png"
    _red_image = image_list[2] # "\\redarrow.png"
    
    for row in Matrix:
        col = Matrix.TopAxis.DataMembers.Count
        shape = Table.Cell(row.Member.DataIndex + 2, col + 1).Shape    
        _value = row[col-1][0].GetNumericValue()

        _image_to_use = _red_image
        if(_value >= green_limit):
            _image_to_use = _green_image
        elif(_value >= yellow_limit):
            _image_to_use = _yellow_image
        try:
            set_bg_image_and_size(_image_to_use, Shape)
        except:
            try:
                from System.IO import Path
                _my_dir = Path.GetDirectoryName(__file__) #relative to the module file
                _image_path = _my_dir + "\\transformations\\utils\\images\\"
                set_bg_image_and_size(_image_path + _image_to_use, shape)
            except:
                raise
       
if __name__ == "__main__":
    import doctest
    doctest.testmod()
