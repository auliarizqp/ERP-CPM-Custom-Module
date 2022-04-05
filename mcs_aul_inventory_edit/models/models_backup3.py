from email.policy import default
from logging import warning
from pickle import TRUE
import string
from odoo import models, fields, api
from odoo.exceptions import UserError, Warning
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class AlasanStock(models.Model):
    _name = 'alasan.stock.picking'

    name = fields.Char(string='Alasan')


class WizardAlasan(models.Model):
    _name = 'wizard.alasan'

    alasan = fields.Boolean(string='Alasan')
    alasan_id = fields.Many2one(comodel_name='alasan.stock.picking', string='Keterangan Alasan', related="stock_picking_id.alasan_id")
    stock_picking_id = fields.Many2one(comodel_name='stock.picking', string='Stock Picking')

    @api.onchange('alasan_id','alasan')
    def save_submit(self):
        for r in self:
            r.stock_picking_id.alasan = r.alasan
            r.stock_picking_id.alasan_id = r.alasan_id
            r.stock_picking_id.act_picking_complete = False
            r.stock_picking_id.act_picking_validate = False
            r.stock_picking_id.state = 'assigned'
        

class MethodFieldUnloadingArea(models.Model):
    _inherit = 'stock.picking'
    
    unloading_area = fields.Char(string='Unloading Area', related="sale_id.sales_forecast")
    transfer_category = fields.Many2one(comodel_name='stock.picking.type', string='Transfer To')
    ref_id = fields.Many2one(comodel_name='stock.picking', string='Stock Picking')
    alasan_id = fields.Many2one(comodel_name='alasan.stock.picking', string='Keterangan Alasan')
    alasan = fields.Boolean(string='Alasan')
    
    user_qc = fields.Many2one(comodel_name='res.users', string='QC')
    trans_cat = fields.Selection(string='Category', selection=[('purchase', 'Purchase'), 
                                                                        ('sale', 'Sale'),
                                                                        ('raw_material', 'Raw Material'),
                                                                        ('consume', 'Consume'),
                                                                        ('produce_product', 'Produce Product'),
                                                                        ('result_product', 'Result Product'),
                                                                        ('valasi_loss', 'Valasi Loss'),
                                                                        ('transfer', 'Transfer'),
                                                                        ('raw_material_makloon', 'Raw Material Makloon'),
                                                                        ('result_makloon', 'Result Makloon'),
                                                                        ('valasi_makloon', 'Valasi Makloon')])
    
    validate_seconds = fields.Boolean(string='Validate Confirm', default=False)

    # wizard_alasan = fields.Many2one(comodel_name='wizard.alasan', string='Wizard Alasan')
    
    def button_validate(self):
        for r in self:
            search_quant = r.env['stock.quant']
            for line in r.move_ids_without_package:
                auto_form = {
                    'product_id' : line.product_id.id,
                    # 'product_tmpl_id' : create_line_id.product_tmpl_id.id,
                    'location_id' : r.picking_type_id.default_location_dest_id.id,
                    'inventory_quantity' : line.product_uom_qty + line.quantity_done,
                    'product_uom_id' : line.product_uom.id,
                    'value' : line.product_id.standard_price * (line.product_uom_qty + line.quantity_done),
                }
                create_form = search_quant.sudo().create(auto_form)
                _logger.info(auto_form)
            super(MethodFieldUnloadingArea, r).action_generate_backorder_wizard()
            return super(MethodFieldUnloadingArea, r).button_validate()
            
    def action_validate_second(self):
        for r in self:
            if r.transfer_category:
                r.validate_seconds = True
                stock_create_id = self.env['stock.picking']
                stock_create_line_id = self.env['stock.move']
                quant_create_id = self.env['stock.quant']
                # state_inv = r.state
                auto_form = {
                    'ref_id' : r.id,
                    'name' : '/',
                    # 'state' : r.state,
                    'partner_id' : r.partner_id.id,
                    'picking_type_id' : r.transfer_category.id,
                    'scheduled_date' : r.scheduled_date,
                    'delvery_date' : r.delvery_date,
                    'injection_type' : r.injection_type,
                    'shift' : r.shift,
                    'origin' : r.origin,
                    'reschedule_state' : r.reschedule_state,
                    'unloading_area' : r.unloading_area,
                    'no_sj' : r.no_sj,
                    'invoice_state' : r.invoice_state,
                    'location_id' : r.transfer_category.default_location_src_id.id,
                    'location_dest_id' : r.transfer_category.default_location_dest_id.id,
                }
                # stock_create_id.state = r.state
                create_id = stock_create_id.sudo().create(auto_form)
                # r.ref_id.state = r.state
                for line in r.move_ids_without_package:
                    line_auto_form = {
                        'picking_id' : create_id.id,
                        'part_number' : line.part_number.id,
                        'item_number' : line.item_number.id,
                        'product_id' : line.product_id.id,
                        'product_uom_qty' : line.product_uom_qty,
                        'qty_ng' : line.qty_ng,
                        'psn_ng' : line.psn_ng,
                        'quantity_done' : line.quantity_done,
                        'product_uom' : line.product_uom.id,
                        'balance' : line.balance,
                        'location_id' : r.transfer_category.default_location_src_id.id,
                        'location_dest_id' : r.transfer_category.default_location_dest_id.id,
                    }
                    create_line_id = stock_create_line_id.sudo().create(line_auto_form)
                    
                    for line_quant in line:
                        quant_auto = {
                            'product_id' : line_quant.product_id.id,
                            # 'product_tmpl_id' : create_line_id.product_tmpl_id.id,
                            'location_id' : r.transfer_category.default_location_dest_id.id,
                            'inventory_quantity' : line_quant.product_uom_qty + line_quant.quantity_done,
                            'product_uom_id' : line_quant.product_uom.id,
                            'value' : line_quant.product_id.standard_price * (line_quant.product_uom_qty + line_quant.quantity_done),
                        }
                        create_quant = quant_create_id.sudo().create(quant_auto)
                        print(quant_auto)
                    
                    
                    # search_quant_prod = line.env['product.product'].search([('id','=', line.product_id.id)])
                    # if search_quant_prod:
                    #     quant_auto = {
                    #         'stock_quant_ids' : [
                    #             (0, 0, {
                    #                 'product_id' : line.product_id.id,
                    #                 'product_tmpl_id' : create_line_id.product_tmpl_id.id,
                    #                 'location_id' : r.transfer_category.default_location_dest_id.id,
                    #                 'inventory_quantity' : line.product_uom_qty + line.quantity_done,
                    #                 'product_uom_id' : line.product_uom.id,
                    #                 'value' : line.product_id.standard_price * (line.product_uom_qty + line.quantity_done),
                    #             })
                    #         ]
                    #     }
                    #     create_quant = search_quant_prod.sudo().create(quant_auto)
                create_id.action_confirm()
                r.button_validate()
                
                if self._check_backorder():
                    return self.action_generate_backorder_wizard()
                self.action_done()
                
                r.write({'state':'done'})
                
