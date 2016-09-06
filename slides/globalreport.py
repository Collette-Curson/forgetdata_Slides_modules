def globalReport():
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
    # 1.Connect to the api
    try: 
        reload(api)
    except:
        import api
    from Forgetdata.Slides.PowerPointHandler import PowerPointScripting as ppt, SlidesScripting as ss
    
    # 2. Check if this presentation is automated 
    ctxt= presentationAutomated(ppt, api)
    if ctxt==None: return 

    print "***************** Running Global Report *****************************"
    # 3. Create array for storing report
    reportFileName="Slides Connection Report - " + ppt.ActivePresentation.Name

    reportFile=[]
    if  reportFileName !=None:
        # 3a. General information about the selected pptx file.
        getConnectionInfo(reportFile,ctxt)
        getSlideConnectInfo(reportFile,ppt.ActivePresentation.Slides, api)

        # 3b. Information about the slides that are automated.
        getSlideInfo(reportFile,ppt.ActivePresentation.Slides, api)
        # 3c. Information about the shapes that are automated.
        getShapeInfo(reportFile,ppt.ActivePresentation.Slides, api,ppt)

        # 6. Write out the report
        for row in reportFile:
            print row

    print "******************* Global Report End *****************************"

def TransformationAndAfterFillScriptReport():
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
    #Connect to the api
    try: 
        reload(api)
    except:
        import api
    from Forgetdata.Slides.PowerPointHandler import PowerPointScripting as ppt, SlidesScripting as ss
    
    #Check if this presentation is automated 
    ctxt= presentationAutomated(ppt, api)
    if ctxt==None: return 

    print "***************** Running Custom Script Report *****************************"

    #Create array for storing report
    scriptReportFileName= "Slides Connection Report - " + ppt.ActivePresentation.Name

    reportFile=[]
    if  scriptReportFileName !=None:
        #Information about the slides that are automated using a data transformation or after fill action 
        getSlideInfo(reportFile,ppt.ActivePresentation.Slides, api, DataTransform=True)
        #Information about the shapes that are automated and using a data transformation or after fill action 
        getShapeInfo(reportFile,ppt.ActivePresentation.Slides, api, ppt, DataTransform=True)

        #Write out the report
        for row in reportFile:
            print row
    print "***************** Custom Script Report End *****************************"

def EditTransformationAndAfterFillScriptReport():
    """
    This is an Automated Report Script which will look for csv files called a specific name, based on slide and shape name, and will import the contents into the Transformation/After Fill scripts: \r\n
    It will produce the following:\r\n
    1. A SLIDE based report containing:\r
          total number of connected slides using a data transformation or after fill action\r\n
    2. A SHAPE based report containing:  \r
          the script contained within the data transformation or after fill action before the update. \r
          And an updated script based on scripts found.\r\n\r\n
    NOTE: This script WILL edit the Shape Settings for each shape on your slides, if the csv file for that shape is found.
    """
    #Connect to the api
    try: 
        reload(api)
    except:
        import api
    from Forgetdata.Slides.PowerPointHandler import PowerPointScripting as ppt, SlidesScripting as ss
    
    #Check if this presentation is automated 
    ctxt= presentationAutomated(ppt, api)
    if ctxt==None: return 

    print "***************** Running Edit Transformation and After Fill Script Report *****************************"

    #Create array for storing report
    scriptReportFileName= "Slides Connection Report - " + ppt.ActivePresentation.Name

    reportFile=[]
    if  scriptReportFileName !=None:
        #Information about the slides that are automated using a data transformation or after fill action 
        getSlideInfo(reportFile,ppt.ActivePresentation.Slides, api, DataTransform=True)
        #Information about the shapes that are automated and using a data transformation or after fill action 
        getShapeInfo(reportFile,ppt.ActivePresentation.Slides, api, ppt, EditDataTransform=True)

        #Write out the report
        for row in reportFile:
            print row
    print "***************** Edit Transformation and After Fill Report End *****************************"

