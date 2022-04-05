from odoo import models, api, fields, _
from odoo.exceptions import UserError
from datetime import datetime


class InheritBttn(models.Model):
    _inherit = 'mrp.production'
    
    total_hasil_ok_produksi = fields.Float(string='Total hasil Ok Produksi', compute="_compute_total_hasil_ok_produksi")
    total_ng = fields.Float(string='Total NG', compute="_compute_total_ng")
    total_hasil_ok = fields.Float(string='Total Hasil Ok', compute="_compute_total_hasil_ok_produksi")
    total_hold_ok = fields.Float(string='Total Hold OK', compute="_compute_total_hasil_ok_produksi")
    total_hold_ng = fields.Float(string='Total Hold NG', compute="_compute_total_hasil_ok_produksi")
    
    total_ng_sementara = fields.Float(string='Total NG Sementara', compute="_compute_total_hasil_ok_produksi")
    
    @api.depends('total_hasil_ok_produksi',
                 'total_ng_sementara',
                 'total_hasil_ok',
                 'total_hold_ok',
                 'total_hold_ng')
    def _compute_total_hasil_ok_produksi(self):
        for r in self:
            r.total_hasil_ok_produksi = 0.0
            r.total_ng_sementara = 0.0
            r.total_hasil_ok = 0.0
            r.total_hold_ok = 0.0
            r.total_hold_ng = 0.0
            for line in r.validate_ids:
                r.total_hasil_ok_produksi += line.ok_qty_prod
                r.total_ng_sementara += line.ng_qty_prod
                r.total_hasil_ok += line.ok_qty
                r.total_hold_ok += line.hold_ok_qty
                r.total_hold_ng += line.ng_qty
                
    @api.depends('total_ng', )
    def _compute_total_ng(self):
        for r in self:
            # for p in r.workorder_ids:
            #     r.total_ng += p.total_ng
            ng = 0.0
            ng_total = 0.0
            r.total_ng = 0.0
            search_ng = r.env['mrp.workorder'].search([('production_id.name', '=', r.name), ('state', '=', 'done')])
            if search_ng:
                for p in search_ng:
                    ng += p.total_ng_time_tracking
                ng_total = r.total_ng_sementara + r.total_ng_sementara
                r.total_ng = ng_total
            else:
                r.total_ng = 0.0
    
    def check_equipment_a(self):
        for r in self:
            for line in r.equipment_ids:
                mp = self.env['mrp.production'].search([('id', '!=', r.id), ('state','=','progress')])
                if mp:  
                    equipmnt = r.env['bom.maintenance.equipment'].search([('name','=',line.name.id),('mo_id','in',[m.id for m in mp]),])
                    if equipmnt:
                        mmp = ''
                        for e in equipmnt:
                            mmp += e.name.name + '/' + e.name.serial_no + ', '
                        raise UserError('Equipment %s Already Use' %(mmp))
                    

class ChangeTime(models.Model):
    _inherit = 'mrp.routing.workcenter'
    
    time_cycle = fields.Float(string='Duration (Second)', compute="_compute_time_cycle")

    @api.depends('time_cycle')
    def _compute_time_cycle(self):
        for r in self:
            time_second = r.time_cycle_manual * 3600
            r.time_cycle = time_second
            
#==============================================================================================

class InheritTotal(models.Model):
    _inherit = 'sale.order.line'
    
    total_semua = fields.Float(string='Total', compute="_compute_total_semua")
    
    @api.depends('total_semua')
    @api.onchange('price_unit','product_uom_qty','total_semua')
    def _compute_total_semua(self):
        for r in self:
            totals = (r.price_unit * r.product_uom_qty)
            r.total_semua = totals


class DandoriMold(models.Model):
    _name = 'dandori.mold'
    _rec_name = 'name'

    name = fields.Char(string='Dandori')
    

class PersiapanProses(models.Model):
    _name = 'persiapan.proses.mold'
    _rec_name = 'name'

    name = fields.Char(string='Persiapan Proses')


class SettingKondisi(models.Model):
    _name = 'setting.kondisi.mold'
    _rec_name ='name'

    name = fields.Char(string='Setting Kondisi')


class ProblemMold(models.Model):
    _name = 'problem.mold'
    _rec_name = 'name'

    name = fields.Char(string='Problem Mold')
    
    
class ProblelmMesinMold(models.Model):
    _name = 'problem.mesin.mold'
    _rec_name = 'name'
    
    name = fields.Char(string='Problem Mesin')


