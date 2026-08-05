import xlwings as xw
from xlwings import script


@script
def hello_world(book: xw.Book):
    sheet = book.sheets.active
    cell = sheet["A1"]
    if cell.value == "Hello xlwings!":
        cell.value = "Bye xlwings!"
    else:
        cell.value = "Hello xlwings!"
