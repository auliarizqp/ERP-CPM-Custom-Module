# -*- coding: utf-8 -*-
{
    'name': "mcs_aul_cpm_add_and_remove",

    'summary': """
        11""",

    'description': """
        Add and Remove Field
    """,

    'author': "Aul",
    'website': "http://www.cpm.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale_management','dn_sales_cpm','rnf_cpm_custom'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/add_and_remove.xml',
    ],
}
