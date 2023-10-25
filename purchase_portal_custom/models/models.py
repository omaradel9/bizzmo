# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrderInh(models.Model):
    _inherit = 'purchase.order'

    vendor_state = fields.Selection(
        string='Vendor state',
        selection=[
            ('pending', 'Pending'),
            ('update', 'Updated'),
            ('approved', 'Approved'),
                   ],
        required=False,default="pending" )


    def confirm_vendor(self):
        self.vendor_state = 'approved'
        for line in self.order_line:
            line.vendor_state = 'approved'


        orders = self.env['purchase.order'].search(
            [('sale_order_dropship', '=', self.sale_order_dropship.id),('vendor_state','=','pending')])
        if not orders:
            self.sale_order_dropship.action_confirm()
            orders = self.env['purchase.order'].search(
                [('sale_order_dropship', '=', self.sale_order_dropship.id)])
            for o in orders:
                o.button_confirm()


class PurchaseOrderLineInh(models.Model):
    _inherit = 'purchase.order.line'

    vendor_state = fields.Selection(
        string='Vendor state',
        selection=[('pending', 'Pending'),
                   ('approved', 'Approved'), ],
        required=False, default="pending")



    order_partner_id = fields.Many2one(related='order_id.partner_id', store=True, string='Vendor', index=True)
