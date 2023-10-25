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
from odoo.addons.portal.controllers.portal import pager as portal_pager


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
            pol.sudo().sale_line_id.product_uom_qty = float(req_qty or 0) if req_qty else 0
            lines.append((
                {
                    'product_id': int(product_id) if product_id else 0,
                    'product_qty': float(req_qty or 0) if req_qty else 0,
                    'line_id': int(line_id) if line_id else 0,
                }))
            pol.sudo().order_id.vendor_state = 'update'
        print("lines :> ", lines)
        try:
            order_sudo = self._document_check_access('purchase.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._purchase_order_get_page_view_values(order_sudo, access_token, **kw)

        return request.redirect('/my/purchase/'+ str(order_id) + "?access_token=" + str(access_token))

    # @http.route(['/my/purchase/update_lines'], type='http', auth="public", website=True)
    # def portal_my_purchase_order_update_lines2(self, order_id=None, access_token=None, **post):
    #     print("kw :> ", post)
    #     print("dddddddkkkkkkk")
    #     form_data = request.httprequest.form
    #     product_names = form_data.getlist('product_name')
    #     print("product_names :> ")
    #     try:
    #         order_sudo = self._document_check_access('purchase.order', order_id, access_token=access_token)
    #     except (AccessError, MissingError):
    #         return request.redirect('/my')
    #     values = self._purchase_order_get_page_view_values(order_sudo, access_token, **post)
    #
    #
    #     return request.render("purchase.portal_my_purchase_order", values)

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
        po.confirm_vendor()
        try:
            order_sudo = self._document_check_access('purchase.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._purchase_order_get_page_view_values(order_sudo, access_token, **post)
        # return request.render("purchase.portal_my_purchase_order", values)
        return request.redirect('/my/purchase/'+ str(order_id) + "?access_token=" + str(access_token))

        # return request.render("purchase.portal_my_purchase_order", values)


    @http.route(['/my/rfq', '/my/rfq/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_requests_for_quotation(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, **kw):
        print("request.env.user.partner_id.id :> ",request.env.user.partner_id.id)
        return self._render_portal(
            "purchase.portal_my_purchase_rfqs",
            page, date_begin, date_end, sortby, filterby,
            [('state', 'in', ['sent','draft'])],
            {},
            None,
            "/my/rfq",
            'my_rfqs_history',
            'rfq',
            'rfqs'
        )

    def _render_portal(self, template, page, date_begin, date_end, sortby, filterby, domain, searchbar_filters, default_filter, url, history, page_name, key):
        values = self._prepare_portal_layout_values()
        PurchaseOrder = request.env['purchase.order']
        domain += [('partner_id','=',request.env.user.partner_id.id)]
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc, id desc'},
            'name': {'label': _('Name'), 'order': 'name asc, id asc'},
            'amount_total': {'label': _('Total'), 'order': 'amount_total desc, id desc'},
        }
        # default sort
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if searchbar_filters:
            # default filter
            if not filterby:
                filterby = default_filter
            domain += searchbar_filters[filterby]['domain']

        # count for pager
        count = PurchaseOrder.search_count(domain)

        # make pager
        pager = portal_pager(
            url=url,
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby},
            total=count,
            page=page,
            step=self._items_per_page
        )

        # search the purchase orders to display, according to the pager data
        orders = PurchaseOrder.search(
            domain,
            order=order,
            limit=self._items_per_page,
            offset=pager['offset']
        )
        request.session[history] = orders.ids[:100]

        values.update({
            'date': date_begin,
            key: orders,
            'page_name': page_name,
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
            'default_url': url,
        })
        return request.render(template, values)


    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        PurchaseOrder = request.env['purchase.order']
        if 'rfq_count' in counters:
            values['rfq_count'] = PurchaseOrder.search_count([
                ('state', 'in', ['sent','draft']),('partner_id','=',request.env.user.partner_id.id)
            ]) if PurchaseOrder.check_access_rights('read', raise_exception=False) else 0
        if 'purchase_count' in counters:
            values['purchase_count'] = PurchaseOrder.search_count([
                ('state', 'in', ['purchase', 'done', 'cancel']),('partner_id','=',request.env.user.partner_id.id)
            ]) if PurchaseOrder.check_access_rights('read', raise_exception=False) else 0
        return values