"""Provides basic matrix manipulation functions for filling the matrix from the
existing current selections.


Note this module is not included in the main transformations class as it
requires Connections and Query to be passed as parameters to this class. 
These are used as the lookup for the Table which as used for the selection.
Transformations classes only require the Matrix as a parameter.
 

Updated October 2016
@author: ccurson

"""
#from globals import Matrix

__version__ = '4.3.0'
#from functools import wraps

class FillMatrix():
    r"""This class is designed to be used when handling very large reports and
    selecting from large tables.  This class will take any existing selections
    and autofill the matrix with all rows or columns matching the existing
    selections from the underlying tables.
    
    :param Matrix: Current connected Matrix
    :param Connections: Connections to report files found in the current
            pptx file.
    :param Query.Items: Query Items used within the selections in the current 
            Matrix.    

    Example:
    
    | import transformations.auto_fill_matrix as fill
    | myfillclass = fill.FillMatrix(Matrix, Connections, Query)
    | myfillclass.auto_fill_rows(5, sort=True)
        
    """
    
    def __init__(self, matrix, connections, query):    
        self.matrix = matrix        
        self.connections = connections
        self.query = query
        try:
            self.query_items = query.Items
        except:
            pass
        self._rows = matrix.Count
        self._columns = matrix.TopAxis.DataMembers.Count
        self.limit_series = None
 
    
    def _get_table_from_connection_and_fill(self, fill_rows, limit_series, sort):
        """For each selection in this matrix, find which table it's connected
        to, and from that table, select out the top N brand rows/columns 
        (based on the sort order of the first selection) and insert them into
        the matrix as new rows/columns.
        
        """        
        
        import transformations.utils.utilities as utilities
            
        def _get_selected(table, query_item, fill_rows):
            """Return the column or rows of the table that are selected, using
            the Query's ColumnSelection and RowSelection
        
            eg selected =  [0]

            """      
                  
            def _get_selection_items(selection):
                """Return which rows or columns are included in the selection"""
                
                if fill_rows:
                    count = table.Count
                else:
                    count = table.TopAxis.DataMembers.Count
                    
                if  selection == "/": # row or all selected
                    return [i for i in range(0, count)] 
                    
                elif selection[0] == "/": # cell or group selected
                    group_selected = int(selection[1:].split("[")[0])
                    counter=0
                    try: # cell selected
                        _row_col = int(selection[1:].split("[")[1].split("]")[0])                    
                        for i in range(0, group_selected):    
                            if fill_rows:
                                counter += table.SideAxis.Groups[i].Count
                            else:
                                counter += table.TopAxis.Groups[i].Count
                        counter += _row_col
                        return [counter]
                    
                    except: #entire group selected
                        if fill_rows:
                            return [i for i in range(0, count) if table.SideAxis.DataMembers[i].Group.SortIndex == group_selected] 
                        else:
                            return [i for i in range(0, table.TopAxis.DataMembers.Count) if table.TopAxis.DataMembers[i].Group.SortIndex == group_selected]  
            
            if fill_rows:
                return _get_selection_items(query_item.RowSelection)
            
            else:
                return _get_selection_items(query_item.ColumnSelection)
        
        def _get_sorted_list_from_table(table, query_item, number, sort,
                                             brand_list = list()):
            """Create a set containing (Label, Row_DataIndex, Column_DataIndex,
            CellItem0, FormatString, QueryItem) the each row/column of the
            connected table. Sort order is established only from the first
            connection when there are multiple connections, 
            i.e when "brand_list" is empty.
            
            """
            
            cell_item =  0
            
            # get a full list of all rows/cols in the table for inserting into the matrix.
            if fill_rows:
                print "fill rows"
                set_of_items = ([col.TopMember.Group.Label + " :: " + col.TopMember.Label, number,
                                 col.TopMember.DataIndex,
                                 col[cell_item].GetNumericValue(),
                                 col[cell_item].FormatString, query_item]
                                for col in table[number] if col.Count > 0 and 
                                (brand_list.__len__() == 0 or 
                                 col.TopMember.Label in brand_list) and 
                                 col.TopMember.IsVisible == True)
                #print "set_of_items" , list(set_of_items)
            else:
                print "fill columns"
                set_of_items = ([row.Member.Group.Label + " :: " + row.Member.Label, row.Member.DataIndex,
                                 number, row[number][cell_item].GetNumericValue(),
                                 row[number][cell_item].FormatString, query_item] 
                                for row in table if row[number].Count > 0 and 
                                (brand_list.__len__() == 0 or 
                                 row.Member.Label in brand_list) and 
                                 row.Member.IsVisible == True)
            
            # sort the list only for the first selection in the Matrix.
            # For remaining selections, use first selection's sort order
            def _get_key(item):                
                return item[3] # sort by Numeric Value
            
            if sort == True and brand_list.__len__() == 0:   
                sorted_list = sorted(set_of_items, key=_get_key, reverse=True)
            else:
                sorted_list = list(set_of_items)
             
            #print "sorted_list ", sorted_list
             
            #get unique rows/columns only, in case of duplicate row or columns
            unique_set = set([item[0] for item in sorted_list])
            #print unique_set
            
            if unique_set.__len__() <  sorted_list.__len__():
                # There are non-unique items, only select the unique ones for insert                
                print "There are multiple rows within one group the same text to be sorted"
                new_sorted_list = list()
                
                if brand_list.__len__() == 0: # first selection, get sort order with only uniquevalues.
                    for item in sorted_list:
                        if new_sorted_list.__len__() < self.limit_series:
                            #print "new_sorted_list", new_sorted_list
                            temp_list = set([itemx[0] for itemx in new_sorted_list])
                            if item[0] not in temp_list:
                                new_sorted_list.append(item)
                else: # subsequent selections, add additional items

                    for item in sorted_list:
                        brand = item[0].split(" :: ")[1]
                        if new_sorted_list.__len__() < self.limit_series:
                            temp_list = set([itemx[0].split(" :: ")[1] for itemx in new_sorted_list])
                            if brand in brand_list and brand not in temp_list:
                                new_sorted_list.append(item)

            else: # only contains unique items

                if brand_list.__len__() == 0: # first selection
                    new_sorted_list = sorted_list[0:self.limit_series]

                else: # subsequent selections,
                    new_sorted_list = list()
                    for item in sorted_list:
                        if new_sorted_list.__len__() < self.limit_series:
                            if item[0].split(" :: ")[1] in brand_list:
                                new_sorted_list.append(item)      
            return new_sorted_list
            
        def _get_table_list(brand_list,):
            """Return the sorted list of items to be inserted into the table"""
            
            table_list = list()
                        
            # add the equivalent list from the remaining connections.
            for i in range(0, self.query_items.Count):
                table = utilities.find_table(self.connections, self.query_items[i]) 
                if table is not None:
                    selected =_get_selected(table, self.query_items[i], fill_rows)
                    for item in selected:
                        table_list.append(list(_get_sorted_list_from_table(table, i, item, sort, brand_list)))
            return table_list
        
        table = utilities.find_table(self.connections, self.query_items[0])
        
        first_selected =_get_selected(table, self.query_items[0], fill_rows)
        
        if limit_series is None:            
            if fill_rows:  # this is the number of columns to add per row
                self.limit_series = table.TopAxis.DataMembers.Count
            else:
                self.limit_series = table.Count
        else:
            self.limit_series = limit_series
                        
        #brand_list is not set at this point, so brand_list = list()
        
        filtered_list = _get_sorted_list_from_table(table, 0, first_selected[0], sort)
        print  "filtered_list ", filtered_list
        
        brand_list = [item[0].split(" :: ")[1] for item in filtered_list]        
        
        table_list = ()
        table_list = _get_table_list(brand_list)
        
        insert_rows = fill_rows
        if self.query.SwitchRowsAndColumns == True:
            if fill_rows == True:
                insert_rows = False
            else:
                insert_rows = True
        
        for item in brand_list:
            label = item
            if insert_rows:  # note when filling rows, you add columns 
                first_fill_col = self.matrix.TopAxis.DataMembers[self.matrix.TopAxis.DataMembers.Count-1]
                newCol = self.matrix.InsertBlankColumnAfter(first_fill_col, label, label)            
            else: # note when filling columns, you add rows
                first_fill_row = self.matrix.SideAxis.DataMembers[self.matrix.Count-1]
                newRow = self.matrix.InsertBlankRowAfter(first_fill_row, label, label)  
        
        # delete the original selections as these were not included in the top
        # N brands
        if insert_rows == True:
            for col in reversed(range(0, self._columns)):
                self.matrix.DeleteColumn(col)
        else:
            for row in reversed(range(0, self._rows)):
                self.matrix.DeleteRow(row)

        # for each connection, insert the data from the corresponding table
        # into the rows or columns
        
        _rows_or_cols_added = list()
        i = 0
        #print "table_list", table_list
        for list_of_brands in table_list: # this is per selection in Slides.
            query_item = list_of_brands[0][5]
            table = utilities.find_table(self.connections, self.query_items[query_item])
            
            if table is not None:
                if insert_rows:
                    #if list_of_brands[0][1] not in _rows_or_cols_added:
                    _rows_or_cols_added.append(list_of_brands[0][1])
                    for col in self.matrix[0]:
                        item2 = [item for item in list_of_brands if col.TopMember.Label == item[0].split(" :: ")[1]]
                        if item2.__len__() > 0:
                            index = col.TopMember.DataIndex
                            if item2[0][3] is not None:
                                self.matrix[i][index].AddValue(str(float(item2[0][3])))
                                self.matrix[i][index][0].FormatString = item2[0][4]
                    i+=1
                    
                else:
                    #if list_of_brands[0][2] not in _rows_or_cols_added:
                    _rows_or_cols_added.append(list_of_brands[0][2])
                    j = 0
                    counter = 0
                    for row in self.matrix:
                        item2 = [item for item in list_of_brands if row.Member.Label == item[0].split(" :: ")[1]]
                        
                        if item2.__len__() > 0:
                            index = row.Member.DataIndex
                            if item2[0][3] is not None:
                                #if item2.__len__() > 1 and index < item2.__len__() or item2.__len__()== 1:
                                    
                                self.matrix[index][i].AddValue(str(float(item2[0][3])))
                                self.matrix[index][i][0].FormatString = item2[0][4]
              
                    i+=1
                
    
    def _set_selection_to_all(self, fill_rows):
        """set the RowSelection or ColumnSelection to '/' to select all"""
        
        for row in self.matrix:
            for col in row:
                cell = col.AttachedToQuery
                if fill_rows:
                    try:
                        cell.ColumnSelection = "/"
                    except:
                            pass    
                else:
                    try:
                        cell.RowSelection = "/"
                    except:
                        pass
                    
    def _get_table(self, item):
        """Return the connected table"""
        
        import transformations.utils.utilities as utilities
        try:
            return utilities.find_table(self.connections, self.query_items[item])
        except:
            pass
    
    
    def _do_sort(self, fill_rows):
        """Sort the values"""
        
        import transformations as tr
        myclass = tr.MatrixManipulator(self.matrix)
        if fill_rows:
            if self.query.SwitchRowsAndColumns == False:
                myclass.sort_columns()
            else:
                myclass.sort_rows()
        else:
            if self.query.SwitchRowsAndColumns == False:
                myclass.sort_rows()
            else:
                myclass.sort_columns()
    
    def _do_limit_series(self, limit_series, fill_rows):
        """limit the series inserted if limit_series is set"""
        
        if fill_rows:
            if self.matrix.TopAxis.DataMembers.Count > limit_series:
                for i in reversed(range(limit_series,self.matrix.TopAxis.DataMembers.Count)):
                    try:
                        self.matrix.DeleteColumn(i)
                    except:
                        pass
        else:
            if self.matrix.Count > limit_series:
                for i in reversed(range(limit_series,self.matrix.Count)):
                    try:
                        self.matrix.DeleteRow(i)
                    except:
                        pass
                           
    def auto_fill_rows(self, limit_series = None, sort=False):
        """Automatically fill the rows of the selected Matrix from the
        underlying connected table.
        
        For example, use Shape settings to select one cell from the required
        row, and use fillMatrix.auto_fill_rows() to fill up the remaining row
        from the connected table.
        
        :param limit_series: Only add the first N rows
        :param sort: Sort the rows before adding them to the Matrix.
        
        Used together, limit_series and sort can enable you to add the top N
        rows to the selection.
        
        Example:
        
        | import transformations.auto_fill_matrix as fill
        | myfillclass = fill.FillMatrix(Matrix, Connections, Query)
        | myfillclass.auto_fill_rows(5, sort=True)
        
        """
    
        table = self._get_table(0)
        
        fill_rows = True
        # Use more complex selection for filling rows if SimplifyOutPut is
        # enabled, or if the table is large
        num_cols = table.TopAxis.DataMembers.Count
        ##TODO change this back to 200
        try:
            if self.query.SimplifyOutput == True or num_cols > 120:
                self._get_table_from_connection_and_fill(fill_rows, limit_series, sort)
        
        except: # update basic selection to all rows
            self._set_selection_to_all(fill_rows)
       
            if sort == True:
                self._do_sort(fill_rows)
                
            if limit_series is not None:
                self._do_limit_series(limit_series, fill_rows)
            
            
    def auto_fill_columns(self, limit_series = None, sort=False):
        """Automatically fill the columns of the selected Matrix from the
        underlying connected table.
        
        For example, use Shape settings to select one cell from the required
        column, and use fillMatrix.auto_fill_columns() to fill up the remaining
        column from the connected table.         
        
        :param limit_series: Only add the first N columns
        :param sort: Sort the columns before adding them to the Matrix
        
        Used together, limit_series and sort can enable you to add the top N
        columns to the selection.
        
        Example:
        
        | import transformations.auto_fill_matrix as fill
        | myfillclass = fill.FillMatrix(Matrix, Connections, Query)
        | myfillclass.auto_fill_columns(5, sort=True)

        """
        
        table = self._get_table(0) 
        
        fill_rows = False
        
        # Use more complex selection for filling columns if SimplifyOutPut is
        # enabled, or if the table is large
        
        ##TODO change this back to 200
        try:
            if self.query.SimplifyOutput == True or table.Count > 120:
                self._get_table_from_connection_and_fill(fill_rows, limit_series, sort)
        except: # update basic selection to all rows
            self._set_selection_to_all(fill_rows)
    
        
            if sort == True:
                self._do_sort(fill_rows)
            
            if limit_series is not None: # delete the remaining rows
                self._do_limit_series(limit_series, fill_rows)
                
if __name__ == "__main__":
    import doctest
    doctest.testmod()


"""
To run doctest, using a command prompt, go to:

cd C:\Projects\RepSuite\Releases\4.3\Forgetdata\Libraries\Lib\forgetdata\Scripts>
>python transformations\auto_fill_matrix.py

"""