def RemoveReloadFromScript():
    """
    This is an Automated Report Script which will do the following: \r\n
    1. Identify all shapes containing a Data Transformation Script, or After Fill Script AND contains a reload statement. \r
    2. Update the existing script to comment out the reload() within the script.\r
    3. And report the original and updated script.\r\n\r\n
    NOTE: This script WILL edit the Shape Settings for each shape on your slides, if a reload() statement is found within that shape's script.
    """
    #Connect to the api
    try: 
        reload(api)
    except:
        import api
    from Forgetdata.Slides.PowerPointHandler import PowerPointScripting as ppt, SlidesScripting as ss

    #Check if this presentation is automated
    ctxt= presentationAutomated(ppt, api)
    if ctxt==None: return 

    print "***************** Running Custom Script Remove 'reload(module)' *****************************"
 
    #Create array for storing report information:
    scriptReportFileName= "Slides Connection Report - " + ppt.ActivePresentation.Name

    reportFile=[]
    if  scriptReportFileName !=None:
        #Information about the shapes that contain Reload within their transformation or after fill scripts.
        getShapeInfo(reportFile,ppt.ActivePresentation.Slides, api, ppt, RemoveReload=True)
    
        #Write out the report
        for row in reportFile:
            print row
    print "***************** Custom Script Remove 'reload(module)' End *****************************"

def ReinsertReloadIntoScript():
    """
    This is an Automated Report Script which will do the following: \r\n
    1. Identify all shape containing a Data Transformation Script, or After Fill Script AND contains a commented out reload statement. \r
    2. Update the existing script to remove the comment from this statement, ie reinserting the reload().\r
    3. And report the original and updated script.\r\n\r\n
    NOTE: This script WILL edit the Shape Settings for each shape on your slides, if a commented out reload() statement is found within that shape's script.
    """
    #Connect to the api
    try: 
        reload(api)
    except:
        import api
    from Forgetdata.Slides.PowerPointHandler import PowerPointScripting as ppt, SlidesScripting as ss

    #Check if this presentation is automated
    ctxt= presentationAutomated(ppt, api)
    if ctxt==None: return 

    print "***************** Running Custom Script Reinsert 'reload(module)' *****************************"
 
    #Create array for storing report information:
    scriptReportFileName= "Slides Connection Report - " + ppt.ActivePresentation.Name

    reportFile=[]
    if  scriptReportFileName !=None:
        #Information about the shapes that contain a commented out Reload within their transformation or after fill scripts.
        getShapeInfo(reportFile,ppt.ActivePresentation.Slides, api, ppt, ReinsertReload=True)
    
        #Write out the report
        for row in reportFile:
            print row
    print "***************** Custom Script Reinsert 'reload(module)' End *****************************"
   
def GlobalTextSubstitution():
    """
    This is an Automated Report Script which will enable you to substitute, or replace text from within your project in the following places: \r\n
    1. Matrix Labels \r
    2. Group Labels \r
    3. Side axis labels \r
    4. Top axis labels \r\n\r\n
    NOTE: This script will enable you to enter the text substitutions into a text file, which will be saved to the same folder as your pptx file.  \r
    Then, it will also update all connected shapes to contain a Data Transformation which will run a global text substitution script against each shape.\r\n
    """
    #Connect to the api
    try: 
        reload(api)
    except:
        import api
    from Forgetdata.Slides.PowerPointHandler import PowerPointScripting as ppt, SlidesScripting as ss
    from forgetdata import *
    #Check if this presentation is automated 
    ctxt= presentationAutomated(ppt, api)
    if ctxt==None: return 

    print "***************** Running Global Text Substitution Script *****************************"
 
    ###
    ##TODO create the js file during the script using a pop up window.
    ### for now just read existing file.
    ###

    textSubstitionFilename="\"" + ppt.ActivePresentation.Path  +"\\" + ppt.ActivePresentation.Name[:-5] + ".js" + "\"" # path to existing file containing text replacements, called pptxfilename.js
    print "Global Text Substitutions for this project can be found here: "
    print textSubstitionFilename
 
    #Create array for storing report information:
    scriptReportFileName= "Slides Connection Report - " + ppt.ActivePresentation.Name
    reportFile=[]
    if  scriptReportFileName !=None:
        #Information about the shapes that contain a commented out Reload within their transformation or after fill scripts.
        getShapeInfo(reportFile,ppt.ActivePresentation.Slides, api, ppt, TextSubstitution=True)
    
        #Write out the report
        for row in reportFile:
            print row
    print "***************** Running Global Text Substitution Script End *****************************"

