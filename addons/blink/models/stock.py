# -*- coding: utf-8 -*-
# Part of Blinklastmile. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.tools.sql import column_exists, create_column


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sale_order = fields.Many2one(related="group_id.sale_id", string="Sales Order", store=True, readonly=False)

    # deliv_label = fields.Char(related="sale_id.deliv_label")