#======================================================================================================================================

    picking_type_id_compute = fields.Char(string='Picking Type', compute="_compute_picking_type_id_compute")
    act_picking_warehouse = fields.Char(string='Warehouse', compute="_compute_picking_type_id_compute")
    
    @api.depends('picking_type_id')
    def _compute_picking_type_id_compute(self):
        for r in self:
            r.picking_type_id_compute = r.picking_type_id.warehouse_id.name + ": " + r.picking_type_id.name
            r.act_picking_warehouse = r.picking_type_id.warehouse_id.name
    
    act_picking_complete = fields.Boolean(string='Complete')
    act_picking_validate = fields.Boolean(string='Validate')

    def action_complete(self):
        for r in self:
            r.ensure_one()
            if r.state != 'done':
                raise Warning("Transaction Not Completed")
            else:
                r.act_picking_complete = True
            
    def action_validate_accounting(self):
        for r in self:
            r.ensure_one()
            if r.act_picking_complete == False :
                raise Warning("Transaction Not Completed")
            else:
                r.act_picking_validate = True
                return True
                
    def action_revisi(self):
        for r in self:
            r.ensure_one()
            return {
                'name': 'Revisi',
                'domain': [],
                'res_model': 'wizard.alasan',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_stock_picking_id' : self.id},
                'target': 'new',
            }
            


class InheritName(models.Model):
    _inherit = 'stock.move'

    name = fields.Char(string='Description', required=False)
    product_uom = fields.Many2one('uom.uom', 'Unit of Measure', required=False, domain="[('category_id', '=', product_uom_category_id)]")
    is_quantity_done_editable = fields.Boolean(string='is quantity done editable', default=True, compute="_onchange_product_id_and_part_item")
    is_initial_demand_editable = fields.Boolean(string='Is initial demand editable', default=True, compute="_onchange_product_id_and_part_item")
    
    @api.depends('is_quantity_done_editable', 'is_initial_demand_editable')
    def _onchange_product_id_and_part_item(self):
        for r in self:
            if r.product_id != None or r.item_number != None or r.part_number != None:
                r.is_quantity_done_editable = True
                r.is_initial_demand_editable = True
            else:
                r.is_quantity_done_editable = True
                r.is_initial_demand_editable = True

    @api.onchange('quantity_done')
    def _onchange_quantity_done(self):
        for r in self:
            r.product_uom_qty = r.quantity_done
