from odoo import api, fields, models, _

class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    initial_type = fields.Many2one("stock.package.type", string="Initial package type from oms")
    external_id = fields.Char(string="UUID")