def presentationAutomated(ppt,api):
    #This is a function which will check if the current report is Automated or not.
    if ppt:
        print "Presentation name: "+ ppt.ActivePresentation.Name

        ctxt = api.GetDataContext(ppt.ActivePresentation)
        if ctxt:
            print  "Presentation is automated"
        else:
            print "Presentation is NOT automated"
            ctxt=None
        return ctxt

def getConnectionInfo(reportFile, ctxt):
    #This function will report the connection information for the current connections.
    reportFile.append(" ")
    reportFile.append("Data Context:-")
    for item in ctxt:
        reportFile.append("   Connection Name: " + item.Name)
        reportFile.append("   Connection String: " + item.ConnectionString)
        reportFile.append("   Provider: " + item.Provider)
    return reportFile

def getSlideConnectInfo(reportFile,Slides, api):
    #This function will report a general summary of which slides are connected within the current presentation.
    numberOfSlides=0
    slideNumber=1
    whichSlides=[]
    for slide in Slides:
        if slide.Shapes.Count>0: 
            shapeNumber=1
            whichShapes=[]
            numberOfShapes=0
            for shape in slide.Shapes:
                connected = api.GetShapeLink(shape)
                if connected:
                    numberOfShapes+=1
                    whichShapes.append(shapeNumber)
                shapeNumber += 1
        if numberOfShapes > 0:
            numberOfSlides += 1
            whichSlides.append(slideNumber)
        slideNumber+=1
    reportFile.append(" ")
    reportFile.append("Total Number of slides connected = " + str(numberOfSlides))
    reportFile.append("Slides connected = " + str(whichSlides))
    reportFile.append(" ")
    reportFile.append(" ")
    return reportFile

def getSlideInfo(reportFile,Slides, api, DataTransform=None):     
    #This function will get general information about the current presentation on a slide by slide basis. i.e how many shapes on each slide that are connected.
    reportFile.append(" ")
    reportFile.append("REPORT BY SLIDE")
    reportFile.append(" ")
    txt=""
    if DataTransform:
        txt=", using Data Transformation, using Custom Action Scripts"
    reportFile.append("Slide Number, " + "Number of shapes automated" + txt)
 
    reportTxt=""
    slideNumber=1
    for slide in Slides:
        if slide.Shapes.Count>0: 
            shapeNumber=1
            numberOfShapes=0
            numberOfTransformShapes=0
            numberOfAfterFillShapes=0
            for shape in slide.Shapes:
                connected = api.GetShapeLink(shape)
                if connected:
                    numberOfShapes+=1
                    if DataTransform:
                        if (connected.Query.Transformation):
                            numberOfTransformShapes+=1
                        if (connected.FillerProperties.AfterFillAction):
                            numberOfAfterFillShapes+=1
                shapeNumber += 1
        if DataTransform: 
            if slideNumber < 10: reportTxt= str(slideNumber) + ",            " + str(numberOfShapes) + ",                          " + str(numberOfTransformShapes)+ ",                         " + str(numberOfAfterFillShapes)
            else: reportTxt= str(slideNumber) + ",           " + str(numberOfShapes) + ",                          " + str(numberOfTransformShapes)+ ",                         " + str(numberOfAfterFillShapes)
        else:  
            if slideNumber < 10: reportTxt = str(slideNumber) + ",            " + str(numberOfShapes)
            else: reportTxt = str(slideNumber) + ",           " + str(numberOfShapes)
        reportFile.append(reportTxt)
        slideNumber+=1
    return reportFile

