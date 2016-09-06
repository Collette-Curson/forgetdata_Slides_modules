from unittest import (TestCase, main)

class LabelClass:
    """
    This is a dummy label class which acts a little like
    a Member or group in a Matrix axis
    
    """

    def __init__(self, label, parent=None, cell=None):
        # uppercase names used for compatibility only
        self.Label = label
        self.Parent = parent
        self.Cell=cell
        self.Children = []
        self.Values = []
        
        if parent:
            print "self/parent ", parent, " - ", self
            parent.Children.append(self)
        if cell:
            print "cell values", cell, self
            cell.Values.append(self)

    def add(self, label=""):
            rv = LabelClass(label, parent=self)
            
    def addValue(self, label=""):
            rv = LabelClass(label, cell=self)
            
    def __str__(self):
        return self.Label
        

class FillSimulation(TestCase):
    test_axis = LabelClass("Q1 - What is your gender")
    #add children
    male = test_axis.add("Male")
    female = test_axis.add("Female")
    #add 2nd level children
    malechild1 = test_axis.Children[0].add("Child 1")
    malechild2 = test_axis.Children[0].add("Child 2")
    femalechild1 = test_axis.Children[1].add("Child 3")
    femalechild2 = test_axis.Children[1].add("Child 4")
    #add cell values
    val1=test_axis.Children[0].addValue("100")
    val2=test_axis.Children[0].addValue("98")
    val3=test_axis.Children[1].addValue("88")
    val4=test_axis.Children[1].addValue("27")
    #add 2nd level cell values
    val5=test_axis.Children[0].Children[0].addValue("12")
    val6=test_axis.Children[0].Children[1].addValue("14")
    
    def test_fill_defaults(self):
        """ simulates being default settings for different labels within object"""
        
        from format_labels import FormatSettings
        
        settings = FormatSettings()
        
        #top level label
        label = settings.label_format(self.test_axis)
        self.assertEqual(label,self.test_axis.Label)
        
        #children
        for child in self.test_axis.Children:
            label = settings.label_format(child)
            self.assertEqual(label,child.Label)
    
        #2nd level children
        for child in self.test_axis.Children:
            for item in child.Children:
                label = settings.label_format(item)
                self.assertEqual(label,item.Label)
        #individual items
        label = settings.label_format(self.test_axis.Children[0])
        self.assertEqual(label,self.test_axis.Children[0].Label)
        
        label = settings.label_format(self.test_axis.Children[0].Children[0])
        self.assertEqual(label,self.test_axis.Children[0].Children[0].Label)
       
        
    def test_fill_simple_format(self):
        """ simulates what might happen during a
        fill with a string format given as an argument
        
        """
        
        from format_labels import FormatSettings
        
        settings = FormatSettings(label_format="{0.Parent};{0}")
        
        #children
        for child in self.test_axis.Children:
            label = settings.label_format(child)
            expected = child.Parent.Label + ";" + child.Label
            self.assertEqual(expected,label)
        
        #2nd level children
        for child in self.test_axis.Children:
            for item in child.Children:
                label = settings.label_format(item)
                expected = item.Parent.Label + ";" + item.Label
                self.assertEqual(expected,label)

    def test_fill_complex_format(self):
        """ simulates what might happen during a
        fill with a string format given as an argument
        
        """
        
        from format_labels import FormatSettings
        
        settings = FormatSettings(label_format="Parent: {0.Parent} - Label: {0}")
        
        #children
        for child in self.test_axis.Children:
            label = settings.label_format(child)
            expected = "Parent: " + child.Parent.Label + " - Label: " + child.Label
            self.assertEqual(expected,label)
        
        #2nd level children
        for child in self.test_axis.Children:
            for item in child.Children:
                label = settings.label_format(item)
                expected = "Parent: " + item.Parent.Label + " - Label: " + item.Label
                self.assertEqual(expected,label)

    def test_replacement_func(self):
        """ simulates what might happen in a fill if a custom function is used 
        to format arguments, for example to replace texts.
        
        """
        
        from format_labels import FormatSettings

        corrections =  {"Male": "m",
                    "Female": "f",
                    "Child": "ch"}

        def lookup_label_format( item ):
            """ run the replacement texts on the string"""
            
            #make sure its a string
            item = str(item)
            for key in corrections.keys():
                item = item.replace(key,corrections[key])
            return item

        settings = FormatSettings(label_format = lookup_label_format)
        
        #children
        for child in self.test_axis.Children:
            label = settings.label_format(child)
            if child.Label == "Male":
                expected = "m"
            if child.Label == "Female":
                expected = "f"

            self.assertEqual(expected,label)

        #2nd level child
        for child in self.test_axis.Children:
            for item in child.Children:
                label = settings.label_format(item)
            if "Child" in item.Label:
                expected = "ch " + label.split("ch ")[1]

            self.assertEqual(expected,label)

    def test_fill_cell_defaults(self):
        """ simulates being default settings for different cell values
        
        settings = FormatSettings(cell_format = "{0}")
        
        """
        
        from format_labels import FormatSettings
        
        settings = FormatSettings(cell_format = "{0}")
        
        #children
        for child in self.test_axis.Children:
            for val in child.Values:
                label = settings.cell_format(val)
                self.assertEqual(label,str(val))
                
        #2nd level children
        for child in self.test_axis.Children:
            for item in child.Children:
                for val in item.Values:
                    label = settings.label_format(val)
                    self.assertEqual(label,str(val))

    def test_fill_cell_pre_suffix(self):
        """ simulates being default settings for different cell values
        
        settings = FormatSettings(cell_format = "prefix: {0}, suffix")
        
        """
        
        from format_labels import FormatSettings
        
        settings = FormatSettings(cell_format = "prefix: {0}, suffix")
        
        #children
        for child in self.test_axis.Children:
            for val in child.Values:
                label = settings.cell_format(val)
                expected = "prefix: " + str(val) + ", suffix"
                self.assertEqual(label, expected)
                
        #2nd level children
        for child in self.test_axis.Children:
            for item in child.Children:
                for val in item.Values:
                    label = settings.cell_format(val)
                    expected = "prefix: " + str(val) + ", suffix"
                    self.assertEqual(label, expected)
    
    def test_fill_cell_complex(self):
        """ simulates being default settings for different cell values
        
        settings = FormatSettings(cell_format = "{0} - (n={1})")
        
        """
        
        from format_labels import FormatSettings
                   
        #children        
        for child in self.test_axis.Children:
            #use default cell_format for getting values into list, 
            #which can then be formatted
            settings = FormatSettings(cell_format = "{0}")
            vals=list()
            for val in child.Values:
                vals.append(settings.cell_format(str(val)))
                
            settings = FormatSettings(cell_format = "{0} - (n={1})")
            label = settings.cell_format(child,vals)
            expected = child.Label + " - (n=" + str(vals) + ")"
            self.assertEqual(label, expected)
                
        #2nd level children
        for child in self.test_axis.Children:
            for item in child.Children:
                settings = FormatSettings(cell_format = "{0}")
                vals=list()
                if item.Values.__len__() > 0:
                    for val in item.Values:
                        vals.append(settings.cell_format(str(val)))
                    settings = FormatSettings(cell_format = "{0} - (n={1})")
                    label = settings.cell_format(item,vals)
                    expected = item.Label + " - (n=" + str(vals) +")"
                    self.assertEqual(label, expected)
                    
if __name__ == "__main__":
    main()
