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
    'depends': ['stock_account'],
    'data': [
        'views/sale.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': True,
    'assets': {},
    'license': 'LGPL-3',
}
