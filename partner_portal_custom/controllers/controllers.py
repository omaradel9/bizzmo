# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import content_disposition, Controller, request, route

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo import fields as odoo_fields, http, tools, _, SUPERUSER_ID
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError, AccessDenied


class PortalCustom(CustomerPortal):

    @route(['/my/sub/partner'], type='http', auth='user', website=True)
    def smy_sub_partner(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            print("post :> ",post)
            found = request.env['res.users'].sudo().search([('id', '=', request.env.user.id)])
            if found:
                ids = []
                ids = found.partner_id.child_ids.ids
                new_portal_user = found.copy(default={'login': post['email']})
                print("new_portal_user :> ", new_portal_user)
                new_portal_user.write({
                    'name': post['name'],
                    'email': post['email'],
                    'password': '1',
                })
                ids.append(new_portal_user.partner_id.id)
                print("ids :> ",ids)
                found.partner_id.child_ids = [(6,0,ids)]
            #
            # # internal_user_group.users = [(3, created_user.id)]
            # # portal_user_group.users = [(4, created_user.id)]
            #
            # # public_user_group.users = [(3, created_user.id)]
            #
            # rec.user_id = new_portal_user.id
            if redirect:
                        return request.redirect(redirect)
            return request.redirect('/my/home')



        response = request.render("partner_portal_custom.portal_create_partner", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    def details_form_validate_company(self, data):
        error = dict()
        error_message = []

        # Validation
        for field_name in self.MANDATORY_BILLING_FIELDS:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # vat validation
        partner = request.env.user.partner_id.parent_id
        if data.get("vat") and partner and partner.vat != data.get("vat"):
            # if partner.can_edit_vat():
                if hasattr(partner, "check_vat"):
                    if data.get("country_id"):
                        print("request.env['res.partner'] :> ",request.env["res.partner"])
                        data["vat"] = request.env["res.partner"].fix_eu_vat_number(int(data.get("country_id")), data.get("vat"))
                    partner_dummy = partner.new({
                        'vat': data['vat'],
                        'country_id': (int(data['country_id'])
                                       if data.get('country_id') else False),
                    })
                    try:
                        partner_dummy.check_vat()
                    except ValidationError:
                        error["vat"] = 'error'
            # else:
            #     error_message.append(_('Changing VAT number is not allowed once document(s) have been issued for your account. Please contact us directly for this operation.'))

        # error message for empty required fields
        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        unknown = [k for k in data if k not in self.MANDATORY_BILLING_FIELDS + self.OPTIONAL_BILLING_FIELDS]
        if unknown:
            error['common'] = 'Unknown field'
            error_message.append("Unknown field '%s'" % ','.join(unknown))

        return error, error_message

    @route(['/update/company/data'], type='http', auth='user', website=True)
    def update_company_data(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id.parent_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            error, error_message = self.details_form_validate_company(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
                values.update({key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})
                for field in set(['country_id', 'state_id']) & set(values.keys()):
                    try:
                        values[field] = int(values[field])
                    except:
                        values[field] = False
                values.update({'zip': values.pop('zipcode', '')})
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            # 'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })

        response = request.render("partner_portal_custom.portal_my_company_details", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response