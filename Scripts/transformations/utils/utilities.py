"""Provides utility functions for use with the Scripts installed with Slides!"""

def read_comma_separated_file(_file_name, val = None):
    """Read a named csv file and return the values

    This is used within the sort_columns() and sort_rows() functions for reading
    from a fixed.txt file for fixed position rows/columns within the sorting.
    
    """

    import _csv
    global _f
    print ("_file_name: ", str(_file_name))
    try:
        _f = _csv.reader(open(_file_name, "r"))
        for row in _f:
            if val is not None:
                if (row[0] == val):
                    return row[1:]
            else:
                return row

    except:
        print ("_file_name was not found: " + str(_file_name))
        _file_name = None
        return

def write_js_file(list, OutputFile):
    r"""Provides basic functions for reading and writing to json/java script files. 

    Use this function to write out a js file. 
    
    :param list: the information to be stored in the file.
    :param OutputFile: the location you wish to store the file

    Examples:
    
    | a=list()
    | a.append(dict(inp="Some text", outp="Some Replacement Text"))
    | a.append(dict(inp="Some other text", outp="Some Other Replacement Text"))
    | file = "C:\\temp\\outputfile.js"
    | writeJSfile(a,file)
    """
    
    import json
    import codecs
    import os
    json_list = json.dumps(list)
    json_loads = json.loads(json_list)

    file = codecs.open(OutputFile, "w", "utf-8-sig")
    json.dump(json_loads, file)
    file.close()

def read_js_file(InputFile):
    r"""Provides basic functions for reading and writing to json/java script files. 

    Use this function to read a js file. 
    The function returns the file.   
    
    :param InputFile: the file location of the  file you wish to read.
    
    Examples:
    
    | input = C:\\temp\\inputFile.js
    | json_file=read_js_file(input)
    """
    
    import json
    import codecs
    import os
    file = codecs.open(InputFile, "r", "utf-8-sig")
    json_file = json.load(file)
    return json_file

def print_matrix(matrix,colWidth=11,maxWidth=80):
    """Print a friendly output representing the current Matrix"""
    
    print ""
    if matrix.Name:
        print "Name : " + "%.60s" % matrix.Name
    if matrix.Label:
        print "Label : " + "%.60s" % matrix.Name

    colFmtWidth=colWidth - 1

    stringFmt = "%" + str(colFmtWidth) + "." + str(colFmtWidth) + "s"
    header = ("X" * colFmtWidth) + "|"

    for top in matrix.TopAxis.DataMembers:
        try:
            if top.MemberSigTestHeading != "":
                stat = " (" + top.MemberSigTestHeading + ")"
            else:
                stat = ""
        except:
            stat = ""
            
        header += stringFmt % ( top.Label ) + stat + "|"

    print header

    desiredWidth= (matrix.TopAxis.DataMembers.Count +1) * colWidth
    if(desiredWidth > maxWidth):
        print "=" * maxWidth
    else:
        print "=" * desiredWidth


    for row in matrix:

        strRow = stringFmt % row.Member.Label +  "|"

        for cell in row:
            try:
                if cell.SigTestResult != "":
                    statResult = " (" + cell.SigTestResult + ")"
                else:
                    statResult = ""
            except:
                statResult = ""
            if(cell.Count == 0):
                strRow +=stringFmt % ""
            else:
                strRow += stringFmt % str(cell[0]) + statResult
            strRow +="|"
        print (strRow)
    try:
        print "Matrix Label = ", Matrix.Label
        print "SideGroup0  Label = ", Matrix.SideAxis.Groups[0].Label
        print "TopGroup0 Label = ", Matrix.TopAxis.Groups[0].Label
        print "Header Left = ", Matrix.Header.Left
        print "Header Right = ", Matrix.Header.Right
        print "Footer Left = ", Matrix.Footer.Left
        print "Footer Right = ", Matrix.Footer.Right
        print "\n"
    except:
        pass
    print ""

def find_table(Connections, query_item):
    """Using the Queryitems from the selection within the Matrix, look up the
    Table name and return the connected table.  
    
    """
    
    for conn in Connections:
        if(conn.Name == query_item.ConnectionName):
            return conn[query_item.TableName]
    return None    