def getShapeInfo(reportFile, Slides, api, ppt, DataTransform=None,EditDataTransform=None,RemoveReload=None,ReinsertReload=None,TextSubstitution=None): 
    #This function is widely used to get information about each shape on each slide, and report back, or update different aspects of the shapes settings.
    reportFile.append(" ")
    txt=""
    if DataTransform: txt=" - SHAPES USING DATA TRANSFORMATION OR AFTER FILL SCRIPTS"
    if EditDataTransform: txt=" - SHAPES WITH EDITED DATA TRANSFORMATION OR AFTER FILL SCRIPTS"
    if RemoveReload: txt=" - SHAPES CONTAINING 'RELOAD' WITHIN THE DATA TRANSFORMATION OR AFTER FILL SCRIPTS"
    if ReinsertReload: txt=" - SHAPES CONTAINING a COMMENTED OUT 'RELOAD' WITHIN THE DATA TRANSFORMATION OR AFTER FILL SCRIPTS"
    if TextSubstitution: txt=" - ALL CONNECTED SHAPES"
    reportFile.append("REPORT BY SHAPE" + txt)
    reportFile.append(" ")

    slideNumber=1
    reloadTransformations=[]
    reloadAfterFill=[]

    #Loop through each slide
    for slide in Slides:
        if slide.Shapes.Count>0: 
            shapeNumber=1
            numberOfShapes=0
            # Loop through all shapes within each slide
            for shape in slide.Shapes:
                connected = api.GetShapeLink(shape)
                containsAfterFill=False
                containsTransformation=False
                transformScript=[]
                afteractionScript=[]
                containsScript=False

                #DataTransform = True is used by TransformationAndAfterFillScriptReport()
                if DataTransform:
                    ReportFileX=[]
                    dataTransformAfterFill(ReportFileX, ppt, connected,slideNumber,shapeNumber)
                    for row in ReportFileX:
                        reportFile.append(row)
                #EditDataTransform = True is used by EditTransformationAndAfterFillScriptReport()
                elif EditDataTransform:
                    ReportFileX=[]
                    dataTransformAfterFill(ReportFileX, ppt, connected,slideNumber,shapeNumber,Edit=True)
                    for row in ReportFileX:
                        reportFile.append(row)
                    ##Save the update made to the scripts.
                    api.SaveShapeLink(connected,shape)
 
                #RemoveReload = True is used by RemoveReloadFromScript()
                elif RemoveReload:
                    ReportFileX=[]
                    reloadReport(ReportFileX, connected,slideNumber,shapeNumber)
                    for row in ReportFileX:
                        reportFile.append(row)
                    ##Save the update made to the scripts.
                    api.SaveShapeLink(connected,shape)
 
                #ReinsertReload = True is used by ReinsertReloadIntoScript()
                elif ReinsertReload:
                    ReportFileX=[]
                    reloadReport(ReportFileX, connected,slideNumber,shapeNumber,reInsert=True)  # note this is running the remove function, but with an additional parameter, reInsert=True
                    for row in ReportFileX:
                        reportFile.append(row)
                    ##Save the update made to the scripts.
                    api.SaveShapeLink(connected,shape)

                #textSubstitutionFilename is used by GlobalTextSubstitution()
                elif TextSubstitution:
                    ReportFileX=[]
                    globalTextSubstitutionScript(ReportFileX, connected, ppt, slideNumber,shapeNumber,TextSubstitution=True)  # note this is a function to add a data transformation to every connected shape.
                    for row in ReportFileX:
                        reportFile.append(row)
                    ##Save the update made to the scripts.
                    api.SaveShapeLink(connected,shape)
                #Global report script
                else:
                    ReportFileX=[]
                    globalReportReport(ReportFileX, connected,slideNumber,shapeNumber)
                    for row in ReportFileX:
                        reportFile.append(row)          
                shapeNumber += 1
        slideNumber+=1

    return reportFile

