
# issues - srt by column, etc options
# what if sorting nets with multiple  labels that match, eg top 2. 
# using dict and lists and tuples - too complicated ? check why we have each step?
# check data index for concatenated tables.

def sort_rows(Matrix, by_column=0, using_cell_value=0, descending=True, filename=None):
    """Sorts the rows in the active matrix numerically, keeping nets together.

    :param by_column: Use the values in this column to determine the sort
            order of the rows.
    :param using_cell_value: When there are multiple values within a cell
            use this to control which value row within each cell is used
            for sorting (zero-based)
    :param descending: Determines the order in which the values should be
            sorted. Default = True
    :param filename: text file containing a list of row names to fix at the
            end of the table/chart.  filename is located in the pptx
            folder, and contains a comma separated row, e.g.:
            "Other","Don't know","None of these"

    """
    
    def make_dictionary_from_sideaxis(Matrix):
        """Basic sorting within nets, based on col 1, cell item 1 and reverse order."""
            
        def inner_dict(_dict, _indent, _index, _netIndex):
            
            def make_dict(_dict = dict()):
                """Make a dictionary containing the structure of the Axis including Nets"""
                _dict["Value"] = row[by_column][using_cell_value].NumericValue
                _dict["Label"] = row.Member.Label
            
            if row.Member.IndentLevel == _indent:
                
                if _indent == 0:
                    _dict[_index] = dict()
                    make_dict(_dict[_index]) 
                    
                    if row.Member.MemberType == "Net":
                        _netIndex = _index
                                
                elif _indent == 1:
                    _dict[_netIndex][_index] = dict()
                    make_dict(_dict[_netIndex][_index]) 

                    if row.Member.MemberType == "Net":
                        _netIndex2 = _index

                elif _indent == 2:
                    _dict[_netIndex][netIndex2][_index] = dict()
                    make_dict(_dict[_netIndex][netIndex2][_index])
                
                    if row.Member.MemberType == "Net":
                        print "Function only supports 2 levels of nets"
                    
            return _dict, _netIndex
        
        _dict = dict()
        for row in Matrix:
            if row.Member.IndentLevel == 0: #reset after each net
                _netIndex = "-1"               
            _dict, _netIndex = inner_dict(
                                        _dict, row.Member.IndentLevel, 
                                        str(row.Member.DataIndex), _netIndex
                                        )            
        return _dict

    def sorted_list_from_dict(Matrix, _dict):
        """Return a list of tuples including DataIndex, Label and Value"""
        
        sorted_list = list()

        from operator import itemgetter
        
        if descending:
            sort_order = True
        else:
            sort_order = False
            
        sorted_list = list()
        
        _tuple = [(k, _dict[k]["Label"], _dict[k]["Value"]) for k in _dict.keys() if k != "Value" and k != "Label"]
        
        for row in sorted(_tuple, key = itemgetter(2), reverse = sort_order):
            sorted_list.append( row[0])

            try:            
                _tuple2 = [(k2, _dict[row[0]][k2]["Label"], _dict[row[0]][k2]["Value"]) for k2 in _dict[row[0]].keys() if k2 != "Value" and k2 != "Label"]
                
                for row2 in sorted(_tuple2, key = itemgetter(2), reverse = sort_order):
                    sorted_list.append( row2[0])
                
                try:
                    _tuple3 = [(k3, _dict[row[0]][row2[0]][k3]["Label"], _dict[row[0]][row2[0]][k3]["Value"]) for k3 in _dict[row[0][row2[0]]].keys() if k3 != "Value" and k3 != "Label"]
                
                    for row3 in sorted(_tuple3, key = itemgetter(2), reverse = sort_order):
                        sorted_list.append( row3[0])
                except:
                    pass
            except:
                pass
         
        #if filename is not None, place these values at the end
        if filename == None:
            return sorted_list
        
        try:
            from utils.utilities import read_comma_separated_file
            _keep_at_end = read_comma_separated_file(filename)
        except:
            print "Unable to read _file_name: " + filename
            return sorted_list
            
        if _keep_at_end is None:  # there are no specific rows to keep at end.
            return sorted_list
            
        def find_keep_items():
            """if filename is not None, find all items listed and place them at the end of the sorted list"""
            keep = list()
            keep = [int(x) for x in sorted_list for item in _keep_at_end if item == Matrix[int(x)].Member.Label]
            if len(keep) > 0:
                for item in keep:
                    sorted_list.remove(str(item))
                    sorted_list.append(str(item))
        find_keep_items()
        return sorted_list
        
    def reorder_rows(Matrix, sorted_list):
        """Reorder rows of Matrix based on an input list of rows."""
            
        from operator import itemgetter
        
        #for debugging purposes , make this list include the dataIndex, labels and index within the ordered list.
        list_incl_labels = [(i,row.Member.Label, sorted_list.index(i)) for i in sorted_list for row in Matrix  if row.Member.DataIndex == int(i)]
        print "list_incl_labels:", "Original DataIndex, Label, Required position - ", list_incl_labels
        
        for required_row in sorted(list_incl_labels, key=itemgetter(2), reverse=True):
            # matrix labels wil be calculated on each iteration as the 
            # positions of the rows can move each time.
            matrix_labels = [(r.Member.Label,r.Member.DataIndex) for r in Matrix]   
            for r in matrix_labels:
                label = required_row[1]
                current_position = r[1]
                new_position = required_row[2]
                if r[0] == label:
                    if current_position < new_position:
                        for i in range(current_position, new_position):
                            Matrix.SwitchRows(i,i+1)
                    
                    elif  current_position > new_position:
                        for i in reversed(range(new_position,current_position)):
                            Matrix.SwitchRows(i+1,i)
        
        return
    
    reorder_rows(Matrix, sorted_list_from_dict(Matrix, make_dictionary_from_sideaxis(Matrix)))
    
    
