# -*- coding: utf-8 -*-
{
    'name': "mcs_aul_sales_orders_manufacturing_orders",

    'summary': """
        Sales and Manufacture""",

    'description': """
        Sales and Manufacture
    """,

    'author': "Aul",
    'website': "http://www.cpm.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales and Manufacture',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','cel_custom_cpm','mrp','dn_purchase_cpm','dn_inventory_cpm','mrp','mrp_maintenance','mrp_workorder','quality_control'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/dandori_mold.xml',
        'views/persiapan_proses_mold.xml',
        'views/setting_kondisi_mold.xml',
        'views/problem_mold.xml',
        'views/problem_mesin_mold.xml',
        'views/robot_mold.xml',
        'views/cooling_mold.xml',
        'views/matl_mold.xml',
        'views/utility_mold.xml',
        'views/wizard_persiapan_mold.xml',
        'views/popup_quantity.xml',
        'views/views.xml',
    ],
}
