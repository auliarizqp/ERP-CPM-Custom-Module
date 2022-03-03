# -*- coding: utf-8 -*-
{
    'name': "mcs_aul_sales_product",

    'summary': """
        Product""",

    'description': """
        Product
    """,

    'author': "Aul",
    'website': "http://www.cpm.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Product',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale_blanket_order','mc_aul_reporting_and_report'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/product_approval.xml',
        'views/product_approval_sales.xml',
        'views/templates.xml',
    ],
}
