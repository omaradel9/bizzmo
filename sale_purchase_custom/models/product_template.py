# -*- coding: utf-8 -*-

from odoo import models, fields, api

class productTemplateInh(models.Model):
    _inherit = 'product.template'

    @api.model
    def _get_buy_route(self):
        buy_route = self.env.ref('purchase_stock.route_warehouse0_buy', raise_if_not_found=False)
        drop_shipping = self.env.ref('stock_dropshipping.route_drop_shipping', raise_if_not_found=False)
        print("drop_shipping :> ",drop_shipping)
        ids = []
        if buy_route:
            ids.append(self.env['stock.location.route'].search([('id', '=', buy_route.id)]).id)
            # return self.env['stock.location.route'].search([('id', '=', buy_route.id)]).ids
        if drop_shipping:
            ids.append(self.env['stock.location.route'].search([('id', '=', drop_shipping.id)]).id)
        # return []
        return ids

    route_ids = fields.Many2many(default=lambda self: self._get_buy_route())



    @api.model
    def create(self, values):
        res = super(productTemplateInh, self).create(values)
        print('res :> ',res)
        print('res :> ',res.id)
        # Add code here
        self.env['product.supplierinfo'].create([
            {
                'name': self.env.user.partner_id.id,
                'product_tmpl_id': res.id,
                'min_qty': 1,
                'price': 1,
            }])
        return res


    purchase_price = fields.Float(
        string='Purchase price',
        required=False)


    dropship_custom = fields.Boolean(
        string='Dropship',
        required=False,default=True)