# -*- coding: utf-8 -*-
# from odoo import http


# class McsAulProductPricelist(http.Controller):
#     @http.route('/mcs_aul_product_pricelist/mcs_aul_product_pricelist/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mcs_aul_product_pricelist/mcs_aul_product_pricelist/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mcs_aul_product_pricelist.listing', {
#             'root': '/mcs_aul_product_pricelist/mcs_aul_product_pricelist',
#             'objects': http.request.env['mcs_aul_product_pricelist.mcs_aul_product_pricelist'].search([]),
#         })

#     @http.route('/mcs_aul_product_pricelist/mcs_aul_product_pricelist/objects/<model("mcs_aul_product_pricelist.mcs_aul_product_pricelist"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mcs_aul_product_pricelist.object', {
#             'object': obj
#         })
