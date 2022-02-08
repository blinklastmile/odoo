# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = ['barcodes.barcode_events_mixin', 'stock.picking']

    def on_barcode_scanned(self, barcode):

        is_last_scanned = False
        sequence = 0
        warm_sound_code = ""

        if self.env.user.company_id.sudo().sh_inventory_barcode_scanner_last_scanned_color:
            is_last_scanned = True

        if self.env.user.company_id.sudo().sh_inventory_barcode_scanner_move_to_top:
            sequence = -1

        if self.env.user.company_id.sudo().sh_inventory_barcode_scanner_warn_sound:
            warm_sound_code = "SH_BARCODE_SCANNER_"

        if self.env.user.company_id.sudo().sh_inventory_barcode_scanner_auto_close_popup:
            warm_sound_code += "AUTO_CLOSE_AFTER_" + \
                str(self.env.user.company_id.sudo(
                ).sh_inventory_barcode_scanner_auto_close_popup) + "_MS&"

        if self and self.state not in ['assigned', 'draft', 'confirmed']:
            selections = self.fields_get()['state']['selection']
            value = next((v[1] for v in selections if v[0]
                          == self.state), self.state)
            raise UserError(
                _(warm_sound_code + "You can not scan item in %s state.") % (value))

        elif self:
            self.move_ids_without_package.update({
                'sh_inventory_barcode_scanner_is_last_scanned': False,
                'sequence': 0,
            })
            search_mls = False
            domain = []
            if self.env.user.company_id.sudo().sh_inventory_barcode_scanner_type == 'barcode':
                search_mls = self.move_ids_without_package.filtered(
                    lambda ml: ml.product_id.barcode == barcode)
                domain = [("barcode", "=", barcode)]

            elif self.env.user.company_id.sudo().sh_inventory_barcode_scanner_type == 'int_ref':
                search_mls = self.move_ids_without_package.filtered(
                    lambda ml: ml.product_id.default_code == barcode)
                domain = [("default_code", "=", barcode)]

            elif self.env.user.company_id.sudo().sh_inventory_barcode_scanner_type == 'sh_qr_code':
                search_mls = self.move_ids_without_package.filtered(
                    lambda ml: ml.product_id.sh_qr_code == barcode)
                domain = [("sh_qr_code", "=", barcode)]

            elif self.env.user.company_id.sudo().sh_inventory_barcode_scanner_type == 'all':
                search_mls = self.move_ids_without_package.filtered(lambda ml: ml.product_id.barcode == barcode or
                                                                    ml.product_id.default_code == barcode or
                                                                    ml.product_id.sh_qr_code == barcode
                                                                    )
                domain = ["|", "|",
                          ("default_code", "=", barcode),
                          ("barcode", "=", barcode),
                          ("sh_qr_code", "=", barcode)
                          ]
            if search_mls:
                for move_line in search_mls:
                    if move_line.show_details_visible:
                        raise UserError(
                            _(warm_sound_code + "You can not scan product item for Detailed Operations directly here, Pls click detail button (at end each line) and than rescan your product item."))

                    if self.state == 'draft':
                        move_line.product_uom_qty += 1
                        move_line.sh_inventory_barcode_scanner_is_last_scanned = is_last_scanned
                        move_line.sequence = sequence
                    else:
                        move_line.quantity_done = move_line.quantity_done + 1
                        move_line.sh_inventory_barcode_scanner_is_last_scanned = is_last_scanned
                        move_line.sequence = sequence
                        if move_line.quantity_done == move_line.product_uom_qty + 1:
                            warning_mess = {
                                'title': _('Alert!'),
                                'message': warm_sound_code + 'Becareful! Quantity exceed than initial demand!'
                            }
                            return {'warning': warning_mess}
                    break
            elif self.state == 'draft':
                if self.env.user.company_id.sudo().sh_inventory_barcode_scanner_is_add_product:
                    if not self.picking_type_id:
                        raise UserError(
                            _(warm_sound_code + "You must first select a Operation Type."))
                    search_product = self.env["product.product"].search(
                        domain, limit=1)
                    if search_product:
                        order_line_val = {
                            "name": search_product.name,
                            "product_id": search_product.id,
                            "product_uom_qty": 1,
                            "price_unit": search_product.lst_price,
                            "location_id": self.location_id.id,
                            "location_dest_id": self.location_dest_id.id,
                            'sh_inventory_barcode_scanner_is_last_scanned': is_last_scanned,
                            'sequence': sequence,
                        }
                        if search_product.uom_id:
                            order_line_val.update({
                                "product_uom": search_product.uom_id.id,
                            })
                        old_lines = self.move_ids_without_package
                        new_order_line = self.move_ids_without_package.create(
                            order_line_val)
                        self.move_ids_without_package = old_lines + new_order_line
                        new_order_line._onchange_product_id()
                    else:
                        raise UserError(
                            _(warm_sound_code + "Scanned Internal Reference/Barcode/QR Code '%s' does not exist in any product!") %(barcode))

                else:
                    raise UserError(
                        _(warm_sound_code + "Scanned Internal Reference/Barcode/QR Code '%s' does not exist in any product!") %(barcode))
            else:
                raise UserError(
                    _(warm_sound_code + "Scanned Internal Reference/Barcode/QR Code '%s' does not exist in any product!") %(barcode))
