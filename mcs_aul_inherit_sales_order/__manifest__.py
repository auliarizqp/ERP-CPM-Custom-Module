# -*- coding: utf-8 -*-
{
    'name': "mcs_aul_inherit_sales_order",

    'summary': """
        Sales Orders""",

    'description': """
        Install after module mcs_aul_cpm_add_and_remove
    """,

    'author': "Aul",
    'website': "http://www.cpm.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','mcs_aul_cpm_add_and_remove','purchase','product','stock','setu_inventory_ledger_report'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
}
