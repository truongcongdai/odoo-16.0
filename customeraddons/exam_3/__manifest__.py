# -*- coding: utf-8 -*-
{
    'name': "Plan Sale Order",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', "sale", "mail", 'sale_management'],

    # always loaded
    'data': [
        'security/plan_group_security.xml',
        'security/ir.model.access.csv',
        'views/plan_sale_order_views.xml',
        'views/plan_sale_order_menu_views.xml',
        'views/s_sale_order_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'exam_3/static/src/css/custom_style.css',
        ]},
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
