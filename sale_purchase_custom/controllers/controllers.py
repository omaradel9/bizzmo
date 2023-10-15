# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
print("herer operm")
class OdooWebsiteProductQuote(http.Controller):


    @http.route(['/shop/product/quote/confirm'], type='http', auth="public", website=True)
    def quote_confirm(self, **post):
        print("dddddddddddddddddddddddddd")
        if not post.get('debug'):
            order = request.env['quote.order'].sudo().browse(request.session['quote_order_id'])
            if not order:
                order = request.env['quote.order'].sudo().search([], order='id desc', limit=1)
            if order:
                product_obj = request.env['product.template']
                partner_obj = request.env['res.partner']
                sale_order_obj = request.env['sale.order']
                sale_order_line_obj = request.env['sale.order.line']
                line_vals = {}
                pricelist_id = request.website.get_current_pricelist().id
                vals = {
                    'partner_id': order.partner_id.id,
                    'pricelist_id': pricelist_id,
                    'user_id': request.website.salesperson_id and request.website.salesperson_id.id,
                    'team_id': request.website.salesteam_id and request.website.salesteam_id.id
                }
                sale_order_create = sale_order_obj.sudo().create(vals)
                for i in order.quote_lines:
                    line_vals = {
                        'product_id': i.product_id.id,
                        'name': i.product_id.name,
                        'product_uom_qty': i.qty,
                        'customer_lead': 7,
                        'product_uom': i.product_id.uom_id.id,
                        'order_id': sale_order_create.id}
                    sale_order_line_create = sale_order_line_obj.sudo().create(line_vals)
                    sale_order_line_create.create_po_dropship()

                order.sudo().unlink()
                request.session['quote_order_id'] = False
            return request.render("odoo_website_product_quote.quote_thankyou")
