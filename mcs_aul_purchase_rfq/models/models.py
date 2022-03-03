from odoo import models, fields


class PicName(models.Model):
    _name = 'contact.pic.name'
    _rec_name = 'pic_name'

    pic_name = fields.Char(string='PIC Name')
    

class InheritType(models.Model):
    _inherit = 'purchase.request'
    
    picking_id = fields.Many2one(comodel_name='stock.picking.type', string='Picking Type Id')
    

class ChangeName(models.Model):
    _inherit = 'maintenance.equipment'
    
    umur = fields.Many2one(string='Age')
    
        
class RessPartner(models.Model):
    _inherit = 'res.partner'

    contacts_id = fields.Many2one(comodel_name='contact.pic.name', string='Contact')


class InheritState(models.Model):
    _inherit = 'purchase.order'
    
    state = fields.Selection([('draft', 'RFQ'),
                              ('purchase', 'Temporary PO'),
                              ('sent', 'RFQ Sent'),
                              ('to approve', 'To Approve'),
                              ('purchase final', 'Purchase Order'),
                              ('done', 'Locked'),
                              ('cancel','Canceled')])
    
    def action_confirm_sent(self):
        for r in self:
            r.write({'state':'sent'})
    
    def action_confirm_to_approve(self):
        for r in self:
            r.write({'state':'to approve'})
    
    def action_confirm_purchase_final(self):
        for r in self:
            r.write({'state':'purchase final'})
            
    def action_confirm_purchase_order(self):
        for r in self:
            super(InheritState, self).button_confirm()
            r.write({'state':'purchase final'})

    def button_approve(self):
        for r in self:
            super(InheritState, self).button_approve()
            r.write({'state':'purchase final'})
            
    def button_confirm(self):
        for r in self:
            super(InheritState, self).button_confirm()
            r.write({'state':'purchase'})