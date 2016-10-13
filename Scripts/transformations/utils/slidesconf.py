"""
Module to configure a slides environment for testing purposes
"""

try:
    
    import os
    import sys
    import platform
    try:
        import clr
    except:
        pass
    from Microsoft.Win32 import Registry
    
    
    MATRIX_PATH= Registry.GetValue("HKEY_CURRENT_USER\\Software\\forgetdata\\Reporting Suite 4.0", "InstallLocation",None)
    #MATRIX_PATH= Registry.GetValue("HKEY_CURRENT_USER\\Software\\forgetdata\\Reporting Suite Debug", "InstallLocation",None)
    
    LOCAL_PYLIB=MATRIX_PATH+"\\Lib"
    TEMPLATES_PATH=Registry.GetValue("HKEY_CURRENT_USER\\Software\\forgetdata\\Reporting Suite 4.0", "TemplateInstallLocation",None)
    #TEMPLATES_PATH=Registry.GetValue("HKEY_CURRENT_USER\\Software\\forgetdata\\Reporting Suite Debug", "TemplateInstallLocation",None)
    
    #print "using matrix objects at " + MATRIX_PATH

    if not MATRIX_PATH in sys.path:
        sys.path.insert(1,MATRIX_PATH)
        import clr
        clr.AddReference("ForgetData.Matrix")
        clr.AddReference("ForgetData.Slides.Programability")
        clr.AddReference("PowerPointHandler")
    
    if not TEMPLATES_PATH in sys.path:
        sys.path.insert(1,TEMPLATES_PATH)
    
    if not LOCAL_PYLIB in sys.path:
        sys.path.insert(0,LOCAL_PYLIB)

except:
    pass

def initRootContainer():
    """updated to also return a matrix handler"""

    try:
        from Forgetdata.Slides.PowerPointHandler import CustomActionFactory
        from Forgetdata.Matrix import RootCompositionContainer,MatrixHandler
        from System import Array

        arr = Array[str]([TEMPLATES_PATH])
        if not RootCompositionContainer.IsInitialized:
            RootCompositionContainer.Initialize(CustomActionFactory(arr))
    
        try:
            from log4net import LogManager
            LogManager.GetLogger("logfile"),MatrixHandler.Create()
        except ImportError:
            clr.AddReference("log4net")
            from log4net import LogManager
        return LogManager.GetLogger("logfile"),MatrixHandler.Create()
    except:
        return None

# this initialization will happen at module import
try:
    Log,Handler = initRootContainer()
except:
    pass

def connect(path,name=None, provider_name=None):
    """uses the matrix handler to create a connection to a
    file based datasource"""
    
    try:
        from os.path import splitext

        if not provider_name:
            ext = splitext(path)[-1]
            ext = ext[1:4].lower()
    
            p_map = {"mtd":"SPSS MTD File"
                    , "xml":"Tabs ML"
                    , "xls":"Excel 2007/2010 Provider"}
    
            provider_name = p_map.get(ext, "Matrix File")
    
        if not name:
            name = path
        from Forgetdata.Matrix import ConnectionDefinition
        defn = ConnectionDefinition()
        defn.Name = name
        defn.Provider = provider_name
        defn.ConnectionString = path
    
        c = Handler.CreateConnection(defn)
        if(c == None):
            raise Exception("Unable to open a matrix connection to file:"+ path)
        return c    
    except:
        return None 

    
###not tested..
@property
def getMatrix():
    try:
        return globals.Matrix
    except:
        return None

    