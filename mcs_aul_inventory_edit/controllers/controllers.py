# -*- coding: utf-8 -*-
# from odoo import http


# class McsAulInventoryEdit(http.Controller):
#     @http.route('/mcs_aul_inventory_edit/mcs_aul_inventory_edit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mcs_aul_inventory_edit/mcs_aul_inventory_edit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mcs_aul_inventory_edit.listing', {
#             'root': '/mcs_aul_inventory_edit/mcs_aul_inventory_edit',
#             'objects': http.request.env['mcs_aul_inventory_edit.mcs_aul_inventory_edit'].search([]),
#         })

#     @http.route('/mcs_aul_inventory_edit/mcs_aul_inventory_edit/objects/<model("mcs_aul_inventory_edit.mcs_aul_inventory_edit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mcs_aul_inventory_edit.object', {
#             'object': obj
#         })
