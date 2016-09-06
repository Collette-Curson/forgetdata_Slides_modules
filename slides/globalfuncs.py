

def __msg(val):
    import clr
    clr.AddReference("System.Windows.Forms")
    from System.Windows.Forms import MessageBox
    MessageBox.Show(val)

def myFunc():
    """This function does very clever things"""
    import Forgetdata.Slides.PowerPointHandler
    svc = Forgetdata.Slides.PowerPointHandler.SlidesScripting

    __msg(str(dir(svc)))

def myFunc2():
    __msg("This is function 2 with a different message")
    pass

def listaddins():
    pptType = "PowerPoint.Application"
    from System import Type, Activator
    tppt = Type.GetTypeFromProgID(pptType)

    pptApp = Activator.CreateInstance(tppt)

    ComAddins = pptApp.COMAddIns
    for i in range(1,ComAddins.Count +1 ):
        ComAddin = pptApp.COMAddIns(i)
        print ("Addin Status for Addin {0}".format(ComAddin.Guid))
        for attr in ["Description","Guid","ProgId"]:
            try:
                print "\t" + attr + "=" + getattr(ComAddin,attr)
            except:
                pass
        if(ComAddin.ProgId=="Slides.Addin"):
            if(ComAddin.Connect != 0):
                print "slides addin connected"
    

def apitest():
    """This function tests all the api features
    it is not designed for production use sss"""
    try:
        reload(api)
    except:
        import api
    
    print "this is the api test..."
    print dir(api)
    print api.__file__

    from Forgetdata.Slides.PowerPointHandler import PowerPointScripting as ppt ,SlidesScripting as ss

    if ppt:
        print "Presentation name  "+ ppt.ActivePresentation.Name

        ctxt = api.GetDataContext(ppt.ActivePresentation)
        if ctxt:
            print  "Presentation is automated"
        else:
            print "Presentation is not automated"

        for slide in ppt.ActivePresentation.Slides:
            print "reading slide " +str(slide.SlideNumber)
            for shape in slide.Shapes:
                print "reading shape using api: " + str(shape.Id)
                try:
                    link = api.GetShapeLink(shape)
                    if link:
                        print "shape is automated"
                except:
                    import traceback
                    tb = traceback.format_exc()
                    
                    print "error : " + str(tb) 

def InsertTemplateTest():
    import api
    reload(api)
    from Forgetdata.Slides.PowerPointHandler import PowerPointScripting as ppt ,SlidesScripting as ss

    api.InsertTemplateSlide(ppt.ActivePresentation,ppt.ActivePresentation.Slides.Count)
    
def runGlobalReport():
    """
    This is an Automated Report Script which will report the following: \r\n\r\n
    1. General information about the presentation - which data file it is connected to etc. \r\n
    2. A SLIDE based report containing:\r
          total number of connected slides\r
          which slides are connected to Slides!\r\n
    3. A SHAPE based report containing:  \r
          which shapes within the connect slides are connected \r
          which connected shapes contain Data Transformation or After Fill scripts, and what the scripts contain \r
          which connections are used for each shape. \r\n\r\n
    NOTE: This report will not edit your PowerPoint file.
    """    
    try:
        reload(globalreport)
    except:
        import globalreport
    globalreport.globalReport()

def runTransformationAndAfterFillScriptReport():
    """
    This is an Automated Report Script which will report the following: \r\n\r\n
    1. A SLIDE based report containing:\r
          total number of connected slides using a data transformation or after fill action\r\n
    2. A SHAPE based report containing:  \r
          what the data transformation contains and what the after fill action contains. \r\n
    3. A csv file will be generated for each Transformation or After Fill script present on each connected slide.   \r
          These files will be found in the Project (pptx) folder. \r\n\r\n
    NOTE: This report will not edit your PowerPoint file.  
    """
    try:
        reload(globalreport)
    except:
        import globalreport
    globalreport.TransformationAndAfterFillScriptReport()

def runEditTransformationAndAfterFillScriptReport():
    """
    This is an Automated Report Script which will look for csv files called a specific name, based on slide and shape name, \r
    and will import the contents into the Transformation/After Fill scripts. It will produce the following: \r\n\r\n
    1. A SLIDE based report containing:\r
          total number of connected slides using a data transformation or after fill action\r\n
    2. A SHAPE based report containing:  \r
          the script contained within the data transformation or after fill action before the update. \r
          And an updated script based on scripts found.\r\n\r\n
    NOTE: This script WILL edit the Shape Settings for each shape on your slides, if the csv file for that shape is found.
    """
    try:
        reload(globalreport)
    except:
        import globalreport
    globalreport.EditTransformationAndAfterFillScriptReport()

def runRemoveReloadFromScript():
    """
    This is an Automated Report Script which will do the following: \r\n\r\n
    1. Identify all shapes containing a Data Transformation Script, or After Fill Script AND contains a reload statement. \r
    2. Update the existing script to comment out the reload() within the script.\r
    3. And report the original and updated script.\r\n\r\n
    NOTE: This script WILL edit the Shape Settings for each shape on your slides, if a reload() statement is found within that shape's script.
    """
    try:
        reload(globalreport)
    except:
        import globalreport
    globalreport.RemoveReloadFromScript()

def runReinsertReloadIntoScript():
    """
    This is an Automated Report Script which will do the following: \r\n\r\n
    1. Identify all shape containing a Data Transformation Script, or After Fill Script AND contains a commented out reload statement. \r
    2. Update the existing script to remove the comment from this statement, ie reinserting the reload().\r
    3. And report the original and updated script.\r\n\r\n
    NOTE: This script WILL edit the Shape Settings for each shape on your slides, if a commented out reload() statement is found within that shape's script.
    """
    try:
        reload(globalreport)
    except:
        import globalreport
    globalreport.ReinsertReloadIntoScript()

def runGlobalTextSubstitution():
    """
    This is an Automated Report Script which will enable you to substitute, or replace text from within your project in the following places: \r\n\r\n
    1. Matrix Labels \r
    2. Group Labels \r
    3. Side axis labels \r
    4. Top axis labels \r\n\r\n
    NOTE: This script will enable you to enter the text substitutions into a text file, which will be saved to the same folder as your pptx file.  \r
    Then, it will also update all connected shapes to contain a Data Transformation which will run a global text substitution script against each shape.\r\n
    """
    try:
        reload(globalreport)
    except:
        import globalreport
    globalreport.GlobalTextSubstitution()

def rundevfunc2():
    print globals()
    from .devfuncs import packagewd2
    packagewd2()   
    