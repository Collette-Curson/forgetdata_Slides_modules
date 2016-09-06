

def SetBgImageAndSize(fileName, Shape = None):
    try:
        import clr
        #from globals import *
        clr.AddReference("System.Drawing")
        from System.Drawing import Image
        from System.Drawing import SizeF

        im = Image.FromFile(fileName)
        sizePx = im.Size
        vertDPI = im.VerticalResolution
        horzDPI = im.HorizontalResolution
        im.Dispose()
        
        # calculate the actual size of the image in points as this is the unit that 
        # PowerPoint uses
        size = SizeF(72.0*float(sizePx.Width)/horzDPI,72*float(sizePx.Height)/horzDPI)
        SetBgImage(fileName, Shape)
        Shape.Width = size.Width
        Shape.Height = size.Height
        Shape.TextFrame.TextRange.Text = ""
        return True
    except:
        raise

def GetPptImageSize(fileName):
    import clr
    clr.AddReference("System.Drawing")
    from System.Drawing import Image
    from System.Drawing import SizeF

    im = Image.FromFile(fileName)
    sizePx = im.Size
    vertDPI = im.VerticalResolution
    horzDPI = im.HorizontalResolution
    im.Dispose()
        
    # calculate the actual size of the image in points as this is the unit that 
    # PowerPoint uses
    size = SizeF(72.0*float(sizePx.Width)/horzDPI,72*float(sizePx.Height)/horzDPI)
    return size
    
def SetBgImage(fileName, Shape = None):
    #from globals import *
    Shape.Fill.UserPicture(fileName)        

def SetBgPictureCenter(shape,fileName):
    from Microsoft.Office.Core import MsoTriState
    import clr
    clr.AddReference("System.Drawing")
    
    picSize = GetPptImageSize(fileName)
    
    boxHeight = shape.Height
    boxWidth = shape.Width
    
    heightScale = boxHeight/picSize.Height
    widthScale = boxWidth/picSize.Width
    
    if heightScale < 1 or widthScale < 1:
        imageScale = min(heightScale,widthScale)
        picSize.Height = picSize.Height * imageScale
        picSize.Width = picSize.Width * imageScale
    
    widthOffsetProportion = (picSize.Width/boxWidth)/2
    heightOffsetProportion = (picSize.Height/boxHeight)/2
        
    shape.Fill.UserPicture(fileName)
    
    shape.Fill.TextureVerticalScale= 2.1
    
    
def RGB(r,g,b):
    import clr
    clr.AddReference("System.Drawing")
    from System.Drawing import Color,ColorTranslator

    ourColor = Color.FromArgb(r,g,b)
    return ColorTranslator.ToOle(ourColor)

def SetBackgroundColor(shape,red,green,blue):
    shape.Fill.Visible = 1
    shape.Fill.ForeColor.RGB = RGB(red,green,blue)

