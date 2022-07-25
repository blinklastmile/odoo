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

        print(stock_picking.move_line_ids)
        # dict data collect
        request_body = {}
        for line in stock_picking.move_line_ids:
            package = self.env['stock.quant.package'].browse([line['result_package_id'].id])
            # self.deliv_label = "http://localhost:8000/admin/database/delivery/63b51efa-8429-4b04-ae59-4781bd76faec"
            try:
                print("name", package.name)
                request_body = {
                    'width': package.package_type_id.width,
                    'height': package.package_type_id.height,
                    'depth': package.package_type_id.packaging_length,
                    'weight': package.package_type_id.max_weight,
                    'delivery': self.deliv_label.split("/")[-1]
                }

                print(request_body)
                url = self.deliv_label.split("admin")[0]

                if package.x_initial_type is not None and package.x_initial_type == package.package_type_id:
                    print('updating package')
                    request_body['code'] = package.name
                    response = requests.patch(url + "api/admin/packages/" + package.id, data=request_body)
                    print(response.content)
                else:
                    print('creating package')
                    response = requests.post(url + "api/admin/packages/", data=request_body)
                    print(response.text)
                    package.name = json.loads(response.text)['code']

            except Exception as e:
                print(str(e))