class Robot(models.Model):
    _name = 'robot.mold'
    _rec_name = 'name'
    
    name = fields.Char(string='Robot')


class Cooling(models.Model):
    _name = 'cooling.mold'
    _rec_name = 'name'
    
    name = fields.Char(string='Cooling')


class Matl(models.Model):
    _name = 'matl.mold'
    _rec_name = 'name'
    
    name = fields.Char(string="Mat'l")
    

class Utility(models.Model):
    _name = 'utility.mold'
    _rec_name = 'name'
    
    name = fields.Char(string='Utility')


class WizardPersiapanMold(models.Model):
    _name = 'wizard.persiapan.mold'
    _description = 'Persiapan Mold'
    _rec_name = 'dandori_id'

    dandori_id = fields.Many2one(comodel_name='dandori.mold', string='Dandori')
    persiapan_proses_id = fields.Many2one(comodel_name='persiapan.proses.mold', string='Persiapan Proses')
    setting_kondisi_id = fields.Many2one(comodel_name='setting.kondisi.mold', string='Setting Kondisi')
    problem_id = fields.Many2one(comodel_name='problem.mold', string='Problem')
    problem_mesin_id = fields.Many2one(comodel_name='problem.mesin.mold', string='Problem Mesin')
    robot_id = fields.Many2one(comodel_name='robot.mold', string='Robot')
    cooling_id = fields.Many2one(comodel_name='cooling.mold', string='Cooling')
    matl_id = fields.Many2one(comodel_name='matl.mold', string="Mat'l")
    utility_id = fields.Many2one(comodel_name='utility.mold', string='Utility')
    note = fields.Text(string='Note')
    
    workorder_id = fields.Many2one(comodel_name='mrp.workorder', string='Workorder')
    
    # persiapan_mold_id = fields.Many2one(comodel_name='persiapan.mold', string='Persiapan Mold')
    
    # @api.onchange('note')
    def save_submit(self):
        for r in self:
            search_time_ids = r.env['mrp.workorder'].search([('id', '=', r.workorder_id.id)])
            list_data = []
            for search_tm in search_time_ids:
                if r.note != None:
                    search_tm.note = r.note
                s_time = search_tm.env['mrp.workcenter.productivity'].search([('workorder_id', '=', search_tm.id)], limit=1)
                for time_idsearch in s_time:
                    list_data.append([
                        0, 0, {
                            'start_date' : s_time.date_start,
                            'dandori_mold' : r.dandori_id.id,
                            'persiapan_proses_mold' : r.persiapan_proses_id.id,
                            'setting_kondisi_mold' : r.setting_kondisi_id.id,
                            'problem_mold' : r.problem_id.id,
                            'problem_mesin_mold' : r.problem_mesin_id.id,
                            'robot_mold' : r.robot_id.id,
                            'cooling_mold' : r.cooling_id.id,
                            'matl_mold' : r.matl_id.id,
                            'utility_mold' : r.utility_id.id,
                        }
                    ])
                search_tm.persiapan_mold_ids = list_data
                
                
                # for persipan_mold in relation.persiapan_mold_id:
                #     persipan_mold.dandori_mold = r.dandori_id.name
                #     persipan_mold.persiapan_proses_mold = r.persiapan_proses_id.name
                #     persipan_mold.setting_kondisi_mold = r.setting_kondisi_id.name
                #     persipan_mold.problem_mold = r.problem_id.name
                #     persipan_mold.problem_mesin_mold = r.problem_mesin_id.name
                #     persipan_mold.robot_mold = r.robot_id.name
                #     persipan_mold.cooling_mold = r.cooling_id.name
                #     persipan_mold.matl_mold = r.matl_id.name
                #     persipan_mold.utility_mold = r.utility_id.name
                #     persipan_mold.note = r.note
                

