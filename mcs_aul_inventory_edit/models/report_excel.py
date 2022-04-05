from odoo import models, fields
from datetime import datetime

class ReportDeliveryOrder(models.AbstractModel):
    _name = 'report.mcs_aul_inventory_edit.rdoseid'
    _inherit = 'report.report_xlsx.abstract'
    
    # print_date = fields.Datetime(default=fields.Datetime.now)
    
    def generate_xlsx_report(self, workbook, data, partners):
        format1 = workbook.add_format({'font_size' : 14, 'align' : 'center', 'left': 1, 'bottom':1, 'right':1, 'top':1})
        format2 = workbook.add_format({'font_size' : 14, 'align' : 'center'})
        format3 = workbook.add_format({'font_size' : 12, 'align' : 'center'})
        date_style = workbook.add_format({'text_wrap': True, 'num_format': 'dd-mm-yyyy', 'font_size' : 12, 'align' : 'center'})
        date_style1 = workbook.add_format({'num_format': 'dd-mm-yyyy', 'font_size' : 14, 'align' : 'center', 'left': 1, 'bottom':1, 'right':1, 'top':1})
        sheet = workbook.add_worksheet('Delivery Order Status')
        
        sheet.set_column('A:A', 20)
        sheet.set_column('B:E', 30)
        sheet.set_column('F:G', 5)
        
        sheet.merge_range('A1:G1', 'Delivery Order Status', format2)
        
        self.print_date = fields.Date.today()
        sheet.write(1, 0, 'Tanggal', format3)
        sheet.write(1, 1, self.print_date, date_style)
        
        sheet.write(2, 0, 'Nomor', format1)
        sheet.write(2, 1, 'Customer', format1)
        sheet.write(2, 2, 'No PO', format1)
        sheet.write(2, 3, 'No DN', format1)
        sheet.write(2, 4, 'Tanggal', format1)
        sheet.write(2, 5, 'FG', format1)
        sheet.write(2, 6, 'ACC', format1)
        
        row = 3
        
        for r in partners:
            sheet.write(row, 0, r.name, format1)
            sheet.write(row, 1, r.partner_id.name, format1)
            sheet.write(row, 2, r.po_customer, format1)
            sheet.write(row, 3, r.origin, format1)
            sheet.write(row, 4, r.delvery_date, date_style1)
            sheet.write(row, 5, '', format1)
            sheet.write(row, 6, '', format1)
            
            row += 1
        
