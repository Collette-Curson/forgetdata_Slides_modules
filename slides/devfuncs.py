# devfuncs script will/should install

def addDummyProvider():
    import clr
    clr.AddReference("Forgetdata.Matrix")
    from System.Collections.ObjectModel import ReadOnlyCollection
    from System.Collections.Generic import List
    from System.Reflection import BindingFlags
    from Forgetdata.Matrix import IProvider,MatrixHandler
    import System
    print dir(IProvider)
    class MyProv(IProvider):
        NAME = "extreme provider"
        """
        bool Initialize(IMatrixHandler handler);
        string ProviderName { get; }
        IConnection CreateConnection(ConnectionDefinition connectionDefinition);
        Image Icon { get; }
        string ShowConnectionStringEditor(string existingConnectionString);
        bool IsValidConnectionString(string connectionString);"""

        
        def Initialize(self, handler):
            self.impl = handler.GetProvider("Tabs ML")
            return self.impl != None
        def CreateConnection(self,cdefn):
            return self.impl.CreateConnection(cdefn)

        def get_Icon(self):
            return self.impl.Icon
        
        def get_ProviderName(self):
            return NAME

        def ShowConnectionStringEditor(self, existingConnectionString):
            return impl.ShowConnectionStringEditor(existingConnectionString)

        def IsValidConnectionString(self, connectionString):
            return impl.IsValidConnectionString(connectionString)
    
    h = MatrixHandler.Create()
    m = MyProv()
    m.Initialize(h)

    newList = List[IProvider](h.Providers)
    newList.Add(m)
    print "added in provider"
    t = h.GetType()
    method = t.GetProperty("Providers").GetSetMethod(True)
    print "Set method is called " + method.Name
    parms = System.Array[System.Object]([ReadOnlyCollection[IProvider](newList)])
    method.Invoke(h,parms)
    print h.Providers.Count
    #print [p.ProviderName for p in h.Providers]
def df2():
    pass
def packagewd2():
    
    import api
    from Forgetdata.Slides.PowerPointHandler import PowerPointScripting as ppt, SlidesScripting as ss
    from Forgetdata.Matrix import MatrixHandler
    handler = MatrixHandler.Create()
    ctxt = api.GetDataContext()
    connections = handler.ResolveConnections(ctxt)
    
    itemReferences = []


    for slide in ppt.ActivePresentation.Slides:
            for shape in slide.Shapes:
                link= api.GetShapeLink(shape)
                if link:
                    for item in link.Query.Items:
                        print "adding refrence to table " + item.ConnectionName + " "+ item.TableName
                        
