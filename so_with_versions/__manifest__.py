# -*- coding: utf-8 -*-
{
    'name': "SO(versioning)",

    'summary': "An improved version of SO module which includes versioning",

    'description': """
Long description of module's purpose
    """,

    'author': "Adnan Sabbir",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sales_order_views.xml'
    ]
}
