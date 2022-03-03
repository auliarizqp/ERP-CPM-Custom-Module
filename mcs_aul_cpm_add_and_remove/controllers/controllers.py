# -*- coding: utf-8 -*-
# from odoo import http


# class McsAulCpmAddAndRemove(http.Controller):
#     @http.route('/mcs_aul_cpm_add_and_remove/mcs_aul_cpm_add_and_remove/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mcs_aul_cpm_add_and_remove/mcs_aul_cpm_add_and_remove/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mcs_aul_cpm_add_and_remove.listing', {
#             'root': '/mcs_aul_cpm_add_and_remove/mcs_aul_cpm_add_and_remove',
#             'objects': http.request.env['mcs_aul_cpm_add_and_remove.mcs_aul_cpm_add_and_remove'].search([]),
#         })

#     @http.route('/mcs_aul_cpm_add_and_remove/mcs_aul_cpm_add_and_remove/objects/<model("mcs_aul_cpm_add_and_remove.mcs_aul_cpm_add_and_remove"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mcs_aul_cpm_add_and_remove.object', {
#             'object': obj
#         })