def reloadReport(ReportFileX, connected,slideNumber,shapeNumber,reInsert=None):
    #This function is used by 2 other functions, to comment out reload() functions, and to reinsert them back into the Data Transformation or After Fill scripts.
    #The functions are called RemoveReloadFromScript() and ReInsertReloadIntoScript()

    containsAfterFill=False   # set to true if the shape contains an After Fill action script.
    containsTransformation=False # set to true if the shape contains a Transformation script.
    containsScript=False  # set to true if the shape contains a Transformation script, or After Fill Action Script, ie if containsAfterFill = True or containsTransformation = True.
    transformScript=[]  # contains the Transformation script, stored row by row
    afteractionScript=[] # contains the After Fill Action script, stored row by row
    
    #only run this if the shape contains a Slides! connection
    if not connected: return

    #look at the connections and see if they contain Transformation or After Fill scripts.
    if (connected.Query.Transformation):
        containsTransformation=True
        containsScript=True
        transformScript = connected.Query.Transformation.EditableScript.split("\r")
    if (connected.FillerProperties.AfterFillAction):
        containsAfterFill=True
        containsScript=True
        afteractionScript=connected.FillerProperties.AfterFillAction.EditableScript.split("\r")

    #only run the script if a transformation or After fill script is found.
    if not containsScript: return

    #If the shape contains a Transformation script.
    if containsTransformation:
        scriptType=" Transformation Script"
        ReportFileX, connected.Query.Transformation.EditableScript = updateReloadInScript(ReportFileX,slideNumber,shapeNumber, transformScript, scriptType, connected.Query.Transformation.EditableScript,reInsert)
    if containsAfterFill:
        scriptType=" After Fill Script"
        ReportFileX, connected.FillerProperties.AfterFillAction.EditableScript = updateReloadInScript(ReportFileX,slideNumber,shapeNumber, afteractionScript, scriptType, connected.FillerProperties.AfterFillAction.EditableScript,reInsert)

def updateReloadInScript(ReportFileX,slideNumber,shapeNumber, Script, scriptType, ShapeScript,reInsert=None):
    scriptReload=False  # Set to true if a "reload" statement was found within the  script.
    newScript=""   # to be used to edit the existing  script if reload() or commented out reload() is found.

    for row in Script:  # for each row in the current script.
        starttxt=""
        #If running the re-insert reload() function...look for the commented out statement, and remove it
        if reInsert: 
            if "Removed reload statement" in row:
                #what is the first character of the text?
                if "\t#" in row:
                    starttxt="\t"  # set indentation for the statement to tab
                elif "    #" in row:
                    starttxt="    "  # set indentation for the statement to spaces
                else:
                    starttxt=""  # set indentation for the statement to nothing
                ReportFileX.append("Comment 'Removed reload statement' found in slide  " + str(slideNumber) + ",  shape " + str(shapeNumber) + scriptType)
                ReportFileX.append("============================================================================================")
                rowtxt=row.split("statement: ")
                newScript+= starttxt + rowtxt[1] + "\r\n"
                scriptReload=True
            else:
                newScript+=row + "\r\n"
        #If running the Remove reload() function.
        else: 
            if not "Removed reload statement" in row:
                if "reload(" in row:
                    #what is the first character of the text?
                    if "\t" in row:
                        starttxt="\t"  # set indentation for the statement to tab
                    elif "    " in row:
                        starttxt="    "  # set indentation for the statement to spaces
                    else:
                        starttxt=""  # set indentation for the statement to nothing
                    ReportFileX.append(starttxt + "reload() found in slide " + str(slideNumber) + ",  shape " + str(shapeNumber) + scriptType)
                    ReportFileX.append("=================================================================================")
                    newScript += starttxt + "### Removed reload statement: " + row.strip() + "\r\n"
                    newScript += starttxt + "pass \r\n"
                    scriptReload=True
                else:
                    newScript+=row + "\r\n"

    #if the script was edited,  write out a report containing the original script, and then update the script, and write out the updated script.
    if scriptReload:
        try:
            ReportFileX.append(" ")
            ReportFileX.append( "Original Script - " + scriptType)
            ReportFileX.append( "-------------------------------")
            ReportFileX.append( " ")
            for row in ShapeScript.split("\r"):
                ReportFileX.append(row)
            #update the script here
            ShapeScript = newScript
            ReportFileX.append( " ")
            ReportFileX.append( "Updated Script - "+ scriptType)
            ReportFileX.append( "------------------------------")
            ReportFileX.append( " ")
            for row in ShapeScript.split("\r"):
                ReportFileX.append(row)
            ReportFileX.append( " ")
        except:
            pass
    return ReportFileX, ShapeScript

