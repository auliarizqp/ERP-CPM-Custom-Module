from odoo import models, fields, api


class InheritSalesORder(models.Model):
    _inherit = 'sale.order'
    
    sales_forecast = fields.Char(string='Sales Forecast', related="blanket_order_id.name")
    

class InheritSaleBlankedOrder(models.Model):
    _inherit = 'sale.blanket.order.line'
    
    product_id = fields.Many2one(string='Part Name')

   
class InheritDepreciation(models.Model):
    _inherit = 'molding.depreciation.line'
    
    sisa_depreciation = fields.Float(string='Sisa Depreciation', compute="_compute_sisa_depreciation")
    
    @api.depends('sisa_depreciation')
    def _compute_sisa_depreciation(self):
        for a in self:
            a.sisa_depreciation = a.residual
        # self.sisa_depreciation = self.molding_id.qty_depreciation - self.depreciation
        # sisa_dep = self.sisa_depreciation
        # for a in self:
        #     sisa_dep -= self.depreciation
        #     a.sisa_depreciation = False
        #     a.depreciation = False
        #     a.sisa_depreciation = 0.0
        #     a.sisa_depreciation = a.molding_id.qty_depreciation - a.depreciation
        #     for u in a.molding_id:
        #         a.sisa_depreciation = u.qty_depreciation - a.depreciation
        #         a.sisa_depreciation -= a.depreciation
        #     return a.sisa_depreciation
                
        