class InheritButtonMold(models.Model):
    _inherit = 'mrp.workorder'
    
    # dandori_mold = fields.Char(string='Dandori')
    # persiapan_proses_mold = fields.Char(string='Persiapan Proses')
    # setting_kondisi_mold = fields.Char(string='Setting Kondisi')
    # problem_mold = fields.Char(string='Problem Mold')
    # problem_mesin_mold = fields.Char(string='Problem Mesin')
    # robot_mold = fields.Char(string='Robot')
    # cooling_mold = fields.Char(string='Cooling')
    # matl_mold = fields.Char(string="Mat'l")
    # utility_mold = fields.Char(string='Utility')
    persiapan_mold_ids = fields.One2many(comodel_name='persiapan.mold', inverse_name='persiapan_mold_id', string='Persiapan Mold')
    
    equipment_id = fields.One2many(comodel_name='bom.maintenance.equipment', inverse_name='equipment_ids', string='Maintenance Equipment', compute="_compute_equipment_id")
    validate_id = fields.One2many(comodel_name='manufacture.validate', inverse_name='workorder_id', string='Manufacture Validate', compute="_compute_equipment_id")
    
    total_hasil_ok_produksi = fields.Float(string='Total hasil Ok Produksi', compute="_compute_total_hasil_ok_produksi")
    total_hasil_ok = fields.Float(string='Total Hasil Ok', compute="_compute_total_hasil_ok_produksi")
    total_hold_ok = fields.Float(string='Total Hold OK', compute="_compute_total_hasil_ok_produksi")
    total_hold_ng = fields.Float(string='Total Hold NG', compute="_compute_total_hasil_ok_produksi")
    total_ng = fields.Float(string='Total NG', compute="_compute_total_ng")
    total_ng_sementara = fields.Float(string='Total NG Sementara', compute="_compute_total_hasil_ok_produksi")
    
    total_ng_time_tracking = fields.Float(string='Sub Total NG', compute="_compute_total_ng_time_tracking")
    
    state = fields.Selection(selection_add=[('done_all', 'Done')])
    
    @api.depends('total_ng_time_tracking')
    def _compute_total_ng_time_tracking(self):
        for r in self:
            ng_total = 0.0
            ng_ng = 0.0
            ng_s_awal = 0.0
            ng_r = 0.0
            ng_r_set = 0.0
            for line in r.time_ids:
                ng_ng += line.ng_wc
                ng_s_awal += line.ng_setting_awal
                ng_r += line.ng_running
                ng_r_set += line.ng_re_setting
        ng_total = ng_ng + ng_s_awal + ng_r + ng_r_set
        self.total_ng_time_tracking = ng_total
    
    @api.depends('total_hasil_ok_produksi',
                 'total_ng_sementara',
                 'total_hasil_ok',
                 'total_hold_ok',
                 'total_hold_ng')
    def _compute_total_hasil_ok_produksi(self):
        for r in self:
            r.total_hasil_ok_produksi = 0.0
            r.total_ng_sementara = 0.0
            r.total_hasil_ok = 0.0
            r.total_hold_ok = 0.0
            r.total_hold_ng = 0.0
            for line in r.validate_id:
                r.total_hasil_ok_produksi += line.ok_qty_prod
                r.total_ng_sementara += line.ng_qty_prod
                r.total_hasil_ok += line.ok_qty
                r.total_hold_ok += line.hold_ok_qty
                r.total_hold_ng += line.ng_qty
    
    @api.depends('total_ng')
    def _compute_total_ng(self):
        self._compute_total_hasil_ok_produksi()
        self._compute_total_ng_time_tracking()
        self.total_ng = 0.0
        for r in self:
            r.total_ng = r.total_ng_sementara + r.total_ng_time_tracking
    
    @api.depends('equipment_id','validate_id','production_id')
    def _compute_equipment_id(self):
        for r in self:
            r.equipment_id = r.production_id.equipment_ids    
            r.validate_id = r.production_id.validate_ids    

    def action_persiapan_mold(self):
        for r in self:
            r.ensure_one()
            return {
                'name': 'Persiapan Mold',
                'domain': [],
                'res_model': 'wizard.persiapan.mold',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_workorder_id' : self.id},
                'target': 'new',
            }

    def do_finish(self):
        for r in self:
            r.write({'state':'done_all'})
            super(InheritButtonMold, self).do_finish()
            form_id = self.env.ref('cel_custom_cpm.manufacture_validate_form')
            ctx = {
                'default_mrp_id': r.production_id.id,
            }
            return {
                'name': 'Manufacture Validate',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'manufacture.validate',
                'view_id': form_id.id,
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': ctx
            }
        
    def action_open_manufacturing_order(self):
        for r in self:
            r.write({'state':'done_all'})
            super(InheritButtonMold, self).action_open_manufacturing_order()
            form_id = self.env.ref('cel_custom_cpm.manufacture_validate_form')
            ctx = {
                'default_mrp_id': r.production_id.id,
            }
            return {
                'name': 'Manufacture Validate',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'manufacture.validate',
                'view_id': form_id.id,
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': ctx
            }

    def change_state_fix(self):
        for r in self:
            if any(workorder.state == 'done' for workorder in self):
                r.write({'state':'done_all'})
            