def globalTextSubstitutionScript(ReportFileX, connected, ppt, slideNumber,shapeNumber,TextSubstitution):
    #This function is used by GlobalTextSubstitution() to insert a global text substitution script into all connected shapes as a data transformation script.
    #global_text_replacements.py is installed with Slides! into the Template folder - C:\Users\<username>\Documents\Slides Templates\Scripts\Transformations\
    containsTransformation=False
    newTransformScript=""
    newScript=""
    scriptPresent=False
    scriptupdated = False
    textSubstitutionFilename = "\"" + ppt.ActivePresentation.Path  +"\\" + ppt.ActivePresentation.Name[:-5] + ".js" + "\""

    if not connected: 
        return
    
    #Only run if the shape is connected.
    newScript = "\n\r###This is a global text replacement script, added via Global Scripts \r\n"
    newScript += "from transformations import *" + "\r\n"
    newScript +="try: " + "\r\n"
    newScript += "  filename=" + textSubstitutionFilename + "   # path to existing file containing text replacements." + "\r\n"
    newScript += "  GlobalTextReplace(filename)" + "\r\n"
    newScript +="except: " + "\r\n"
    newScript +="   pass " + "\r\n"
    newScript += "###End of global text replacement script." + "\r\n"

    if (connected.Query.Transformation): containsTransformation=True

    #If a Data Transformation script already present, then insert the global text substitution script at the bottom of the existing script.
    if containsTransformation: 
        #check if this global script has already been run, and if so, do not re-insert it into this shape.
        for row in connected.Query.Transformation.EditableScript.split("\r"):
            if "This is a global text replacement script" in row:
                scriptPresent = True
                break
        if scriptPresent == True:
            newTransformScript = connected.Query.Transformation.EditableScript
        else:
            newTransformScript= connected.Query.Transformation.EditableScript + newScript 
            scriptupdated=True

    #If no Data Transformation Script found on this shape, add one.
    else:
        ##
        ##TODO   add something here to enable data transformation scripts for shapes without a script currently.
        ##
        # ??? connected.Query.Transformation ??
        #connected.Query.Transformation
        newTransformScript = newScript
        scriptupdated=True

    #If the global Text substitution has been added to the script, create a before/after report, and update the script.
    if scriptupdated==True:
        ReportFileX.append(" ")
        ReportFileX.append("SlideNumber = " + str(slideNumber) + " ShapeNumber = " + str(shapeNumber))
        ReportFileX.append( "Original Transformation Script:")
        ReportFileX.append( "-------------------------------")
        ReportFileX.append( " ")
        try:
            for row in connected.Query.Transformation.EditableScript.split("\r"):
                ReportFileX.append(row)
        except:
            pass
        #update the script here.
        try:
            connected.Query.Transformation.EditableScript = newTransformScript    
        except:
            pass
        ReportFileX.append( " ")
        ReportFileX.append( "Updated Transformation Script:")
        ReportFileX.append( "------------------------------")
        ReportFileX.append( " ")
        try:
            for row in connected.Query.Transformation.EditableScript.split("\r"):
                ReportFileX.append(row)
        except:
            pass
        ReportFileX.append( " ")
    else: # if the script not changed.
        ReportFileX.append("SlideNumber = " + str(slideNumber) + " ShapeNumber = " + str(shapeNumber))
        ReportFileX.append( "Transformation Script not updated - Global Text Substitution already found")
        ReportFileX.append( " ")
    return ReportFileX

