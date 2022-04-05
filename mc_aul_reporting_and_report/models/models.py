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
    remarks = fields.Text(string='Remarks')
    injection_reason = fields.Many2one(comodel_name='injection.reason', string='Alasan Injection')
    nd_injection_reason = fields.Many2one(comodel_name='nd.process.reason', string='Alasan 2nd Injection')
    
    picking_type_id_compute = fields.Char(string='Picking Type Id Compute', default="PRODUKSI: Internal Transfers Produksi", compute="_compute_picking_type_id_compute")


    @api.depends('picking_type_id_compute')
    def _compute_picking_type_id_compute(self):
        for r in self:
            if r.picking_type_id != False:
                # r.picking_type_id_compute = r.picking_type_id.warehouse_id.name + ": " + r.picking_type_id.name
                r.picking_type_id_compute = False
    
    @api.depends('product_id','quantity_done')
    def _compute_compute_qty(self):
        for r in self: 
            r.compute_qty = r.product_id.qty_available - r.quantity_done
            r.compute_qtyz = r.product_id.qty_available
    
    @api.depends('product_uom_qty','quantity_done','balance')
    def _compute_product_uom_qty_and_balance(self):
        for r in self:
            r.balance = r.product_uom_qty - r.quantity_done
            
    @api.onchange('product_id','item_number','part_number')
    def _compute_product_id_and_itemn(self):
        for r in self:
            domain_prod = [('name', '=', r.product_id.name)]
            domain_item = [('item_number','=',r.item_number.id)]
            domain_part = [('part_number', '=', r.part_number.id)]
            product_change = r.env['product.product'].search(domain_prod, limit=1)
            item_number_change = r.env['product.product'].search(domain_item, limit=1)
            part_number_change = r.env['product.product'].search(domain_part, limit=1)
            if r.item_number.id == False and r.part_number.id == False:
                if product_change:
                    r.part_number = product_change.part_number.id
                    r.item_number = product_change.item_number.id
            elif r.part_number.id == False and r.product_id.id == False:
                if item_number_change:
                    r.part_number = item_number_change.part_number.id
                    r.product_id = item_number_change.id
            elif r.item_number.id == False and r.product_id.id == False:
                if part_number_change:
                    r.product_id = part_number_change.id
                    r.item_number = part_number_change.item_number.id
            elif product_change:
                r.part_number = product_change.part_number.id
                r.item_number = product_change.item_number.id
            elif item_number_change:
                r.part_number = item_number_change.part_number.id
                r.product_id = item_number_change.id
            elif part_number_change:
                r.product_id = part_number_change.id
                r.item_number = part_number_change.item_number.id

            # domain = [('item_number','=',r.item_number.id)]
            # onch_product = r.env['product.product'].search(domain, limit=1)
            # if r.item_number.id == False:
                # r.product_id = False
            # elif onch_product:
                # r.product_id = onch_product.id
                # r.part_number = onch_product.part_number


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

    item_number = fields.Many2one(comodel_name='master.item.number', string='Item Code', related="product_id.item_number")
    part_number = fields.Many2one(comodel_name='master.part.number', string='Part Number', related="product_id.part_number")
    
    @api.onchange('product_id','item_number')
    def _compute_product_id_and_item(self):
        for r in self:
            domain = [('item_number','=',r.item_number.id)]
            onch_product = r.env['product.product'].search(domain,limit=1)
            if r.item_number.id == False:
                r.product_id = False
            elif onch_product:
                r.product_id = onch_product.id


class ChangeRelation(models.Model):
    _inherit = 'purchase.order.line'
    
    item_number = fields.Many2one(comodel_name='master.item.number', string='Item Code', related="product_id.item_number")
    balance = fields.Float(string='Balance', compute="_compute_product_qty_and_balance")
    
    @api.depends('product_qty','qty_received','balance')
    def _compute_product_qty_and_balance(self):
        for r in self:
            r.balance = r.product_qty - r.qty_received
            
    @api.onchange('product_id','item_number')
    def _compute_product_id_and_item(self):
        for r in self:
            domain = [('item_number','=',r.item_number.id)]
            domain1 = [('name', '=', r.product_id.name)]
            onch_product = r.env['product.product'].search(domain,limit=1)
            product_change = r.env['product.product'].search(domain1, limit=1)
            if r.item_number.id == False:
                if product_change:
                    r.item_number = product_change.item_number.id
            elif onch_product:
                r.product_id = onch_product.id


class InheritPartNumberSaleBOL(models.Model):
    _inherit = 'sale.blanket.order.line'
    
    part_number = fields.Many2one(comodel_name='master.part.number', string='Part Number', related='product_id.part_number')
    
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
    
    part_number = fields.Many2one(comodel_name='master.part.number', string='Part Number', related="product_id.part_number")
    
    @api.onchange('product_id','part_number')
    def _compute_product_id_and_part(self):
        for r in self:
            domain = [('part_number','=',r.part_number.id)]
            onch_product = r.env['product.product'].search(domain)
            if r.part_number.id == False:
                r.product_id = False
            elif onch_product:
                r.product_id = onch_product.id


class InheritAccount(models.Model):
    _inherit = 'account.bank.statement'
    
    @api.onchange('balance_end')
    def _onchange_balance_end(self):
        for r in self:
            r.balance_end_real = r.balance_end
            

