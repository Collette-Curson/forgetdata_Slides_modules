import Forgetdata.Slides.PowerPointHandler.PowerPointScripting as ppts

# SlidesScripting is a static class with some useful helper functions, 
# these are all wrapped then called from here because it allows the underlying implementation 
# to be altered more easily
import Forgetdata.Slides.PowerPointHandler.SlidesScripting as ss
import Forgetdata.Slides.PowerPointHandler.SlidesManagementService as srv


def __getPres(pres):
    """ attempts to get the presentation object
    given either a presentation object, some child of a presentation object (e.g. a shape)
    or a filename"""

    from os import path
    Presentations = ppts.Application.Presentations
    if isinstance(pres,str):
        try:
            maybePres = Presentations[path.basename(pres)]
            if maybePres.FullName.lower() == pres:
                return maybePres
            else:
                raise ValueError("There is already a presentation open with that name in a different location")
        except EnvironmentError:
            return ppts.Application.Presentations.Open(pres)
    else:
        #check if it looks like a presentation object already
        try:
            s = pres.Slides
            return pres
        except AttributeError:
            raise ValueError("Unable to return a presentation object from the parameter provided:")

def __getFilename(pres):
    """attempts to get the path of a presentation object as a full/absolute path"""
    from os import path
    if isinstance(pres,str):
        return path.abspath(pres)
    else:
        if pres.Path == "":
            raise Exception("The presentation hasn't been saved, unable to get the full path")
        else:
            return path.abspath(pres.FullName)


       
        


def GetDataContext(pres = None):
    """Gets the data context from the PowerPoint presentation object
    that is passed in, if no presentation is specified then the 
    ActivePresentation is assumed"""
    return ss.GetDataContext(pres)


def SaveDataContext(ctxt, pres = None):
    """Saves the data context passed in into the PowerPoint presentation object
    specified presenation, if no presentation is specified then the 
    ActivePresentation is assumed"""
    ss.SaveDataContext(ctxt,pres)

def GetShapeLink(shape = None):
    """Gets the ShapeLink object from the PowerPoint Shape
    that is passed in, if no Shape is specified then the 
    ActiveShape is assumed"""
    return ss.GetShapeLink(shape)

def SaveShapeLink(link, shape = None):
    
    """Saves the specified shapeLink into the specified shape 
    (if no shape is specified then the active shape is assumed).
    If the link passed is None, then the ShapeLink will be deleted 
    from the specified shape."""
    ss.SaveShapeLink(link,shape)

def GetTemplatePresentations():
    """ Gets a list of the currently configured Template Presentations
    the return type is an `Forgetdata.Slides.PowerPointHandler.ITemplatePresentation`"""
    return srv.GetTemplates()

def InsertTemplateSlide(sourcePresentation, sourceSlide, targetPresentation=None, targetSlideIndex = -1):
    """ Inserts a template slide with index sourceSlideIndex from the source presentation into 
    target presentation at the target slide index"""
    
    sourceFileName = __getFilename(sourcePresentation)
    sourceSlideIndex = -1
    if not isinstance(sourceSlide, int):
        try:
            sourceSlideIndex = sourceSlide.SlideIndex
        except:
            raise Exception("Unable to get the index of the source slide")

    else:
        sourceSlideIndex = sourceSlide

    if (targetPresentation == None):
        targetPresentation = ppts.ActivePresentation
    else:
        targetPresentation = __getPres(targetPresentation)


    if targetSlideIndex <0:
        targetSlideIndex = ppts.ActiveSlide.SlideIndex

    numSlides = targetPresentation.Slides.InsertFromFile(sourceFileName,targetSlideIndex,sourceSlideIndex,sourceSlideIndex)
    if(numSlides >0 ):
        return targetPresentation.Slides[targetSlideIndex +1]
    else:
        raise Exception("No slides were inserted")



