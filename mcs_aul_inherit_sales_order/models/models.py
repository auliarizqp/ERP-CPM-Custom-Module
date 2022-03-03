from odoo import models, fields


class InheritAfterSF(models.Model):
    _inherit = 'sale.order'
    
    partner_shipping_id = fields.Many2one(comodel_name='res.partner', string='Delivery Address')
    partner_invoice_id = fields.Many2one(comodel_name='res.partner', string='Invoice Address')


class ChnageTypeData(models.Model):
    _inherit = 'stock.picking'
    
    scheduled_date = fields.Date(string='Scheduled Date', default=fields.Date.today())