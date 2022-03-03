from ast import literal_eval
from copy import copy
from datetime import date
from itertools import groupby
from operator import attrgetter, itemgetter
from collections import defaultdict
import time

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import UserError
from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES


class InheritProdukPricelist(models.Model):
    _inherit = 'product.pricelist'
    
    customers = fields.Many2one(comodel_name='res.partner', string='Customers')
    
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    

class InheritDate(models.Model):
    _inherit = 'purchase.order'

    date_approve = fields.Date(string='Confirmation Date')

class ChangeNameDate(models.Model):
    _inherit = 'stock.picking'

    delvery_date = fields.Many2one(string='Received Date')
    
    # @api.model
    # def write(self, vals):
    #     if vals.get('picking_type_id') and self.state != 'draft':
    #         raise UserError(_("Changing the operation type of this record is forbidden at this point."))
        
    #     if vals.get('partner_id'):
    #         for picking in self:
    #             if picking.location_id.usage == 'supplier' or picking.location_dest_id.usage == 'customer':
    #                 if picking.partner_id:
    #                     picking.message_unsubscribe(picking.partner_id.ids)
    #                 picking.message_subscribe([vals.get('partner_id')])
    #     res = super(ChangeNameDate, self).write(vals)
        
    #     after_vals = {}
    #     if vals.get('location_id'):
    #         after_vals['location_id'] = vals['location_id']
    #     if vals.get('location_dest_id'):
    #         after_vals['location_dest_id'] = vals['location_dest_id']
    #     if after_vals:
    #         self.mapped('move_lines').filtered(lambda move: not move.scrapped).write(after_vals)
    #     if vals.get('move_lines'):
    #         # Do not run autoconfirm if any of the moves has an initial demand. If an initial demand
    #         # is present in any of the moves, it means the picking was created through the "planned
    #         # transfer" mechanism.
    #         pickings_to_not_autoconfirm = self.env['stock.picking']
    #         for picking in self:
    #             if picking.state != 'draft':
    #                 continue
    #             for move in picking.move_lines:
    #                 if not float_is_zero(move.product_uom_qty, precision_rounding=move.product_uom.rounding):
    #                     pickings_to_not_autoconfirm |= picking
    #                     break
    #         (self - pickings_to_not_autoconfirm)._autoconfirm_picking()
    #     return res
    
class ChangeRelated(models.Model):
    _inherit = 'product.pricelist.item'
    
    product_tmpl_id = fields.Many2one(comodel_name='product.template', string='Product', store=True, copy=True, compute="_compute_product_id_and_part")
    part_number = fields.Many2one(comodel_name='master.part.number', string='Part Number', related="product_tmpl_id.part_number")    
    applied_on = fields.Selection([
        ('3_global', 'All Products'),
        ('2_product_category', 'Product Category'),
        ('1_product', 'Product'),
        ('0_product_variant', 'Product Variant')], "Apply On",
        default='0_product_variant',
        help='Pricelist Item applicable on selected option')
    
    @api.depends('product_tmpl_id','part_number')
    def _compute_product_id_and_part(self):
        for r in self:
            domain = [('part_number','=',r.part_number.id)]
            onch_product = r.env['product.template'].search(domain)
            if r.part_number.id == False:
                r.product_tmpl_id = False
            elif onch_product:
                r.product_tmpl_id = onch_product.id
    