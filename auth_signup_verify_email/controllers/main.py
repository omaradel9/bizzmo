# Copyright 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from email_validator import EmailSyntaxError, EmailUndeliverableError, validate_email

from odoo import _
from odoo.http import request, route

from odoo.addons.auth_signup.controllers.main import AuthSignupHome

_logger = logging.getLogger(__name__)
SIGN_UP_REQUEST_PARAMS = {'db', 'login', 'debug', 'token', 'message', 'error', 'scope', 'mode', 'zipcode',
                          'redirect', 'redirect_hostname', 'email', 'name', 'partner_id', 'company_name',
                          'password', 'confirm_password', 'city', 'country_id', 'lang', 'vat', 'mobile', 'phone',
                          'state_id', 'street','industry_id','website'}

class SignupVerifyEmail(AuthSignupHome):


    def _prepare_signup_values(self, qcontext):
        print("ffffffffffff",qcontext)
        values = {key: qcontext.get(key) for key in (
            'login', 'name', 'password', 'mobile', 'phone', 'country_id', 'state_id', 'street','industry_id','website')}
        # if not values:
        #     raise UserError(_("The form was not properly filled in."))
        # if values.get('password') != qcontext.get('confirm_password'):
        #     raise UserError(_("Passwords do not match; please retype them."))
        if qcontext.get('country_id'):
            values['country_id'] = int(qcontext.get('country_id'))
        if qcontext.get('state_id'):
            values['state_id'] = int(qcontext.get('state_id'))
        if qcontext.get('industry_id'):
            values['industry_id'] = int(qcontext.get('industry_id'))
        if qcontext.get('website'):
            values['website'] = int(qcontext.get('website'))

        if qcontext.get('mobile'):
            values['mobile'] = int(qcontext.get('mobile'))
        # if qcontext.get('zipcode'):
        #     values['zip'] = qcontext.get('zipcode')
        #     del values['zipcode']
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '')
        if lang in supported_lang_codes:
            values['lang'] = lang

        print("values :>",values)
        return values

    def get_auth_signup_config(self):
        res = super(SignupVerifyEmail, self).get_auth_signup_config()
        res.update({
            'countries': request.env['res.country'].search([]),
            'states': request.env['res.country.state'].search([]),
            'industries': request.env['res.partner.industry'].sudo().search([])
        })
        return res


    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        print("qcontext :> ",qcontext)
        values = self._prepare_signup_values(qcontext)
        print("values :> ",values)
        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()

    @route()
    def web_auth_signup(self, *args, **kw):
        if request.params.get("login") and not request.params.get("password"):
            return self.passwordless_signup()
        return super().web_auth_signup(*args, **kw)

    def _signup_with_values(self, token, values):
        params = dict(request.params)
        print("params :> ",params)
        country_id = params.get('country_id')
        state_id = params.get('state_id')
        industry_id = params.get('industry_id')
        mobile = params.get('mobile')
        phone = params.get('phone')
        website = params.get('website')
        street = params.get('street')
        street2 = params.get('street2')
        values.update({
            'state_id' : int(state_id) if state_id else state_id,
            'country_id' : int(country_id) if country_id else country_id,
            'industry_id' : int(industry_id) if industry_id else industry_id,
            'mobile': int(mobile) if mobile else mobile,
            'phone': int(phone) if phone else phone,
            'website': website if website else website,
            'street': street if street else street,
            'street2': street2 if street2 else street2,
        })
        print("values ::>>>",values)
        return super(SignupVerifyEmail, self)._signup_with_values(token, values)
    def passwordless_signup(self):
        values = request.params
        qcontext = self.get_auth_signup_qcontext()
        print("passwordless_signup qcontext ")

        # Check good format of e-mail
        try:
            validate_email(values.get("login", ""))
        except EmailSyntaxError as error:
            qcontext["error"] = getattr(
                error,
                "message",
                _("That does not seem to be an email address."),
            )
            return request.render("auth_signup.signup", qcontext)
        except EmailUndeliverableError as error:
            qcontext["error"] = str(error)
            return request.render("auth_signup.signup", qcontext)
        except Exception as error:
            qcontext["error"] = str(error)
            return request.render("auth_signup.signup", qcontext)
        if not values.get("email"):
            values["email"] = values.get("login")

        # preserve user lang
        values["lang"] = request.context.get("lang", "")

        # remove values that could raise "Invalid field '*' on model 'res.users'"
        values.pop("redirect", "")
        values.pop("token", "")

        # Remove password
        values["password"] = ""
        sudo_users = request.env["res.users"].with_context(create_user=True).sudo()

        try:
            with request.cr.savepoint():
                sudo_users.signup(values, qcontext.get("token"))
                sudo_users.reset_password(values.get("login"))
        except Exception as error:
            # Duplicate key or wrong SMTP settings, probably
            _logger.exception(error)
            if (
                request.env["res.users"]
                .sudo()
                .search([("login", "=", qcontext.get("login"))])
            ):
                qcontext["error"] = _(
                    "Another user is already registered using this email" " address."
                )
            else:
                # Agnostic message for security
                qcontext["error"] = _(
                    "Something went wrong, please try again later or" " contact us."
                )
            return request.render("auth_signup.signup", qcontext)

        qcontext["message"] = _("Check your email to activate your account!")
        return request.render("auth_signup.reset_password", qcontext)

# class AuthSighup(AuthSignupHome):
#
#     def get_auth_signup_qcontext(self):
#         SIGN_UP_REQUEST_PARAMS.update({'mobile', 'phone',
#                           'state_id', 'street','industry_id','website'})
#         return super().get_auth_signup_qcontext()