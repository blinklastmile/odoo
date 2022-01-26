# -*- coding: utf-8 -*-
# Part of Blinklastmile. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    deliv_label = fields.Char(string='Label')
