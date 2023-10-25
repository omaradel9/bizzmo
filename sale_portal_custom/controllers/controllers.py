# -*- coding: utf-8 -*-
import base64
from collections import OrderedDict
from datetime import datetime

from odoo import http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request, Response
from odoo.tools import image_process
from odoo.tools.translate import _
from odoo.addons.sale.controllers.portal import CustomerPortal


class PurchasePortalCustom(CustomerPortal):


    @http.route('/my/orders/<int:order_id>/confirm', auth='user', website=True)
    def confirm_sale_order_from(self, order_id=None, access_token=None, **post):
        sale_order = request.env['sale.order'].sudo().browse(int(order_id))
        sale_order.sudo().action_confirm()
        pos = request.env['purchase.order'].search(
            [('sale_order_dropship', '=', sale_order.id)])

        for p in pos:
            p.sudo().button_confirm()
            p.sudo().vendor_state = 'approved'

        try:
            order_sudo = self._document_check_access('purchase.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._purchase_order_get_page_view_values(order_sudo, access_token, **post)
        # return request.render("purchase.portal_my_purchase_order", values)
        return request.redirect('/my/purchase/'+ str(order_id) + "?access_token=" + str(access_token))

        # return request.render("purchase.portal_my_purchase_order", values)

    # def _prepare_home_portal_values(self, counters):
    #     values = super()._prepare_home_portal_values(counters)
    #     partner = request.env.user.partner_id
    #
    #     SaleOrder = request.env['sale.order']
    #     if 'quotation_count' in counters:
    #         values['quotation_count'] = SaleOrder.search_count(self._prepare_quotations_domain(partner)) \
    #             if SaleOrder.check_access_rights('read', raise_exception=False) else 0
    #     if 'order_count' in counters:
    #         values['order_count'] = SaleOrder.search_count(self._prepare_orders_domain(partner)) \
    #             if SaleOrder.check_access_rights('read', raise_exception=False) else 0
    #
    #     return values
