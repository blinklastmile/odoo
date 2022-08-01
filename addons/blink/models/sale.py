# -*- coding: utf-8 -*-
# Part of Blinklastmile. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    deliv_label = fields.Char(string='Label')
    first_order = fields.Boolean('First Order',default=False)
    source = fields.Char(string='Source')
    external_delivery_id = fields.Char(string="External id")
    delivery_url = fields.Char(string="Delivery label", compute="get_delivery_url")

    @api.depends('external_delivery_id')
    def get_delivery_url(self):
        for rec in self:
            if rec.external_delivery_id:
                rec.delivery_url = "http://localhost:8000/admin/database/delivery/{}".format(rec.external_delivery_id)