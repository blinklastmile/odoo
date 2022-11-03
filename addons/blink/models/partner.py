from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    custom_packaging_tutorial_url = fields.Char(string='Packaging tutorial')
