# -*- coding: utf-8 -*-
{
    'name': "mcs_aul_product_pricelist",

    'summary': """
        Pricelist""",

    'description': """
        Sales
    """,

    'author': "Aul",
    'website': "http://www.cpm.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['stock','base','product','mcs_aul_sales_product','mcs_contacts_ext','dn_sales_cpm','purchase','dn_inventory_cpm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
