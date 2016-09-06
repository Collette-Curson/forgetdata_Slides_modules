
def BaseSummaryToSeriesHeadings():
    from globals import *
    
    # summarize the base scores from the first column in to the row headings
    for row in Matrix:
        row.Member.Label = row.Member.Label  + " (n="+row[0][0].Value+")"
    Matrix.DeleteColumn(0)

def BaseSummaryToCategoryHeadings():
    from globals import *
    for column in Matrix.TopAxis.DataMembers:
        column.Label = column.Label + " (n=" + Matrix[0][column][0].Value + ")"
    Matrix.DeleteRow(0)

def BaseSummaryToTableRows():
    from globals import *    
    # summarize the base scores from the first column into the headings in a table, replacing existing headings
    for row in Matrix:
        row.Member.Label = "(n="+row[0][0].Value+")"
