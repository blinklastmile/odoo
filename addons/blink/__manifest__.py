# -*- coding: utf-8 -*-
# Part of Blinklastmile

{
    'name': 'Blink',
    'version': '1.0',
    'category': 'Sales/CRM',
    'summary': 'Quotation, Sales Orders, Delivery & Invoicing Control',
    'description': """
Manage sales quotations and orders
==================================

This module makes the link between the sales and warehouses management applications.


Preferences
-----------
* Shipping: Choice of delivery at once or partial delivery
* Invoicing: choose how invoices will be paid
* Incoterms: International Commercial terms

""",
    'depends': ['stock_account','sale','sale_stock', 'purchase'],
    'data': [
        'views/sale.xml',
        'views/picking.xml',
        'views/location.xml',
        'views/purchase.xml',
        'views/user.xml',
        'views/partner.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': True,
    'assets': {},
    'license': 'LGPL-3',
}
