# -*- coding: utf-8 -*-
# from odoo import http


# class McAulReportingAndReport(http.Controller):
#     @http.route('/mc_aul_reporting_and_report/mc_aul_reporting_and_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mc_aul_reporting_and_report/mc_aul_reporting_and_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mc_aul_reporting_and_report.listing', {
#             'root': '/mc_aul_reporting_and_report/mc_aul_reporting_and_report',
#             'objects': http.request.env['mc_aul_reporting_and_report.mc_aul_reporting_and_report'].search([]),
#         })

#     @http.route('/mc_aul_reporting_and_report/mc_aul_reporting_and_report/objects/<model("mc_aul_reporting_and_report.mc_aul_reporting_and_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mc_aul_reporting_and_report.object', {
#             'object': obj
#         })
