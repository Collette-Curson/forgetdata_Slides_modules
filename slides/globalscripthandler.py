
class globalscripthandler(object):
    def __init__(self):
        try:
            import os
            mydir = os.path.dirname(__file__)
            gf = os.path.join(mydir,"globalfuncs.py")
            dict = {}
            execfile(gf,globals(),dict)
            self.localmod = dict

        except:
            raise


    def getList(self):
       
       return [funcName for funcName in self.localmod if not funcName.startswith("__")]
        
    def getscripthelptext(self,scriptid):
        
        func = self.localmod[scriptid]
        return func.__doc__

    def runglobalscript(self, scriptid):
        
        func = self.localmod[scriptid]
        try:
            func()
        except:

            import sys

            print sys.exc_info()