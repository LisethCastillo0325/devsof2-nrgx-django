

def size_column_excel(writer, sheet, name):
    for column in sheet:
        column_length = max(sheet[column].astype(str).map(len).max(), len(column))
        col_idx = sheet.columns.get_loc(column)
        writer.sheets[name].set_column(col_idx, col_idx, column_length)
    return writer