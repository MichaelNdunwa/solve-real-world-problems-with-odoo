from odoo import models, fields, _
import base64
import io
from datetime import datetime
import openpyxl

class FinanceEntryImportWizard(models.TransientModel):
    _name = 'finance.entry.import.wizard'
    _description = 'Import Past Finance Records'

    upload_file = fields.Binary(string='Excel File (.xlsx)', required=True)
    filename = fields.Char()

    def action_import(self):
        if not self.upload_file:
            raise UserError(_("Please upload a valid Excel file."))

        file_content = base64.b64decode(self.upload_file)
        workbook = openpyxl.load_workbook(io.BytesIO(file_content))
        sheet = workbook.active
    
        for i, row in enumerate(sheet.iter_rows(min_row=2), start=2): # skip headers
            date_cell, type_cell, desc_cell, amount_cell = row[:4]

            date_val = date_cell.value or fields.Date.today()
            type_val = (type_cell.value or '').strip().lower()
            description = str(desc_cell.value or '').strip()
            amount = float(amount_cell.value or 0)

            if type_val not in ['inflow', 'outflow']:
                continue # skip invalid rows
            
            self.env['finance.entry'].create({
                'date' : date_val,
                'type' : type_val,
                'description' : description,
                'amount' : amount,
                'user_id' : self.env.uid,
            })
            