def dataTransformAfterFill(ReportFileX, ppt, connected,slideNumber,shapeNumber,Edit=None):  
    # This is used by the TransformationAndAfterFillScriptReport() function.  
    # It will report the script found in the Data Transformation or After Fill Script for the shape.
    # It will also output these scripts to an external file, which can be used to edit the scripts, and then run another global script to import the script back into the pptx file

    containsAfterFill=False
    containsTransformation=False
    transformScript=[]
    afteractionScript=[]
    containsScript=False
    if connected:
        #find out if the shape contains an AfterFill or Transformation script.
        if (connected.Query.Transformation):
            containsTransformation=True
            containsScript=True
            transformScript = connected.Query.Transformation.EditableScript.split("\r")
        if (connected.FillerProperties.AfterFillAction):
            containsAfterFill=True
            containsScript=True
            afteractionScript=connected.FillerProperties.AfterFillAction.EditableScript.split("\r")
        #If the shape contains a script, write out a report containing the script, and slide and shape number.
        if containsScript:
            ReportFileX.append("==================================================================================================")
            ReportFileX.append("Slide Number = "  + str(slideNumber) + "   Shape number = " + str(shapeNumber) + "   Contains Transformation =" + str(containsTransformation) + "   Contains After Fill = " + str(containsAfterFill))
            ReportFileX.append("==================================================================================================")
            ReportFileX.append("Filler Type = " + str(connected.FillerProperties.GetType().Name))
            
            #If running the EditTransformationAndAfterFillScriptReport() function
            if Edit==True: #If running the EditTransformationAndAfterFillScriptReport() function
                if containsTransformation:
                    ReportFileX, connected.Query.Transformation.EditableScript = readExternalFile(ppt, slideNumber,shapeNumber,ReportFileX,transformScript,connected.Query.Transformation.EditableScript,Transformation=True)
                if containsAfterFill:
                    ReportFileX, connected.FillerProperties.AfterFillAction.EditableScript = readExternalFile(ppt, slideNumber,shapeNumber,ReportFileX,transformScript,connected.FillerProperties.AfterFillAction.EditableScript,AfterFill=True)                        
            else:  #Else - If running the TransformationAndAfterFillScriptReport() function
                if containsTransformation:
                    writeReportAndExternalFile(ppt, slideNumber,shapeNumber,ReportFileX,transformScript,connected.Query.Transformation.EditableScript,Transformation=True)
                if containsAfterFill:
                    writeReportAndExternalFile(ppt, slideNumber,shapeNumber,ReportFileX,afteractionScript,connected.FillerProperties.AfterFillAction.EditableScript,AfterFill=True)
        return ReportFileX
    else:
        return

def writeReportAndExternalFile(ppt, slideNumber,shapeNumber,ReportFileX,Script,ScriptforExternalFile,Transformation=None, AfterFill=None):
    if Transformation == True: txt = " Data Transformation Script"
    else: txt = " After Fill Script"

    #Write out the Report file containing the scripts all in one report.
    ReportFileX.append(" ")
    ReportFileX.append(txt)
    ReportFileX.append("===========================")
    for row in Script:
        ReportFileX.append(row)
    ReportFileX.append(" ")
    #Also output the script to an external file for editing if required. This is writing out one file per script found in the pptx file. The files are located in the same folder as the pptx file.
    scriptFilename=""
    scriptFilename = ppt.ActivePresentation.Path  +"\\" + ppt.ActivePresentation.Name[:-5] + " slide " + str(slideNumber) + " shape " + str(shapeNumber) + txt + ".csv"
    import csv
    scriptFile = csv.writer(open(scriptFilename, 'wb'), delimiter=',')
    scriptFile.writerow([ScriptforExternalFile]) 
    #print dir(scriptFilename) # .close()
    #write a message to the report file where the script is output to.
    ReportFileX.append(" ")
    ReportFileX.append("-------------------------------")
    ReportFileX.append("The script has been output to " + scriptFilename)
    ReportFileX.append("-------------------------------")
    return ReportFileX

