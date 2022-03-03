# -*- coding: utf-8 -*-
{
    'name': "mcs_aul_inventory_edit",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Aul",
    'website': "http://www.cpm.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','dn_inventory_cpm','sale_blanket_order','dn_sales_cpm','invoice_from_picking'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/wizard_alasan.xml',
        'views/views.xml',
        'views/delivery_order_status.xml',
    ],
}
