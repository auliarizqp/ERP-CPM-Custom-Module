from ast import Store
from odoo import models, fields, api
from datetime import datetime
            
            
# class InheritOrderProduction(models.Model):
#     _inherit = 'x_ks_cr.ks_so4'
    
#     konfirmasi_ppic = fields.Integer(string='Konfirmasi PPIC')
#     date_input = fields.Date(string='Tanggal Konfirmasi')
#     remarks = fields.Char(string='Remarks')

class InheritDateNow(models.Model):
    _inherit = 'stock.picking'
    
    report_date_now = fields.Date(string='Date', default=fields.Date.today)
    
    
class ItemNumberMaster(models.Model):
    _name = 'master.item.number'
    _rec_name ='item_number'
    _order = 'item_number asc'
    
    item_number = fields.Char(string='Item Code')
    
    
class PartNumberMaster(models.Model):
    _name = 'master.part.number'
    _rec_name ='part_number'
    _order = 'part_number asc'

    part_number = fields.Char(string='Part Number')
    

class InheritProduct(models.Model):
    _inherit = 'product.product'
    
    item_number = fields.Many2one(comodel_name='master.item.number', string='Item Code', related="product_tmpl_id.item_number", Store=True)
    part_number = fields.Many2one(comodel_name='master.part.number', string='Part Number', related="product_tmpl_id.part_number", Store=True)
    

class InheritChangeFields(models.Model):
    _inherit = 'product.template'
    
    item_number = fields.Many2one(comodel_name='master.item.number', string='Item Code', Store=True)
    part_number = fields.Many2one(comodel_name='master.part.number', string='Part Number', Store=True)
    
    
class InheritStoc(models.Model):
    _inherit = 'stock.move'
    
    part_number = fields.Many2one(comodel_name='master.part.number', string='Part Number', related="product_tmpl_id.part_number")
    item_number = fields.Many2one(comodel_name='master.item.number', string='Item Code', related="product_tmpl_id.item_number")
    balance = fields.Float(string='Balance', compute="_compute_product_uom_qty_and_balance")
    compute_qty = fields.Float(string='Compute Qty', compute="_compute_compute_qty")
    compute_qtyz = fields.Float(string='Compute Qty', compute="_compute_compute_qty")
    
    @api.depends('product_id')
    def _compute_compute_qty(self):
        for r in self:
            r.compute_qty = r.product_id.qty_available - r.quantity_done
            r.compute_qtyz = r.product_id.qty_available
    
    @api.depends('product_uom_qty','quantity_done','balance')
    def _compute_product_uom_qty_and_balance(self):
        for r in self:
            r.balance = r.product_uom_qty - r.quantity_done
            
    @api.onchange('product_id','item_number')
    def _compute_product_id_and_itemn(self):
        for r in self:
            domain = [('item_number','=',r.item_number.id)]
            onch_product = r.env['product.product'].search(domain, limit=1)
            if r.item_number.id == False:
                r.product_id = False
            elif onch_product:
                r.product_id = onch_product.id
                r.part_number = onch_product.part_number
                

class InheritStocLine(models.Model):
    _inherit = 'stock.move.line'
    
    part_number = fields.Many2one(comodel_name='master.part.number', string='Part Number')


class InheritMRP(models.Model):
    _inherit = 'mrp.bom.line'
    
    part_number = fields.Many2one(comodel_name='master.part.number', string='Part Number', related="product_tmpl_id.part_number")
    product_qty = fields.Float('Quantity', default=0.0, digits=(5,3), required=True)

class InheritMRA(models.Model):
    _inherit = 'maintenance.request.analisis'
    
    part_number = fields.Many2one(comodel_name='master.part.number', string='Part Number', related="product_tmpl_id.part_number")
    

class InheritMD(models.Model):
    _inherit = 'molding.depreciation'
    
    part_number = fields.Many2one(comodel_name='master.part.number', string='Part Number')


class ChangeRelation(models.Model):
    _inherit = 'purchase.request.line'

    item_number = fields.Many2one(comodel_name='master.item.number', string='Item Code')
    part_number = fields.Many2one(comodel_name='master.part.number', string='Part Number')
    
    @api.onchange('product_id','item_number')
    def _compute_product_id_and_item(self):
        for r in self:
            domain = [('item_number','=',r.item_number.id)]
            onch_product = r.env['product.product'].search(domain)
            if r.item_number.id == False:
                r.product_id = False
            elif onch_product:
                r.product_id = onch_product.id


class ChangeRelation(models.Model):
    _inherit = 'purchase.order.line'
    
    item_number = fields.Many2one(comodel_name='master.item.number', string='Item Code', store=True, related="product_id.item_number")
    balance = fields.Float(string='Balance', compute="_compute_product_qty_and_balance")
    
    @api.depends('product_qty','qty_received','balance')
    def _compute_product_qty_and_balance(self):
        for r in self:
            r.balance = r.product_qty - r.qty_received
            
    @api.onchange('product_id','item_number')
    def _compute_product_id_and_item(self):
        for r in self:
            domain = [('item_number','=',r.item_number.id)]
            onch_product = r.env['product.product'].search(domain,limit=1)
            if r.item_number.id == False:
                r.product_id = False
            elif onch_product:
                r.product_id = onch_product.id


class InheritPartNumberSaleBOL(models.Model):
    _inherit = 'sale.blanket.order.line'
    
    part_number = fields.Many2one(comodel_name='master.part.number', string='Part Number', related="product_id.item_number")
    
    @api.onchange('product_id','part_number')
    def _compute_product_id_and_part(self):
        for r in self:
            domain = [('part_number','=',r.part_number.id)]
            onch_product = r.env['product.product'].search(domain,limit=1)
            if r.part_number.id == False:
                r.product_id = False
            elif onch_product:
                r.product_id = onch_product.id


class InheritPartNumbeSaleOLr(models.Model):
    _inherit = 'sale.order.line'
    
    part_number = fields.Many2one(comodel_name='master.part.number', string='Part Number')
    
    @api.onchange('product_id','part_number')
    def _compute_product_id_and_part(self):
        for r in self:
            domain = [('part_number','=',r.part_number.id)]
            onch_product = r.env['product.product'].search(domain,limit=1)
            if r.part_number.id == False:
                r.product_id = False
            elif onch_product:
                r.product_id = onch_product.id