def readExternalFile(ppt,slideNumber,shapeNumber,ReportFileX,Script,ScriptforExternalFile,Transformation=None, AfterFill=None):
    if Transformation == True: txt = " Data Transformation Script"
    else: txt = " After Fill Script"

    newScript=""
    #Write out the Report file containing the scripts all in one report.
    ReportFileX.append(" ")
    ReportFileX.append("Current " + txt)
    ReportFileX.append("===========================")
    for row in Script:
        ReportFileX.append(row)
    ReportFileX.append(" ")
    #Read the script in from an external file. 
    scriptFilename=""
    scriptFilename = ppt.ActivePresentation.Path  +"\\" + ppt.ActivePresentation.Name[:-5] + " slide " + str(slideNumber) + " shape " + str(shapeNumber) + txt + ".csv"
    import csv
    try:
        ScriptFile = csv.reader(open(scriptFilename, 'rb'), delimiter=',')
    except:
        ReportFileX.append("Unable to open file: " + scriptFilename)
        return
    for row in ScriptFile:
        for rowtxt in row[0].split("\r"):
            newScript += rowtxt + "\r\n"

    #Save the new updated script to the Transformation / After Fill script, overwriting what was previously there.
    ScriptforExternalFile=""
    ScriptforExternalFile=newScript
    
    #Report the updated script
    ReportFileX.append(" ")
    ReportFileX.append("Updated " + txt)
    ReportFileX.append("===========================")
    for row in ScriptforExternalFile.split("\r"):
        ReportFileX.append(row)
    ReportFileX.append(" ")
    return ReportFileX,ScriptforExternalFile

def globalReportReport(ReportFileX, connected,slideNumber,shapeNumber):
    #This is used by the globalReport() function.  It will report for each connected shape the following information:
    #Which type of filler is used - chart/table/text
    #Whether the shape has a Transformation or After Fill script, and what it contains
    #Which Selections are found for rows/columns.
    containsAfterFill=False
    containsTransformation=False
    transformScript=[]
    afteractionScript=[]
    containsScript=False
    if connected:
        ReportFileX.append("===================================")
        ReportFileX.append("Slide Number = "  + str(slideNumber) + "   Shape number = " + str(shapeNumber))
        ReportFileX.append("===================================")
        ReportFileX.append("Filler Type = " + str(connected.FillerProperties.GetType().Name))
        if (connected.Query.Transformation):
            containsTransformation=True
            transformScript = connected.Query.Transformation.EditableScript.split("\r")
        ReportFileX.append("Contains Data Transformation Script = " + str(containsTransformation))
        if containsTransformation: 
            #TODO - Testing out how to write out report.
            ReportFileX.append(" ")
            ReportFileX.append("Data Transformation Script:")
            ReportFileX.append(connected.Query.Transformation.EditableScript)
            #for row in transformScript:
            #    ReportFileX.append(row)
            #ReportFileX.append(" ")
        if (connected.FillerProperties.AfterFillAction):
            containsAfterFill=True
            afteractionScript=connected.FillerProperties.AfterFillAction.EditableScript.split("\r")
        ReportFileX.append("Contains After Fill Script = " + str(containsAfterFill))
        if containsAfterFill:
            ReportFileX.append(" ")
            ReportFileX.append("After Fill Script:")
            for row in afteractionScript:
                ReportFileX.append(row)
            ReportFileX.append(" ")
        ReportFileX.append("Selections:")
        for item in connected.Query.Items:
            ReportFileX.append("  --------------------------------------------")
            ReportFileX.append("  Table: " + item.TableName)
            ReportFileX.append("  Connection: " + item.ConnectionName)
            ReportFileX.append("  Row Selection: " + item.RowSelection)
            ReportFileX.append("  Column Selection: " + item.ColumnSelection)
        ReportFileX.append(" ")

        return ReportFileX
    else:
        return