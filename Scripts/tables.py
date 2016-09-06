"""Provides a series of functions which will run against Tables shapes within
PowerPoint, after the Tables Shape has been filled.

"""

__version__ = '4.3.0'


def add_group_names_to_table_column_header(Table, Matrix=None):
    """Adds group names to first row, and merges the headings per group.

    NOTE: This MUST be run with delete_table_row_before_fill() which will
    delete any previous cell merging from the table.  Otherwise the cell
    merges will be applied to the rows of the filled table.

    :param Table: Table shape
    :param Matrix: Matrix associated with the Table. Default is None
 
    """

    if Matrix is None:
        from globals import Matrix
    from globals import Log

    _col_count = Table.Columns.Count

    def _add_group_headers():
        """Add the group headings to the first column per group"""

        # Add a new first row for group headers
        Table.Rows.Add(1)

        _previous_group = ""
        for col in range(0, Matrix.TopAxis.DataMembers.Count):
            if _col_count < col+2:
                print "not enough cols: ", str(col+2)
                return

            _cell = Table.Cell(1, col+2)  # row1, col starting from 2.
            if Matrix.TopAxis.DataMembers[col].Group.Label != _previous_group:
                _label = Matrix.TopAxis.DataMembers[col].Group.Label
                _cell.Shape.TextFrame.TextRange.Text = _label
            _previous_group = _label
        Log.Info("Added Group Labels to row 1")

    def _merge_header_cells():
        """Then merge the cells for the group headings"""

        for col in range(2, _col_count+1):
            _cell = Table.Cell(1, col)   # 1st row, columns start at 2.

            if _cell.Shape.TextFrame.TextRange.Text == "":
                try:
                    _cell.Merge(Table.Cell(1, col-1))
                except:
                    pass
        Log.Info("Merged group Header Cells")

    _add_group_headers()
    _merge_header_cells()


def replace_row_labels_with_group_names(Table, Matrix=None):
    """Pre-pend every row in the table with the Group Name.

    This is typically used with making a summary table, for example displaying
    Top 2 scores from a selection of scores or tables.

    :param Table: Table shape
    :param Matrix: Matrix associated with the Table. Default is None
 
    """

    if Matrix is None:
        from globals import Matrix
    from globals import Log

    _row_count = Table.Rows.Count

    try:
        for row in range(2, _row_count+1):
            _cell = Table.Cell(row, 1)    # 1st column
            _label = Matrix.SideAxis.DataMembers[row-2].Group.Label
            _text = _cell.Shape.TextFrame.TextRange.Text
            _cell.Shape.TextFrame.TextRange.Text = _label + " - " + _text
        Log.Info("Updating row labels with group names")
    except:
        Log.Warn("replace_row_labels_with_group_names failed to run")


def _unset_bold(Table, Log):
    """unset Bold Font of group headings on refresh."""

    for row in range(2, Table.Rows.Count+1):
        _cell = Table.Cell(row, 1)  # 1st column
        _cell.Shape.TextFrame.TextRange.Font.Bold = False
    Log.Info("resetting fonts Bold = False")


def insert_rows_for_group_labels(Table, Matrix=None):
    """Add in a new row for group headings (including nested group headings)
    for rows of the table.

    The new row will be inserted at the top of each new group or nested group.

    :param Table: Table shape
    :param Matrix: Matrix associated with the Table. Default is None
    
    """

    if Matrix is None:
        from globals import Matrix
    from globals import Log

    def _which_rows_to_insert():
        """Calculate which rows need to be inserted for each outer nest"""

        _rows_for_group = dict()
        # Outer groups
        _group_text = ""
        _previous_group_text = ""

        for row in Matrix:
            try:
                _parent = row.Member.ParentMember.ParentMember.Group.Label
                _parent_grp = row.Member.ParentMember.Group.Label
                _grp = row.Member.Group.Label

                _group_text = _parent + " - " + _parent_grp + " - " + _grp
            except:
                try:
                    _parent_grp = row.Member.ParentMember.Group.Label
                    _grp = row.Member.Group.Label

                    _group_text = _parent_grp + " - " + _grp
                except:

                    _group_text = row.Member.Group.Label

            if _previous_group_text != _group_text:
                # Update dict
                _rows_for_group[row.Member.DataIndex + 1] = _group_text
                _previous_group_text = _group_text

        Log.Info("Rows to insert into table " + str(_rows_for_group))
        return _rows_for_group

    def _insert_rows_and_text():
        """Insert rows, and set the text to the nested group label"""

        keys = sorted(_rows_for_group.keys())

        for i in reversed(keys):
            # Insert row
            Table.Rows.Add(i+1)
            _cell = Table.Cell(i+1, 1)  # 1st column
            _cell.Shape.TextFrame.TextRange.Text = _rows_for_group[i]
            # make font bold for this _cell.
            _cell.Shape.TextFrame.TextRange.Font.Bold = True
        Log.Info("set text to Parent Grp Label - Grp Label or Group Label")

    _unset_bold(Table, Log)
    _rows_for_group = _which_rows_to_insert()
    _insert_rows_and_text()


def delete_table_row_before_fill():
    """Manipulate the table before it is filled.
    Delete first row so that any merged cells are removed before the fill.

    NOTE: This needs to be run from the transformations script, and is run
    before any script that will merge cells in the first row.
    
    Note, the Table object is not available from the Transformation
    script, and therefore the active object is used to find the Table.

    """

    from globals import Log
    import System
    _ppt_pap = System.Type.GetTypeFromProgID("PowerPoint.Application")
    app = System.Activator.CreateInstance(_ppt_pap)
    activeShape = app.ActiveWindow.Selection.ShapeRange[1]

    activeShape.Table.Rows[1].Delete()
    Log.Info("First Row deleted")

def indent_net_items(Table, Matrix=None):
    """Indent Net items within a table. Supported up to 1 level of net in the 
    axis
    
    :param Table: Table shape
    :param Matrix: Matrix associated with the Table. Default is None
    
    """
    
    for i in range(0, Table.Rows.Count-1):
        Table.Rows(i+2).Cells(1).Shape.TextFrame.TextRange.ParagraphFormat.Alignment = 1 #left
        if Matrix[i].Member.IndentLevel > 0:
            txt = Table.Rows(i+2).Cells(1).Shape.TextFrame.TextRange.Text
            Table.Rows(i+2).Cells(1).Shape.TextFrame.TextRange.ParagraphFormat.Alignment = 3 #right    
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
