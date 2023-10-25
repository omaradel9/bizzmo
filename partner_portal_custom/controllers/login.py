# -*- coding: utf-8 -*-
import logging
import werkzeug
import werkzeug
import werkzeug.exceptions
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi
from collections import OrderedDict
from werkzeug.urls import url_decode, iri_to_uri
from xml.etree import ElementTree
import unicodedata

from odoo import http, _
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db, Home,SIGN_UP_REQUEST_PARAMS
# from odoo.addons.web_settings_dashboard.controllers.main import WebSettingsDashboard as Dashboard
from odoo.exceptions import UserError
from odoo.http import request
import requests
import json
_logger = logging.getLogger(__name__)


class AuthSignupHome(Home):


    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = {key: qcontext.get(key) for key in ('login', 'name', 'password','company_name')}
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        # if values.get('company_name'):
        #     raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '').split('_')[0]
        if lang in supported_lang_codes:
            values['lang'] = lang
        print("_signup_with_values :> ",values)
        self._signup_with_values(qcontext.get('token'), values)

        user = request.env['res.users'].sudo().search([('email','=',values['login'])])
        if values.get('company_name'):

            request.env['res.partner'].sudo().create(
                {
                    'name': values['company_name'],
                    'company_type': 'company',
                    'child_ids': [(6,0,[user.partner_id.id])],
                    'email': values['login'],
                }
            )
        print("request.env :> ",request.env)
        request.env.cr.commit()
        print("request.env 2 :> ",request)


class AuthSighup(AuthSignupHome):

    def get_auth_signup_qcontext(self):
        SIGN_UP_REQUEST_PARAMS.update({'company_name'})
        return super().get_auth_signup_qcontext()