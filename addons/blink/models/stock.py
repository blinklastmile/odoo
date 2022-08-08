# -*- coding: utf-8 -*-
# Part of Blinklastmile. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
import logging
from odoo.addons.blink.config._env import *
from odoo.exceptions import ValidationError, UserError
from odoo.tools.sql import column_exists, create_column
import requests, json

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    deliv_label = fields.Char(related="sale_id.deliv_label", string="Label")
    first_order = fields.Boolean(related="sale_id.first_order", string='First Order')
    external_delivery_id = fields.Char(related="sale_id.external_delivery_id", string="External id")
    delivery_url = fields.Char(string="Delivery label", compute="get_delivery_url")

    @api.depends('external_delivery_id')
    def get_delivery_url(self):
        for rec in self:
            if rec.external_delivery_id:
                rec.delivery_url = "{}admin/database/delivery/{}".format(BLINK_ADMIN_BASE_URL, rec.external_delivery_id)
            else:
                rec.delivery_url = None

    def action_sync_packages(self):
        stock_picking = super(StockPicking, self)
        request_body = []
        already_in = []
        for line in stock_picking.move_line_ids:
            package = self.env['stock.quant.package'].browse([line['result_package_id'].id])

            if package.name in already_in:
                continue
            try:
                package_data = {
                    'width': package.package_type_id.width,
                    'height': package.package_type_id.height,
                    'depth': package.package_type_id.packaging_length,
                    'weight': package.package_type_id.max_weight,
                    'external_id': package.id
                }
                if package.external_id:
                    package_data['uuid'] = package.external_id

                already_in.append(package.name)
                request_body.append(package_data)
            except Exception as e:
                _logger.exception(str(e))
        _logger.debug("Request sync packages body: {}".format(request_body))

        if not self.env.user.access_token:
            self.set_access_token()

        if not self.external_delivery_id:
            raise UserError("No external delivery id found")

        response = self.request_sync_packages(request_body)
        _logger.debug("Requesting access token: {}".format(response.text))
        if response.status_code == 201:
            new_packages = json.loads(response.text)
            for new_package in new_packages:
                package = self.env['stock.quant.package'].browse([int(new_package['external_id'])])
                if package:
                    package.name = new_package['code']

                if 'uuid' in new_package:
                    package.external_id = new_package['uuid']
        elif response.status_code == 401:
            update_response = self.update_access_token()
            if not update_response == 200:
                self.set_access_token()
            response = self.request_sync_packages(request_body)
            if not response.status_code == 201:
                _logger.debug("Error occurred when sending request.\n{}".format(response.text))
                raise UserError("Error occurred when sending request.\n{}".format(response.text))

    def request_sync_packages(self, request_body):
        _logger.debug("Request sync packages body: {}".format(request_body))
        return requests.post(BLINK_ADMIN_BASE_URL + "api/admin/deliveries/"
                             + self.external_delivery_id + "/sync_packages/",
                             json=request_body,
                             headers={"Authorization": "Bearer {}".format(self.env.user.access_token)})

    def set_access_token(self):
        request_body = {
            "grant_type": "password",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "username": self.env.user.blink_email,
            "password": self.env.user.blink_password,
        }
        response = requests.post(BLINK_ADMIN_BASE_URL + "api/admin/o/token/", data=request_body)
        if response.status_code == 200:
            response = json.loads(response.text)
            self.env.user.access_token = response['access_token']
            self.env.user.refresh_token = response['refresh_token']
        _logger.debug("Request body: {}".format(request_body))

    def update_access_token(self):
        request_body = {
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": self.env.user.refresh_token,
        }
        response = requests.post(BLINK_ADMIN_BASE_URL + "api/admin/o/token/", data=request_body)
        if response.status_code == 200:
            response = json.loads(response.text)
            self.env.user.access_token = response['access_token']
            self.env.user.refresh_token = response['refresh_token']
            return 200
        _logger.debug("Request body: {}".format(request_body))
