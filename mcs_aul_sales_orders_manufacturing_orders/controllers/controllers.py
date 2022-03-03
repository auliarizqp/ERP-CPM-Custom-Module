# -*- coding: utf-8 -*-
# from odoo import http


# class McsAulSalesOrdersManufacturingOrders(http.Controller):
#     @http.route('/mcs_aul_sales_orders_manufacturing_orders/mcs_aul_sales_orders_manufacturing_orders/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mcs_aul_sales_orders_manufacturing_orders/mcs_aul_sales_orders_manufacturing_orders/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mcs_aul_sales_orders_manufacturing_orders.listing', {
#             'root': '/mcs_aul_sales_orders_manufacturing_orders/mcs_aul_sales_orders_manufacturing_orders',
#             'objects': http.request.env['mcs_aul_sales_orders_manufacturing_orders.mcs_aul_sales_orders_manufacturing_orders'].search([]),
#         })

#     @http.route('/mcs_aul_sales_orders_manufacturing_orders/mcs_aul_sales_orders_manufacturing_orders/objects/<model("mcs_aul_sales_orders_manufacturing_orders.mcs_aul_sales_orders_manufacturing_orders"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mcs_aul_sales_orders_manufacturing_orders.object', {
#             'object': obj
#         })
