# -*- coding: utf-8 -*-
# from odoo import http


# class McsAulSalesProduct(http.Controller):
#     @http.route('/mcs_aul_sales_product/mcs_aul_sales_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mcs_aul_sales_product/mcs_aul_sales_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mcs_aul_sales_product.listing', {
#             'root': '/mcs_aul_sales_product/mcs_aul_sales_product',
#             'objects': http.request.env['mcs_aul_sales_product.mcs_aul_sales_product'].search([]),
#         })

#     @http.route('/mcs_aul_sales_product/mcs_aul_sales_product/objects/<model("mcs_aul_sales_product.mcs_aul_sales_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mcs_aul_sales_product.object', {
#             'object': obj
#         })