class InheritEquiment(models.Model):
    _inherit = 'bom.maintenance.equipment'

    equipment_ids = fields.Many2one(comodel_name='mrp.workorder', string='Workorder')
    

class InheritValidate(models.Model):
    _inherit = 'manufacture.validate'

    workorder_id = fields.Many2one(comodel_name='mrp.workorder', string='Workorder')
    

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.onchange('partner_id','payment_term_id')
    def _onchange_payment_terms(self):
        for r in self:
            customer_id = r.env['res.partner'].search([('name','=',r.partner_id.name)], limit=1)
            if customer_id:
                r.payment_term_id = customer_id.property_payment_term_id

    @api.onchange('sales_forecast_two')
    def _onchange_sales_forecast_two(self):
        for r in self:
            domain_forecast = [('id', '=', r.sales_forecast_two.id)]
            search_forecast = r.env['sale.blanket.order'].search(domain_forecast, limit=1)
            shelter = []
            if search_forecast:
                for sale_force in search_forecast.line_ids:
                    shelter.append([
                        0, 0, {
                            'name' : r.sales_forecast_two.name,
                            'part_number' : sale_force.part_number.id,
                            'product_id' : sale_force.product_id.id,
                            'product_uom_qty' : sale_force.original_uom_qty,
                            'product_uom' : sale_force.product_uom.id,
                            'price_unit' : sale_force.price_unit,
                            'tax_id' : sale_force.taxes_id.id,
                            'total_semua' : sale_force.price_subtotal,
                        }
                    ])
                r.order_line = shelter
                
                
class MrpWorkcenterProductivity(models.Model):
    _inherit = 'mrp.workcenter.productivity'
    
    ng_wc = fields.Integer(string='NG')
    ng_setting_awal = fields.Integer(string='NG Setting Awal')
    ng_running = fields.Integer(string='NG Running')
    ng_re_setting = fields.Integer(string='NG Re Setting')
    hold_wc = fields.Integer(string='Hold')
    ng_ratio = fields.Float(string='NG Ratio')
    actual_cycle = fields.Float(string='Actual Cycle Time')
    
    @api.onchange('ng_wc','ng_setting_awal','ng_running','ng_re_setting','ng_ratio')
    def _compute_ng_ratio(self):
        self.ng_ratio = 0.0
        for r in self:
            if r.ng_wc >= 1 or r.ng_setting_awal >= 1 or r.ng_running >= 1 or r.ng_re_setting >= 1 or r.qty >= 1:
                r.ng_ratio = (((r.ng_wc + r.ng_setting_awal + r.ng_running + r.ng_re_setting) / r.qty) + (r.ng_wc + r.ng_setting_awal + r.ng_running + r.ng_re_setting)) / 10
            

class CreateModelDownTime(models.Model):
    _name = 'persiapan.mold'
    
    dandori_mold = fields.Many2one(comodel_name='dandori.mold', string='Dandori')
    persiapan_proses_mold = fields.Many2one(comodel_name='persiapan.proses.mold', string='Persiapan Proses')
    setting_kondisi_mold = fields.Many2one(comodel_name='setting.kondisi.mold', string='Setting Kondisi')
    problem_mold = fields.Many2one(comodel_name='problem.mold', string='Problem')
    problem_mesin_mold = fields.Many2one(comodel_name='problem.mesin.mold', string='Problem Mesin')
    robot_mold = fields.Many2one(comodel_name='robot.mold', string='Robot')
    cooling_mold = fields.Many2one(comodel_name='cooling.mold', string='Cooling')
    matl_mold = fields.Many2one(comodel_name='matl.mold', string="Mat'l")
    utility_mold = fields.Many2one(comodel_name='utility.mold', string='Utility')
    
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date', compute="_compute_start_and_end_date")
    
    persiapan_mold_id = fields.Many2one(comodel_name='mrp.workorder', string='Work Order')
    
    @api.depends('start_date','end_date')
    def _compute_start_and_end_date(self):
        for r in self:
            search_date = r.env['mrp.workcenter.productivity'].search([('workorder_id', '=', r.persiapan_mold_id.id), 
                                                                       ('date_start', '=', r.start_date)])
            if search_date:
                for line in search_date:
                    r.end_date = line.date_end
            else:
                r.end_date = r.end_date
