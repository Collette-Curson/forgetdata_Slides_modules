"""Provides a series of functions which will run against any PowerPoint shape,
after the Shape has been filled.

"""

__version__ = '4.3.0'

def RGB(r, g, b):
    """Convert RGB values to ColorTranslator value for PowerPoint."""

    import clr
    clr.AddReference("System.Drawing")
    from System.Drawing import Color, ColorTranslator

    ourColor = Color.FromArgb(r, g, b)
    return ColorTranslator.ToOle(ourColor)

def set_background_color(Shape, red, green, blue):
    """Set the background colour for the shape to an RGB value.

    Example:

    | shapes.set_background_color(Shape, 255, 255, 255)
    | or
    | shapes.set_background_color(cell.Shape, 255, 255, 255)

    """

    Shape.Fill.Visible = 1
    Shape.Fill.ForeColor.RGB = RGB(red, green, blue)

def find_shape(Shapes, shape_name):
    """Find a shape with a specific name within your PowerPoint slide.

    It can be used to delete existing shapes, so that they can be re-generated,
    or to select a specific shape to apply a function to.

    Example:

    | labelShape =find_shape(slide.Shapes,"mySlideName")
    | if(labelShape != None):
    |     labelShape.Delete()
    | else:
    |     break


    :param Shapes: PowerPoint Shapes.
    :param shape_name: Text name of the shape.
    
    """

    if(Shapes is None):
        return None

    try:
        return Shapes(shape_name)
    except:
        return None


if __name__ == "__main__":
    import doctest
    doctest.testmod()
