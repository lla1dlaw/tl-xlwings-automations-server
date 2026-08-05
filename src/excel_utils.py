import xlwings as xw

from models import EstimateDTO, LineItemDTO
from qb_utils import QBHandler


class ExcelHandler:
    def __init__(self, qb_handler: QBHandler):
        self.qb_handler: QBHandler = qb_handler

    def push_estimate_from_excel(self, book: xw.Book):
        # 1. Metadata: Get the sheet where the user triggered the script
        sheet = book.sheets.active
        
        # 2. Read Single Fields via Named Ranges
        # This works even if the user moves the cell to another column
        cust_id = sheet.range("Estimate_CustomerID").value
        
        if not cust_id:
            # Handle validation cleanly before hitting the QB API
            sheet.range("Status_Message").value = "Error: Customer ID is required."
            return

        # 3. Read Dynamic Arrays via Excel Tables
        # This gets just the data (no headers) and sizes perfectly to the active rows
        table = sheet.tables["EstimateLineItems"]
        
        # Always force ndim=2 so a single-row table doesn't return a flat list

        raw_lines = table.data_body_range.options(ndim=2).value
        
        # 4. Pack data into the DTO
        dto_lines = []
        for row in raw_lines:
            # Assuming Table Columns: [Item ID, Quantity, Unit Price]
            item_id = row[0]
            if item_id:  # Skip completely empty rows
                dto_lines.append(
                    LineItemDTO(
                        item_id=str(int(item_id)), 
                        quantity=float(row[1] or 0), 
                        unit_price=float(row[2] or 0)
                    )
                )
                
        estimate_dto = EstimateDTO(customer_id=str(int(cust_id)), lines=dto_lines)
        
        # 5. Hand off to QBHandler
        try:
            new_estimate_id = self.qb_handler.create_estimate(estimate_dto)
            
            # Write success back to a designated Named Range
            sheet.range("Status_Message").value = f"Success! Est ID: {new_estimate_id}"
        except Exception as e:
            sheet.range("Status_Message").value = f"QuickBooks API Error: {str(e)}"
