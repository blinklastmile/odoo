# -*- coding: utf-8 -*-
# Part of Blinklastmile. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_restock(self):
        purchase_order = super(PurchaseOrder, self)
        seller = purchase_order.partner_id[0]
        supplier_infos = self.env['product.supplierinfo'].search_read([])
        for supplier_info in supplier_infos:
            is_already_in_order_line = False
            if not supplier_info['name'][0] == seller.id:
                continue

            product_tmpl = self.env['product.template'].browse(supplier_info['product_tmpl_id'][0])
            for orderline in purchase_order.order_line:
                if orderline['product_id'] == product_tmpl['product_variant_id']:
                    is_already_in_order_line = True
                    break
            if is_already_in_order_line is True:
                continue

            product = self.env['product.product'].browse([product_tmpl['product_variant_id']]).id
            try:
                min_qty = product[0]['reordering_min_qty']
                max_qty = product[0]['reordering_max_qty']
                # on_hand = product_tmpl['qty_available']
                forecasted = product_tmpl['virtual_available']
                if min_qty <= forecasted < max_qty:
                    move = self.env['stock.move'].create({
                        'name': self.order_line[0].move_dest_ids.name,
                        'location_id': self.order_line[0].move_dest_ids.location_id.id,
                        'location_dest_id': self.order_line[0].move_dest_ids.location_dest_id.id,
                        'product_id': product_tmpl['product_variant_id'].id,
                        'product_uom': product_tmpl['product_variant_id'].uom_id.id,
                        'product_uom_qty': max_qty-forecasted,
                        'rule_id': self.order_line[0].move_dest_ids.rule_id.id,
                        'picking_id': self.order_line[0].move_dest_ids.picking_id.id
                    })
                    move._action_confirm()
                    move._action_assign()
                    self.order_line[0].move_dest_ids.picking_id.state = 'waiting'
                    purchase_order.order_line.create({
                        'order_id': self.ids[0],
                        'product_id': product_tmpl['product_variant_id'].id,  # some product.product ID,
                        'product_qty': max_qty-forecasted,
                        'price_unit': product_tmpl['price'],
                        'move_dest_ids': move
                    })
            except Exception as e:
                _logger.exception(e)