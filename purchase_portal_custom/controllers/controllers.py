# -*- coding: utf-8 -*-
import base64
from collections import OrderedDict
from datetime import datetime

from odoo import http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request, Response
from odoo.tools import image_process
from odoo.tools.translate import _
from odoo.addons.purchase.controllers.portal import CustomerPortal


class PurchasePortalCustom(CustomerPortal):
    @http.route(['/my/purchase/<int:order_id>'], type='http', auth="public", website=True)
    def portal_my_purchase_order(self, order_id=None, access_token=None, **kw):
        try:
            order_sudo = self._document_check_access('purchase.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        report_type = kw.get('report_type')
        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=order_sudo, report_type=report_type,
                                     report_ref='purchase.action_report_purchase_order', download=kw.get('download'))

        confirm_type = kw.get('confirm')
        if confirm_type == 'reminder':
            order_sudo.confirm_reminder_mail(kw.get('confirmed_date'))
        if confirm_type == 'reception':
            order_sudo._confirm_reception_mail()

        values = self._purchase_order_get_page_view_values(order_sudo, access_token, **kw)
        update_date = kw.get('update')
        if order_sudo.company_id:
            values['res_company'] = order_sudo.company_id
        if update_date == 'True':
            return request.render("purchase.portal_my_purchase_order_update_date", values)
        print("dddddddkkkkkkk")
        return request.render("purchase.portal_my_purchase_order", values)

    @http.route(['/my/purchase/<int:order_id>/update_lines'], type='http', auth="public", website=True)
    def portal_my_purchase_order_update_lines(self, order_id=None, access_token=None, **kw):
        print("kw :> ", kw)
        print("order_id :> ", order_id)
        print("dddddddkkkkkkk")
        form_data = request.httprequest.form

        product_ids = form_data.getlist('product_id')
        line_ids = form_data.getlist('line_id')
        reqs_qty = form_data.getlist('product_qty')
        # request_id = post.pop('my_request_id', False)
        # source_warehouse_id = post.pop('source_warehouse_id', False)
        # values['purchase_count'] = PurchaseOrder.search_count([
        #     ('state', 'in', ['purchase', 'done', 'cancel'])
        # ])
        PurchaseOrderLine = request.env['purchase.order.line']

        lines = []
        for product_id, line_id, req_qty in zip(product_ids, line_ids, reqs_qty):
            pol = PurchaseOrderLine.sudo().search([
                ('id', '=', line_id)
            ])
            pol.sudo().product_qty = float(req_qty or 0) if req_qty else 0
            lines.append((
                {
                    'product_id': int(product_id) if product_id else 0,
                    'product_qty': float(req_qty or 0) if req_qty else 0,
                    'line_id': int(line_id) if line_id else 0,
                }))
        print("lines :> ", lines)
        try:
            order_sudo = self._document_check_access('purchase.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._purchase_order_get_page_view_values(order_sudo, access_token, **kw)
        # return request.render("purchase.portal_my_purchase_order", values)
        return request.redirect('/my/purchase/'+ str(order_id) + "?access_token=" + str(access_token))

    @http.route(['/my/purchase/update_lines'], type='http', auth="public", website=True)
    def portal_my_purchase_order_update_lines2(self, order_id=None, access_token=None, **post):
        print("kw :> ", post)
        print("dddddddkkkkkkk")
        form_data = request.httprequest.form
        product_names = form_data.getlist('product_name')
        print("product_names :> ")
        try:
            order_sudo = self._document_check_access('purchase.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._purchase_order_get_page_view_values(order_sudo, access_token, **kw)
        return request.render("purchase.portal_my_purchase_order", values)

    @http.route('/my/purchase/<int:order_id>/<int:line_id>/delete', auth='user', website=True)
    def delete_req_from(self, order_id=None,line_id=None, access_token=None, **post):
        req = request.env['purchase.order.line'].sudo().browse(int(line_id))
        req.unlink()
        try:
            order_sudo = self._document_check_access('purchase.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._purchase_order_get_page_view_values(order_sudo, access_token, **post)
        # return request.render("purchase.portal_my_purchase_order", values)
        return request.redirect('/my/purchase/'+ str(order_id) + "?access_token=" + str(access_token))

        # return request.render("purchase.portal_my_purchase_order", values)

    @http.route('/my/purchase/<int:order_id>/confirm', auth='user', website=True)
    def confirm_req_from(self, order_id=None, access_token=None, **post):
        po = request.env['purchase.order'].sudo().browse(int(order_id))
        po.button_confirm()
        try:
            order_sudo = self._document_check_access('purchase.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._purchase_order_get_page_view_values(order_sudo, access_token, **post)
        # return request.render("purchase.portal_my_purchase_order", values)
        return request.redirect('/my/purchase/'+ str(order_id) + "?access_token=" + str(access_token))

        # return request.render("purchase.portal_my_purchase_order", values)
