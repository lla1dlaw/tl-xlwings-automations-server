import excel_utils
import xlwings as xw
from xlwings import script
from src.excel_utils import ExcelHandler
from src.qb_utils import QBHandler


@script(name="Create QB Estimate")
def create_estimate(book: xw.Book):
    qbhandler = QBHandler()
    xlhandler = ExcelHandler(qb_handler=qbhandler)
    xlhandler.push_estimate_from_excel(book)

@script
def hello_world(book: xw.Book):
    sheet = book.sheets.active
    cell = sheet["A1"]
    if cell.value == "Hello xlwings!":
        cell.value = "Bye xlwings!"
    else:
        cell.value = "Hello xlwings!"
