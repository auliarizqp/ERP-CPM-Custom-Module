# -*- coding: utf-8 -*-
# from odoo import http


# class McsInheritSalesOrder(http.Controller):
#     @http.route('/mcs_inherit_sales_order/mcs_inherit_sales_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mcs_inherit_sales_order/mcs_inherit_sales_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mcs_inherit_sales_order.listing', {
#             'root': '/mcs_inherit_sales_order/mcs_inherit_sales_order',
#             'objects': http.request.env['mcs_inherit_sales_order.mcs_inherit_sales_order'].search([]),
#         })

#     @http.route('/mcs_inherit_sales_order/mcs_inherit_sales_order/objects/<model("mcs_inherit_sales_order.mcs_inherit_sales_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mcs_inherit_sales_order.object', {
#             'object': obj
#         })
