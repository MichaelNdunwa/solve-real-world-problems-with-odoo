from odoo import api, fields, models, _
import base64
import io
from datetime import datetime
import openpyxl
from odoo.exceptions import UserError

class FinanceEntryImportWizard(models.TransientModel):
    _name = 'finance.entry.import.wizard'
    _description = 'Import Past Finance Records'

    upload_file = fields.Binary(string='Excel File (.xlsx)', required=True)
    filename = fields.Char()
    sheet_name = fields.Char(string="Sheet Name", required=True)
    available_sheets = fields.Text(string="Available Sheets", readonly=True)
    
    @api.onchange('upload_file')
    def _onchange_upload_file(self):
        """Update available sheets when file is uploaded"""
        if self.upload_file:
            try:
                file_content = base64.b64decode(self.upload_file)
                workbook = openpyxl.load_workbook(io.BytesIO(file_content), read_only=True)
                sheet_names = [s.strip() for s in workbook.sheetnames]
                
                # Reset sheet selection
                self.sheet_name = sheet_names[0] if sheet_names else ''
                self.available_sheets = ', '.join(sheet_names)
                
                return {
                    'warning': {
                        'title': _('Available Sheets'),
                        'message': _('Available sheets: %s') % ', '.join(sheet_names)
                    }
                }
            except Exception as e:
                self.available_sheets = ''
                self.sheet_name = ''
                raise UserError(_('Error reading Excel file: %s') % str(e))
        else:
            self.sheet_name = ''
            self.available_sheets = ''

    def _map_entry_type(self, excel_type):
        """Map Excel entry types to valid field values"""
        type_mapping = {
            'inflow': 'Inflow',
            'outflow': 'Outflow',
        }
        
        # Get the mapped value, or return the original if not found
        mapped_type = type_mapping.get(str(excel_type).strip(), str(excel_type).lower())
        
        # Validate against actual selection values
        finance_entry_model = self.env['finance.entry']
        type_field = finance_entry_model._fields.get('type')
        
        if hasattr(type_field, 'selection'):
            valid_types = [item[0] for item in type_field.selection]
            if mapped_type not in valid_types:
                for valid_type in valid_types:
                    if valid_type in mapped_type or mapped_type in valid_type:
                        return valid_type
        
        return mapped_type

    def action_import(self):
        if not self.upload_file:
            raise UserError(_("Please upload a valid Excel file."))
        
        if not self.sheet_name:
            raise UserError(_("Please enter a sheet name."))

        try:
            file_content = base64.b64decode(self.upload_file)
            workbook = openpyxl.load_workbook(io.BytesIO(file_content), read_only=True)
            
            # Check if sheet exists
            if self.sheet_name not in workbook.sheetnames:
                available_sheets = ', '.join(workbook.sheetnames)
                raise UserError(_("Sheet '%s' not found. Available sheets: %s") % (self.sheet_name, available_sheets))
            
            sheet = workbook[self.sheet_name]
            imported_count = 0
            skipped_count = 0
            
            for row_num, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                # Skip empty rows
                if not any(row):
                    continue
                
                # Ensure we have at least 4 columns (Date, Type, Description, Amount)
                if len(row) < 4:
                    skipped_count += 1
                    continue
                    
                date, entry_type, description, amount = row[:4]
                
                # Validate required fields
                if not date or not entry_type or not description or amount is None:
                    skipped_count += 1
                    continue
                
                try:
                    # Handle date conversion if needed
                    if isinstance(date, str):
                        try:
                            date = datetime.strptime(date, '%Y-%m-%d').date()
                        except ValueError:
                            try:
                                date = datetime.strptime(date, '%m/%d/%Y').date()
                            except ValueError:
                                try:
                                    date = datetime.strptime(date, '%d/%m/%Y').date()
                                except ValueError:
                                    skipped_count += 1
                                    continue
                    
                    # Map the entry type
                    mapped_type = self._map_entry_type(entry_type)
                    
                    # Convert amount to float
                    try:
                        amount_float = float(amount)
                    except (ValueError, TypeError):
                        skipped_count += 1
                        continue
                    
                    self.env['finance.entry'].create({
                        'date': date,
                        'description': str(description),
                        'amount': amount_float,
                        'type': mapped_type,
                        'user_id': self.env.uid,
                    })
                    imported_count += 1
                    
                except Exception as e:
                    skipped_count += 1
                    continue
            
            workbook.close()
            
        except Exception as e:
            raise UserError(_('Could not process the Excel file: %s') % str(e))
        
        return {'type': 'ir.actions.act_window_close'}
