from unittest import (TestCase, main)
import sys, os
lib_path = os.path.abspath(os.path.join('..'))   #relative path to transformations\utils\
sys.path.append(lib_path)
import slidesconf
import utils.matrixfuncs as t

class MatrixFillSimulation(TestCase):
    """simulate matrix scenarios such as adding (n=xx) on row labels or Group 
    headings added to rows.
    Also examples of formatting cell values
    
    """
    
    m = t.create_test_matrix()
    
    def test_fill_defaults(self):
        """ simulates what might happen during a fill with default arguments"""

        from format_labels import FormatSettings
                
        settings = FormatSettings()
        
        #matrix  
        label = settings.label_format(self.m) 
        ##- This fails currently as matrix has no str() function set on it 
        ##- instead it returns the object.
        #####---------> 
        #self.assertEqual(label, self.m)  
        
        #rows
        for child in self.m: 
            label = settings.label_format(child.Member)
            self.assertEqual(label, child.Member.Label)
            
        #cols
        for child in self.m[0]:
            label = settings.label_format(child.TopMember)
            self.assertEqual(label, child.TopMember.Label)
            
        #side group
        for group in self.m.SideAxis.Groups:
            label = settings.label_format(group)
            self.assertEqual(label, group.Label)
        
        #top group
        for group in self.m.TopAxis.Groups:
            label = settings.label_format(group)
            self.assertEqual(label, group.Label)
                            
    def test_fill_simple_format(self):
        """ simulates what might happen during a fill with a string format 
        given as an argument
        
        """
        
        from format_labels import FormatSettings
        
        settings = FormatSettings(label_format="{0.Group};{0}")
        #rows
        for child in self.m:
            label = settings.label_format(child.Member)
            expected = child.Member.Group.Label +";" + child.Member.Label
            self.assertEqual(expected,label)
        
        #cols
        for child in self.m[0]:
            label = settings.label_format(child.TopMember)
            expected = child.TopMember.Group.Label +";" + child.TopMember.Label
            self.assertEqual(expected,label)
        
    def test_replacement_func(self):
        """simulates what might happen in a fill if a custom function is used 
        to format arguments
        
        """
        
        from format_labels import FormatSettings
        
        corrections =  {"RowGroup": "Row Group", "myRow": "My Row", "ColumnGroup": "Column Group", "myColumn": "My Column"}

        def lookup_label_format( item ):
            """run the replacement texts on the string"""
            
            #make sure item is a string
            item = str(item)
            for key in corrections.keys():
                item = item.replace(key,corrections[key])
            return item
            
        settings = FormatSettings(label_format = lookup_label_format) # pass a function to the format simulates
        settings2 = FormatSettings(label_format = "{0.Group}: {0}")
       
        #rows
        for row in self.m:
            label = settings2.label_format(row.Member)
            label = settings.label_format(label) # replace existing texts
            expected = (row.Member.Group.Label + ": " + row.Member.Label).replace("RowGroup", "Row Group").replace("myRow", "My Row")
            self.assertEqual(expected,label)

        #cols
        for col in self.m[0]:
            label = settings2.label_format(col.TopMember)
            label = settings.label_format(label) # replace existing texts
            expected = (col.TopMember.Group.Label + ": " + col.TopMember.Label).replace("ColumnGroup", "Column Group").replace("myColumn", "My Column")
            self.assertEqual(expected,label)
            
        settings2 = FormatSettings(label_format = "{0};{0.Count}")
        
        #side groups
        for group in self.m.SideAxis.Groups:
            label = settings2.label_format(group)
            label = settings.label_format(label) # replace existing texts
            expected = (group.Label + ";" + str(group.Count)).replace("RowGroup", "Row Group").replace("myRow", "My Row")
            self.assertEqual(expected,label)

        #top groups
        for group in self.m.TopAxis.Groups:
            label = settings2.label_format(group)
            label = settings.label_format(label) # replace existing texts
            expected = (group.Label + ";" + str(group.Count)).replace("ColumnGroup", "Column Group").replace("myColumn", "My Column")
            self.assertEqual(expected,label)
            
    def test_fill_cell_format(self):
        """ simulates a fill with a string format for cell items passed as 
        argument
        
        """
        
        from format_labels import FormatSettings
        
        #cell value 0
        settings = FormatSettings(cell_format="before {0} after")
        for row in self.m:
            for col in row:
                label = settings.cell_format(col[0])
                expected = "before " + col[0].Value + " after"
                self.assertEqual(expected,label)
        
        #add cell value
        for row in self.m:
            for col in row:
                col.AddValue(str(10),None) #add,None to run in python.
        
        #cell value 1
        for row in self.m:
            for col in row:            
                label = settings.cell_format(col[1])
                expected = "before " + col[1].Value + " after"
                self.assertEqual(expected,label)
                
    def test_fill_cell_format_with_row_label(self):
        """ simulates a fill with a string format for cell items passed as 
        argument
        
        """
        
        from format_labels import FormatSettings
        
        #cell value 0
        settings = FormatSettings(cell_format="{0.SideMember} - {0[0].Value}")
        for row in self.m:
            for col in row:
                label = settings.cell_format(col)
                expected = row.Member.Label + " - " + str(col[0].Value)
                self.assertEqual(expected,label)
        
        #cell value 1
        settings = FormatSettings(cell_format="{0.SideMember} - {0[1].Value}")
        for row in self.m:
            for col in row:
                label = settings.cell_format(col)
                expected = row.Member.Label + " - " + str(col[1].Value)
                self.assertEqual(expected,label)
                
                
    def test_fill_label_and_cell_format(self):
        """ simulates a fill with a string format for row and cell items passed as 
        argument
        
        """
        
        from format_labels import FormatSettings
        
        #cell item 0
        settings = FormatSettings(label_format = "{0.SideMember.Group} - {0.SideMember} - {0.TopMember.Group} - {0.TopMember} - (n = {0[0].Value})",cell_format="{0.SideMember} - {0[0].Value}")
        for row in self.m:
            label = settings.label_format(row[0])
            expected = row.Member.Group.Label + " - " + row.Member.Label + " - " + row[0].TopMember.Group.Label + " - " + row[0].TopMember.Label + " - (n = " + row[0][0].Value +")"
            self.assertEqual(expected,label)  
        
        #cell item 1
        settings = FormatSettings(label_format = "{0.SideMember.Group} - {0.SideMember} - {0.TopMember.Group} - {0.TopMember} - (n = {0[0].Value})",cell_format="{0.SideMember} - {0[0].Value}")
        for row in self.m:
            for col in row:
                label2 = settings.cell_format(col)
                expected2 = col.SideMember.Label + " - " + col[0].Value
                self.assertEqual(expected2,label2)        
        
    def test_update_matrix_with_labels_and_cells(self):
        """simulate the update of the matrix with new formatted labels for 
        rows and cell items
        
        """
        
        from format_labels import FormatSettings
        
        settings = FormatSettings(label_format = "{0.SideMember.Group} - {0[0].Value}",cell_format="{0.SideMember} - {0[0].Value}")
        
        init_row = self.m[0].Member.Label
        init_col = self.m[0].TopMember.Label
        init_cell = self.m[0][0][0].Value
        init_cell2 = self.m[0][0][1].Value
        
        #update the cell values to "{0.SideMember} - {0[0].Value}"
        settings = FormatSettings(label_format = "{0.SideMember.Group} - {0[0].Value}",cell_format="{0.SideMember} - {0[0].Value}")
        for row in self.m:
            for col in row:
                col[0].Value = settings.cell_format(col)
        
        settings = FormatSettings(label_format = "{0.SideMember.Group} - {0[0].Value}",cell_format="{0.TopMember} - {0[1].Value}")
        for row in self.m:
            for col in row:
                col[1].Value = settings.cell_format(col)
                
        #update the labels to "{0.SideMember.Group} - {0[0].Value}"
        settings = FormatSettings(label_format = "{0.SideMember.Group} - {0[0].Value}",cell_format="{0.SideMember} - {0[0].Value}")
        for row in self.m:
            row.Member.Label = settings.label_format(row[0])
            
        labels = [row.Member.Label for row in self.m]
        expected = [row[0].SideMember.Group.Label + " - " + row[0][0].Value for row in self.m]
        self.assertEqual(labels,expected)
        
        self.assertEqual(self.m[0][0][0].Value, init_row + " - " + init_cell)
        self.assertEqual(self.m[0][0][1].Value, init_col + " - " + init_cell2)
        
    def test_update_matrix_with_labels_and_cells(self):
        """simulate the update of the matrix with new formatted labels for 
        rows and column items
        
        """
        
        from format_labels import FormatSettings
        
        settings = FormatSettings(label_format = "{0.Group} - {0}")
        
        row_expected = [row.Member.Group.Label + " - " + row.Member.Label for row in self.m]
        col_expected = [col.TopMember.Group.Label + " - " + col.TopMember.Label for col in self.m[0]]
        
        for row in self.m:
            row.Member.Label = settings.label_format(row.Member)
               
        for col in self.m[0]:
            col.TopMember.Label = settings.label_format(col.TopMember)
        
        row_labels = [row.Member.Label for row in self.m]
        col_labels = [col.TopMember.Label for col in self.m[0]]
        
        self.assertEqual(row_labels,row_expected)
        self.assertEqual(col_labels,col_expected)
    
    def test_update_all_cell_values_into_one_cell(self):
        """simulate the update of the matrix with new formatted cell item 
        containing all cell values.
        
        """
        
        from format_labels import FormatSettings
        
        m = t.create_test_matrix()
        
        #add cell value
        for row in m:
            for col in row:
                col.AddValue(str(10),None) #add,None to run in python.
        
        settings = FormatSettings(cell_format = "{0[0].Value} - {0[1].Value}")
        
        expected = list()
        for  row in m:
            for col in row:
                expected.append(col[0].Value + " - " + col[1].Value)
        
        for row in m:
            for col in row:
                col[0].Value = settings.cell_format(col) 
        
        values = list()
        for  row in m:
            for col in row:
                values.append(col[0].Value)
        
        self.assertEqual(values,expected)
        
    def test_formatstring_cells_and_format(self):
        """simulate the update of the matrix with new formatted cell item using
        formatString and also format cell item
        
        """
        
        from format_labels import FormatSettings
        settings = FormatSettings(cell_format = "{0[0].Value} - {0.TopMember}")
        
        m = t.create_test_matrix()
        
        expected = list()
        for row in m:
            for col in row:
                col[0].FormatString="0.00"
                expected.append(str(col[0].Value) + " - " + col.TopMember.Label)
        
        #add a FormatString.
        for row in m:
            for col in row:
                col[0].FormatString="0.00"                
        
        for row in m:
            for col in row:
                col[0].Value = settings.cell_format(col) 
        
        values = list()
        for  row in m:
            for col in row:
                values.append(col[0].Value)
        
        self.assertEqual(values,expected)
        
if __name__ == "__main__":
    main()
