# -*- coding: utf-8 -*-
# Part of Blinklastmile. See LICENSE file for full copyright and licensing details.
from odoo.addons.blink.config._env import BLINK_ADMIN_BASE_URL
from odoo.addons.blink.utils import get_delivery_url
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    deliv_label = fields.Char(string='Label')
    first_order = fields.Boolean('First Order',default=False)
    source = fields.Char(string='Source')
    external_delivery_id = fields.Char(string="External id")
    picking_tutorial = fields.Char(string="Picking Tutorial")
    delivery_url = fields.Char(string="Delivery label", compute="set_delivery_url")

    @api.depends('external_delivery_id')
    def set_delivery_url(self):
        for rec in self:
            rec.delivery_url = get_delivery_url(rec.external_delivery_id)