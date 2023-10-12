# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class QuoteProducts(models.Model):
    _name = "update.quote.product"
    
    def create_quotation_from_quote_products(self):
        domain = []
        if self._context.get('active_ids'):
            active_ids = self._context.get('active_ids')
            products = self.env['product.template'].browse(active_ids)
            if products:
                order = self.env['sale.order'].create({
                    'partner_id': self.env.user.partner_id.id,
                    'order_line': [(0, 0, {'name': product.name,
                                   'product_id': product.product_variant_id.id})
                            for product in products],
                })
                domain = [('id', '=', order.id)]
                
        return {
            'name': 'Quotations',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'domain': domain,
        }