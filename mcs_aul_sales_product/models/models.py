from ast import Store
from odoo import models, fields, api
from datetime import datetime


# class ChangeRelated(models.Model):
    # _inherit = 'product.pricelist.item'
    
    # part_number = fields.Many2one(comodel_name='master.part.number', string='Part Number', related="product_tmpl_id.part_number")
    
    # @api.onchange('product_tmpl_id','part_number')
    # def _compute_product_id_and_part(self):
        # for r in self:
            # domain = [('part_number','=',r.part_number.id)]
            # onch_product = r.env['product.template'].search(domain,limit=1)
            # if r.part_number.id == False:
                # r.product_tmpl_id = False
            # elif onch_product:
                # r.product_tmpl_id = onch_product.id
    

class InheritPartN(models.Model):
    _inherit = 'master.part.number'
    
    product = fields.Char(string='Product', compute="_onchange_part_number_pro")
    
    @api.depends('product')
    def _onchange_part_number_pro(self):
        for rec in self:
            domain = [('part_number','=',rec.part_number)]
            produk = rec.env['product.product'].search(domain,limit=1)
            if produk:
                rec.product = produk.name
            else:
                rec.product = False
    

class InheritItemN(models.Model):
    _inherit = 'master.item.number'
    
    product = fields.Char(string='Product', compute="_onchange_item_number_pro")
    
    @api.depends('product')
    def _onchange_item_number_pro(self):
        for rec in self:
            domain = [('item_number','=',rec.item_number)]
            produk = rec.env['product.product'].search(domain,limit=1)
            if produk:
                rec.product = produk.name
            else:
                rec.product = False


class InheritFieldForecast(models.Model):
    _inherit = 'sale.blanket.order'
    
    order_date = fields.Datetime(string='Order Date')
    name_po_customer = fields.Char(string='Sales Forecast Customer', track_visibility=True)
    # po_customer = fields.Char(string="PO Customer", track_visibility=True, compute="_compute_name_po_customer")
    
    @api.onchange('name_po_customer','po_customer')
    def _compute_name_po_customer(self):
        for r in self:
            # if r.name_pro_customer:
            r.po_customer = r.name_po_customer


class InheritBooleanButton(models.Model):
    _inherit = 'product.template'
    
    active = fields.Boolean(string='Active', store=True, copy=True, default=False)
    
    def account_archive_enable(self):
        for r in self:
            r.active = True
            
    def account_archive_disable(self):
        for r in self:
            r.active = False

    state = fields.Selection(string='Status', selection=[('draft', 'Draft'), 
                                                         ('approved', 'Approved'), 
                                                         ('not_approved', 'Not Approved')], default="draft")
    
    def action_approved(self):
        for r in self:
            r.active = True
            r.date_approve = fields.datetime.now()
            r.write({'state':'approved'})
            
    def action_not_approved(self):
        for r in self:
            r.active = False
            r.write({'state':'not_approved'})

    date_approve = fields.Datetime(string='Approved Date', store=True)

