from email.policy import default
from logging import warning
from pickle import TRUE
import string
from odoo import models, fields, api
from odoo.exceptions import UserError, Warning


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
        

class MethodFieldUnloadingArea(models.Model):
    _inherit = 'stock.picking'
    
    unloading_area = fields.Char(string='Unloading Area', related="sale_id.sales_forecast")
    transfer_category = fields.Many2one(comodel_name='stock.picking.type', string='Transfer To Category')
    ref_id = fields.Many2one(comodel_name='stock.picking', string='Stock Picking')
    alasan_id = fields.Many2one(comodel_name='alasan.stock.picking', string='Keterangan Alasan')
    alasan = fields.Boolean(string='Alasan')
    
    # wizard_alasan = fields.Many2one(comodel_name='wizard.alasan', string='Wizard Alasan')
    
    # @api.onchange('alasan_id','alasan')
    # def onch_alasan(self):
    #     for r in self:
    #         r.wizard_alasan.alasan = r.alasan
    #         r.wizard_alasan.alasan_id = r.alasan_id
            
    def action_validate_second(self):
        for r in self:
            if r.transfer_category:
                stock_create_id = self.env['stock.picking']
                stock_create_line_id = self.env['stock.move']
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
                    'location_id' : r.location_id.id,
                    'location_dest_id' : r.location_dest_id.id,
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
                        'location_id' : r.location_id.id,
                        'location_dest_id' : r.location_dest_id.id,
                    }
                    create_line_id = stock_create_line_id.sudo().create(line_auto_form)
                create_id.action_confirm()
                
                if self._check_backorder():
                    return self.action_generate_backorder_wizard()
                self.action_done()
                
                r.write({'state':'done'})
                
#======================================================================================================================================

    picking_type_id_compute = fields.Char(string='Picking Type', compute="_compute_picking_type_id_compute")
    
    @api.depends('picking_type_id')
    def _compute_picking_type_id_compute(self):
        for r in self:
            r.picking_type_id_compute = r.picking_type_id.warehouse_id.name + ": " + r.picking_type_id.name
    
    act_picking_complete = fields.Boolean(string='Complete')
    act_picking_validate = fields.Boolean(string='Validate')

    def action_complete(self):
        for r in self:
            r.ensure_one()
            r.act_picking_complete = True
            
    def action_validate_accounting(self):
        for r in self:
            r.ensure_one()
            if r.act_picking_complete == False :
                raise Warning("Transaksi Belum Selesai")
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
    # is_quantity_done_editable = fields.Boolean(string='is quantity done editable', default=True)
    
