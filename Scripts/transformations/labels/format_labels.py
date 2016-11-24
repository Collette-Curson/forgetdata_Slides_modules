class FormatSettings:
    """This class is used by a filler whilst outputting text into a chart
    * the default implementation will a basic str.format approach
    * more complex implementation should override the formatter function.
    
    For example, the label_format will expect a matrix, member, or group.
    The cell_format will expect a Cell.
     
    The label_format string can contain whatever the matrix/group/member/cell
    can format,  for example  label_format = "{0.Group}: {0}"
    
    The cell_format string can contain whatever the cell can format, eg
    cell_format = "${0[0].Value} XXX"
    
    Examples:
    
    | import transformations.utils.utilities as utils
    | m = utils.matrixfuncs.create_test_matrix()
    | from transformations.labels.format_labels import FormatSettings
    | settings = FormatSettings(label_format="{0.Member.Label}: " + "{0[0][0].Value}")
    | print ", ".join([settings.label_format(r) for r in m])
    | myRow 0, myRow 1, myRow 2, myRow 3, myRow 4
    
    """
    
    def __init__(self, label_format = "{0}", cell_format="{0}"):
        if isinstance(label_format, str):
            self.label_format = label_format.format
        elif callable(label_format):
            self.label_format = label_format
        if isinstance(cell_format, str):
            self.cell_format = cell_format.format
        elif callable(cell_format):
            self.cell_format = cell_format 