# -*- coding: utf-8 -*-
{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Real Estate',
    'summary': 'Manage real estate properties',
    'depends': ['base'],
    'data': ['security/ir.model.access.csv',
             'views/estate_menus.xml',  
             'views/estate_property_views.xml',
             'views/estate_property_tag_views.xml',
             'views/estate_property_type_views.xml',
             'views/estate_property_offer_views.xml',
             ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

