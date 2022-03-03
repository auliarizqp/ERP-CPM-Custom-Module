# -*- coding: utf-8 -*-
{
    'name': "mc_aul_reporting_and_report",

    'summary': """
        Reporting and Report""",

    'description': """
        Sales and Inventory
    """,

    'author': "CPM",
    'website': "http://www.cpm.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales and Inventory',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','dn_inventory_cpm','dn_sales_cpm','purchase','rnf_cpm_custom','dn_molding_depreciation_cpm','dn_purchase_cpm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/sj_toyota_denso.xml',
        'views/sj_panasonic.xml',
        'views/bukti_terima.xml',
        'views/inherit_rfq.xml',
        # 'views/reporting_other.xml',
        'views/master_data_item_number.xml',
        'views/master_data_part_number.xml',
        
    ],
}
