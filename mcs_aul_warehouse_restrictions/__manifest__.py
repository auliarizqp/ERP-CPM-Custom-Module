# -*- coding: utf-8 -*-

{
    'name': "mcs_aul_warehouse_restrictions",

    'summary': """
         Warehouse and Stock Locations, Picking types and picking Restriction on Users.""",

    'description': """
        This Module Restricts the User from Accessing Warehouse and Process Stock Moves other than allowed to Warehouses and Stock Locations.
    """,

    'author': "Aul",
    'website': "https://www.linkedin.com/in/auliarizqp/",

    'category': 'Warehouse',
    'version': '13.0.2.0',

    'depends': ['base', 'stock'],

    'data': [
        'views/users.xml',
        'security/security.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}
