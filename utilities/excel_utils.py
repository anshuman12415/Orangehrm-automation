import openpyxl


def get_data(file_path, sheet_name="Sheet1"):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb[sheet_name]
    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        username = str(row[0]).strip()
        password = str(row[1]).strip() if row[1] is not None else ""
        expected = str(row[2]).strip().lower(
        ) if row[2] is not None else "failure"
        data.append((username, password, expected))
    return data
