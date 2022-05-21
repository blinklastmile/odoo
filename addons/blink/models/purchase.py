# -*- coding: utf-8 -*-
# Part of Blinklastmile. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_restock(self):
        purchase_order = super(PurchaseOrder, self)
        seller = purchase_order.partner_id[0]
        supplier_infos = self.env['product.supplierinfo'].search_read([])
        for supplier_info in supplier_infos:
            isAlreadyInOrderLine = False
            if not supplier_info['name'][0] == seller.id:
                continue

            product_tmpl = self.env['product.template'].browse(supplier_info['product_tmpl_id'][0])
            for orderline in purchase_order.order_line:
                if orderline['product_id'] == product_tmpl['product_variant_id']:
                    isAlreadyInOrderLine = True
                    break
            if isAlreadyInOrderLine:
                continue

            product = self.env['product.product'].browse([product_tmpl['product_variant_id']]).id

            try:
                min_qty = product[0]['reordering_min_qty']
                max_qty = product[0]['reordering_max_qty']
                on_hand = product_tmpl['qty_available']
                if on_hand > min_qty and on_hand < max_qty:
                    purchase_order.order_line.create({
                        'order_id': seller.id,
                        'product_id': product_tmpl['product_variant_id'].id,  # some product.product ID,
                        'product_qty': max_qty-on_hand,
                        'price_unit': product_tmpl['price'],
                    })
            except:
                print("no reordering data")