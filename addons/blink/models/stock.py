# -*- coding: utf-8 -*-
# Part of Blinklastmile. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.tools.sql import column_exists, create_column
import requests, json
# from openerp.addons.web.http import request

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    deliv_label = fields.Char(related="sale_id.deliv_label", string="Label")
    first_order = fields.Boolean(related="sale_id.first_order",string='First Order')

    def action_sync_packages(self):
        stock_picking = super(StockPicking, self)
        request_body = []
        already_in = []
        for line in stock_picking.move_line_ids:
            package = self.env['stock.quant.package'].browse([line['result_package_id'].id])
            # self.deliv_label = "http://localhost:8000/admin/database/delivery/63b51efa-8429-4b04-ae59-4781bd76faec"

            if package.name in already_in:
                continue
            try:
                package_data = {
                    'width': package.package_type_id.width,
                    'height': package.package_type_id.height,
                    'depth': package.package_type_id.packaging_length,
                    'weight': package.package_type_id.max_weight,
                    'delivery': self.deliv_label.split("/")[-1],
                    'external_id': package.id
                }
                if package.external_id:
                    package_data['uuid'] = package.external_id
                already_in.append(package.name)
                request_body.append(package_data)
            except Exception as e:
                print(str(e))

        url = self.deliv_label.split("admin")[0]
        response = requests.post(url + "api/admin/deliveries/" + self.deliv_label.split("/")[-1] + "/sync_packages/",
                                  json=request_body)
        new_packages = json.loads(response.text)
        for new_package in new_packages:
            package = self.env['stock.quant.package'].browse([int(new_package['external_id'])])
            if package:
                package.name = new_package['code']
                if 'uuid' in new_package:
                    package.external_id = new_package['uuid']


