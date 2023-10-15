# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_order_dropship = fields.Many2one(
        comodel_name='sale.order',
        string='Sale_order_dropship',
        required=False)