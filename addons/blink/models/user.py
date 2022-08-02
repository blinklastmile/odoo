from odoo import api, fields, models, _

class ResUser(models.Model):
    _inherit = 'res.users'

    blink_email = fields.Char(string="Blink email")
    blink_password = fields.Char(string="Blink password")
    access_token = fields.Char(string="Access token")
    refresh_token = fields.Char(string="Refresh token")