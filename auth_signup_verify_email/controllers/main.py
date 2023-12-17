# Copyright 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
import werkzeug
from werkzeug.urls import url_encode

from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.exceptions import UserError
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
import logging
from odoo import http, tools, _
from odoo.http import request
_logger = logging.getLogger(__name__)


class SignupVerifyEmail(AuthSignupHome):
    @http.route('/web/verification', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signupss(self, *args, **kw):
        user = self.send_otps()
        if user.verified:
            return request.redirect('/web')
        else:
            return request.render("auth_signup_verify_email.signup_verification", {'email': request.session.get('login')})

    @http.route('/web/send_otps', type='json', auth="user", csrf=False)
    def send_otps(self, *args, **kw):
        user = request.env["res.users"].sudo().search([("login", "=", request.session.get('login'))])
        user._generate_otp()
        user._send_otp(request.session.get('login'))
        return user

    @http.route('/web/check_otp', type='json', auth="user", csrf=False)
    def check_otp(self, *args, **kw):
        input_email = kw.get('email')
        input_otp = kw.get('otp')
        user = request.env["res.users"].sudo().search([("login", "=", input_email)])
        _logger.exception("=======input_otp : %s", input_otp)
        _logger.exception("=======str(user.otp) : %s", str(user.otp))
        if str(user.otp) == str(input_otp):
            user.write({'verified' : True})
            returns = 'done'

        else:
            returns = 'wrong'

        return returns
    @http.route()
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                User = request.env['res.users']
                user_sudo = User.sudo().search(
                    User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                )
                template = request.env.ref('auth_signup.mail_template_user_signup_account_created', raise_if_not_found=False)
                if user_sudo and template:
                    template.sudo().send_mail(user_sudo.id, force_send=True)
                # return self.web_login(*args, **kw)
                return request.redirect('/web/verification')

            except UserError as e:
                qcontext['error'] = e.args[0]
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        elif 'signup_email' in qcontext:
            user = request.env['res.users'].sudo().search([('email', '=', qcontext.get('signup_email')), ('state', '!=', 'new')], limit=1)
            if user:
                return request.redirect('/web/login?%s' % url_encode({'login': user.login, 'redirect': '/web'}))

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response