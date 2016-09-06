
def SetTrafficLights(greenLimit,yellowLimit, Shape = None):
    import backgrounds
    reload(backgrounds)
    
    from globals import *
    from System.IO import Path
    myDir = Path.GetDirectoryName(__file__)
    greenImage = ""
    yellowImage = ""
    redImage = ""
    greenImage = myDir + "\\images\\traffic-light-green.jpg"
    yellowImage = myDir + "\\images\\traffic-light-yellow.jpg"
    redImage = myDir + "\\images\\traffic-light-red.jpg"
    
    value = Matrix[0][0][0].GetNumericValue()
    imageToUse = redImage
    if(value >=greenLimit):
        imageToUse = greenImage
    elif(value >= yellowLimit):
        imageToUse = yellowImage
    backgrounds.SetBgImageAndSize(imageToUse, Shape)

def SetTrafficLightsFromMatrix(selectrow,selectcolumn,greenLimit,yellowLimit,  Table = None):
    import backgrounds
    from globals import *
    from System.IO import Path
    myDir = Path.GetDirectoryName(__file__)
    greenImage = ""
    yellowImage = ""
    redImage = ""
    greenImage = myDir+"\\images\\greenarrow.png"
    yellowImage = myDir+"\\images\\greyarrow.png"
    redImage = myDir+"\\images\\redarrow.png"
    
    x=selectrow-1
    y=selectcolumn-1
    value = Matrix[x][y][0].GetNumericValue()

    imageToUse = redImage
    if(value >=greenLimit):
        imageToUse = greenImage
    elif(value >= yellowLimit):
        imageToUse = yellowImage
    try:
        backgrounds.SetBgImageAndSize(imageToUse)
    except:
        from v4_2_support import SetBgImageAndSize
        SetBgImageAndSize(imageToUse, Table.Cell(selectrow+1,selectcolumn+1).Shape)