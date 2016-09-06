

def dumps(obj):
    objType = type(obj)
    ret = str(obj)
    try:
        if(objType == Forgetdata.Matrix.DataQuery):
            ret+= "\nRow Settings:\n %s" % dumps(obj.RowCombinationSettings)
            ret+= "\nColumn Settings:\n %s" % dumps(obj.ColumnCombinationSettings)
            

        elif(objType == Forgetdata.Matrix.QuerySettings):
            ret +="Ignored Types: %s" % list(obj.IgnoredTypes)
    except AttributeError,NameError:
        return "Unable to dump object of type  "+ str(objType)
    return ret