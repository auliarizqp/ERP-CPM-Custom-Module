# -*- coding: utf-8 -*-
# from odoo import http


# class McsAulPurchaseRfq(http.Controller):
#     @http.route('/mcs_aul_purchase_rfq/mcs_aul_purchase_rfq/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mcs_aul_purchase_rfq/mcs_aul_purchase_rfq/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mcs_aul_purchase_rfq.listing', {
#             'root': '/mcs_aul_purchase_rfq/mcs_aul_purchase_rfq',
#             'objects': http.request.env['mcs_aul_purchase_rfq.mcs_aul_purchase_rfq'].search([]),
#         })

#     @http.route('/mcs_aul_purchase_rfq/mcs_aul_purchase_rfq/objects/<model("mcs_aul_purchase_rfq.mcs_aul_purchase_rfq"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mcs_aul_purchase_rfq.object', {
#             'object': obj
#         })