class AddFunchInvoiceLine(models.Model):
    _inherit = 'account.move'
    
    @api.onchange('ref')
    def _onchange_ref(self):
        for r in self:
            if r.ref != False:
                r.name = r.ref
    
    @api.onchange('picking_ids')
    def _onchange_picking_ids(self):
        for r in self:
            r.invoice_line_ids = None
            r.line_ids = None
            if r.picking_ids:
                list_data = []
                list_inv = []
                list_inv2 = []
                for line_picking in r.picking_ids:
                    search_picking = r.env['stock.picking'].search([('name', '=', line_picking.name)])
                    print(search_picking)
                    if search_picking:
                        for product_list in search_picking.move_ids_without_package:
                            list_data.append([
                                0, 0, {
                                    'product_id' : product_list.product_id.id,
                                    'account_id' : product_list.product_id.property_account_income_id or product_list.product_id.categ_id.property_account_income_categ_id.id,
                                    'quantity' : product_list.balance,
                                    'product_uom_id' : product_list.product_uom,
                                    'name' : product_list.product_id.name,
                                    'price_unit' : product_list.product_id.lst_price,
                                    'tax_ids' : product_list.product_id.taxes_id,
                                    'price_subtotal' : product_list.balance * product_list.product_id.lst_price,
                                    'credit' : product_list.balance * product_list.product_id.lst_price,
                                }
                            ])
                        list_inv.append([
                            0, 0, {
                                'account_id' : search_picking.move_ids_without_package.product_id.taxes_id.invoice_repartition_line_ids.account_id.id,
                                'name' : search_picking.move_ids_without_package.product_id.taxes_id.name,
                                'debit' : 1 if r.journal_id.name == "Vendor Bills" else 0,
                                'credit' : 1 if r.journal_id.name == "Customer Invoices" else 0,
                            }
                        ])
                        list_inv2.append([
                            0, 0, {
                                'account_id' : r.partner_id.property_account_receivable_id.id if r.journal_id.name == "Customer Invoices" else r.partner_id.property_account_payable_id.id,
                                'name' : '',
                                'debit' : r.amount_untaxed if r.journal_id.name == "Customer Invoices" else - r.amount_untaxed,
                                'credit' : 0,
                            }
                        ])
                r.line_ids = list_inv 
                r.line_ids = list_inv2
                r.invoice_line_ids = list_data
                print(r.invoice_line_ids)
                # if r.invoice_line_ids != None:
                #     for line_pickings in r.picking_ids:
                #         search_pickings = r.env['stock.picking'].search([('name', '=', line_pickings.name)])
                #         print(search_pickings)
                #         if search_pickings:
                #             list_inv.append([
                #                 0, 0, {
                #                     'account_id' : search_pickings.move_ids_without_package.product_id.taxes_id.invoice_repartition_line_ids.account_id.id,
                #                     'name' : search_pickings.move_ids_without_package.product_id.taxes_id.name,
                #                     'debit' : 1 if r.journal_id.name == "Vendor Bills" else 0,
                #                     'credit' : 1 if r.journal_id.name == "Customer Invoices" else 0,
                #                 }
                #             ])
                #             list_inv2.append([
                #                 0, 0, {
                #                     'account_id' : r.partner_id.property_account_receivable_id.id if r.journal_id.name == "Customer Invoices" else r.partner_id.property_account_payable_id.id,
                #                     'name' : '',
                #                     'debit' : r.amount_untaxed if r.journal_id.name == "Customer Invoices" else - r.amount_untaxed,
                #                     'credit' : 0,
                #                 }
                #             ])
                #     print(r.invoice_line_ids)
                    # r.line_ids = list_inv 
                    # r.line_ids = list_inv2
                #     r.invoice_line_ids = list_data
                #     print(r.invoice_line_ids)
    # @api.onchange('invoice_line_ids')
    # def _onchange_invoice_line_ids_change(self):
    #     for r in self:
    #         list_inv = []
    #         list_inv2 = []
    #         if r.invoice_line_ids != None:
    #             for line_pickings in r.picking_ids:
    #                 search_pickings = r.env['stock.picking'].search([('name', '=', line_pickings.name)])
    #                 print(search_pickings)
    #                 if search_pickings:
    #                     list_inv.append([
    #                         0, 0, {
    #                             'account_id' : search_pickings.move_ids_without_package.product_id.taxes_id.invoice_repartition_line_ids.account_id.id,
    #                             'name' : search_pickings.move_ids_without_package.product_id.taxes_id.name,
    #                             'debit' : 1 if r.journal_id.name == "Vendor Bills" else 0,
    #                             'credit' : 1 if r.journal_id.name == "Customer Invoices" else 0,
    #                         }
    #                     ])
    #                     list_inv2.append([
    #                         0, 0, {
    #                             'account_id' : r.partner_id.property_account_receivable_id.id if r.journal_id.name == "Customer Invoices" else r.partner_id.property_account_payable_id.id,
    #                             'name' : '',
    #                             'debit' : r.amount_untaxed if r.journal_id.name == "Customer Invoices" else - r.amount_untaxed,
    #                             'credit' : 0,
    #                         }
    #                     ])
    #             print(r.invoice_line_ids)
    #             r.line_ids = list_inv 
                # r.line_ids = list_inv2