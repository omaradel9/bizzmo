# -*- coding: utf-8 -*-

from odoo import models, fields, api

class NewModule(models.Model):
    _inherit = 'sale.order'

    def _prepare_purchase_order_dropship(self, line, partner):

        # Since the procurements are grouped if they share the same domain for
        # PO but the PO does not exist. In this case it will create the PO from
        # the common procurements values. The common values are taken from an
        # arbitrary procurement. In this case the first.

        company_id = self.env.user.company_id

        return {
            'partner_id': partner.id,
            'user_id': False,
            'company_id': company_id.id,
            'currency_id': partner.with_company(company_id).property_purchase_currency_id.id or company_id.currency_id.id,
            'origin': line.order_id.name,
            'payment_term_id': partner.with_company(company_id).property_supplier_payment_term_id.id,
            'sale_order_dropship':line.order_id.id
        }


    def create_po_dropship(self):
        for rec in self:
            for line in rec.order_line:
                if line.product_id.dropship_custom == True:
                    same_partner = self.env['purchase.order'].sudo().search([('sale_order_dropship','=',rec.id),('partner_id','=',line.product_id.seller_ids.id)])
                    if same_partner:
                        purchase_order_line = self.env['purchase.order.line'].create({
                            'name': line.name,
                            'product_id': line.product_id.id,
                            'order_id': same_partner.id,
                            'product_qty': line.product_uom_qty,
                            'product_uom': line.product_uom.id,
                            'sale_line_id': line.id,
                            'price_unit': line.product_id.seller_ids.price

                        })
                    else:
                        vals = rec._prepare_purchase_order_dropship(line,line.product_id.seller_ids.name)
                        print(" data ",vals)
                        po = self.env['purchase.order'].sudo().create(vals)
                        purchase_order_line = self.env['purchase.order.line'].create({
                            'name': line.name,
                            'product_id': line.product_id.id,
                            'order_id': po.id,
                            'product_qty':line.product_uom_qty,
                            'product_uom':line.product_uom.id,
                            'sale_line_id':line.id,
                            'price_unit':line.product_id.seller_ids.price

                        })
