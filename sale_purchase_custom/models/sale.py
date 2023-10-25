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
        print("line.order_id.id :> ",line.order_id.id)
        return {
            'partner_id': partner.id,
            'user_id': False,
            'company_id': company_id.id,
            'currency_id': partner.with_company(company_id).property_purchase_currency_id.id or company_id.currency_id.id,
            'origin': line.order_id.name,
            'payment_term_id': partner.with_company(company_id).property_supplier_payment_term_id.id,
            'sale_order_dropship':line.order_id.id
        }


    def create_po_dropship_action(self,vals):
        return self.env['purchase.order'].sudo().create(vals)

    def create_po_dropship(self):
        for rec in self:
            for line in rec.order_line:
                if line.product_id.dropship_custom == True and line.line_dropship == False:
                    print("rec.id :>",rec.name)
                    print("rec.id :>",line.product_id.seller_ids.name)
                    same_partner = self.env['purchase.order'].search([('sale_order_dropship','=',rec.id),('partner_id','=',line.product_id.seller_ids.name.id)])
                    # same_partner = self.env['purchase.order'].search([('sale_order_dropship','=',rec.id)])
                    id = 0
                    print("rec.id :>",line.product_id.seller_ids.name)

                    for s in same_partner:
                        if s.partner_id.id == line.product_id.seller_ids.id:
                            id = s.id
                    print("same_partner :> ",same_partner)
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
                        line.line_dropship = True
                        line.purchase_order_dropship_id = po.id

                    else:
                        vals = rec._prepare_purchase_order_dropship(line,line.product_id.seller_ids.name)
                        print(" data ",vals)
                        po = self.create_po_dropship_action(vals)
                        po.state = 'sent'
                        purchase_order_line = self.env['purchase.order.line'].create({
                            'name': line.name,
                            'product_id': line.product_id.id,
                            'order_id': po.id,
                            'product_qty':line.product_uom_qty,
                            'product_uom':line.product_uom.id,
                            'sale_line_id':line.id,
                            'price_unit':line.product_id.seller_ids.price

                        })

                        line.line_dropship = True
                        line.purchase_order_dropship_id = po.id

    vendor_state = fields.Selection(
        string='Vendor state',
        selection=[
            ('pending', 'Pending'),
            ('update', 'Updated'),
            ('approved', 'Approved'),
                   ],
        required=False,compute="compute_vendor_state" )


    def compute_vendor_state(self):
        for rec in self:
            for line in rec.order_line:
                if line.purchase_order_dropship_id.vendor_state == 'update':
                    rec.vendor_state = 'update'
                    break
                elif line.purchase_order_dropship_id.vendor_state == 'pending':
                    rec.vendor_state = 'pending'

                else:
                    rec.vendor_state = 'approved'


class NewModule(models.Model):
    _inherit = 'sale.order.line'

    line_dropship = fields.Boolean(
        string='Line_dropship',
        required=False)


    purchase_order_dropship_id = fields.Many2one(
        comodel_name='purchase.order',
        string='Purchase_order_dropship_id',
        required=False)


