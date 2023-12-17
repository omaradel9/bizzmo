# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Archana (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

from odoo import fields, models
import math, random
import logging
_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    """ THe class ResUsers is used to inherit res.users """
    _inherit = "res.users"

    otp = fields.Integer('OTP')
    verified = fields.Boolean('verified')

    def _generate_otp(self):
        """Generates a one-time password (OTP) for the user.

        The OTP is a 6-digit number generated using a random number generator. The OTP is stored in the ``otp`` field of the user record.

        Returns:
            str: The generated OTP.
        """
        digits = "0123456789"
        otp = ""
        for i in range(6):
            otp += digits[math.floor(random.random() * 10)]
        self.otp = otp
        return otp
    def _send_otp(self, login):

        template = self.env.ref('auth_signup_verify_email.verify_email_omar_adeloewmar')

        email_values = {
            'email_cc': False,
            'auto_delete': True,
            'message_type': 'user_notification',
            'recipient_ids': [],
            'partner_ids': [],
            'scheduled_date': False,
        }

        for user in self:
            email_values['email_to'] = login
            with self.env.cr.savepoint():
                force_send = not (self.env.context.get('import_file', False))
                template.send_mail(user.id, force_send=force_send, raise_exception=True, email_values=email_values)
            _logger.info("=======Verification reset email sent for user <%s> to <%s>", login)

# class PosController(PortalAccount):

#     @http.route(['/pos/web', '/pos/ui'], type='http', auth='user')
#     def pos_web(self, config_id=False, **k):
#         """Open a pos session for the given config.

#         The right pos session will be selected to open, if non is open yet a new session will be created.

#         /pos/ui and /pos/web both can be used to acces the POS. On the SaaS,
#         /pos/ui uses HTTPS while /pos/web uses HTTP.

#         :param debug: The debug mode to load the session in.
#         :type debug: str.
#         :param config_id: id of the config that has to be loaded.
#         :type config_id: str.
#         :returns: object -- The rendered pos session.
#         """
        
#         is_internal_user = request.env.user.has_group('base.group_user')
#         # if not is_internal_user:
#         #     return request.not_found()
#         domain = [
#                 ('state', 'in', ['opening_control', 'opened']),
#                 ('user_id', '=', request.session.uid),
#                 ('rescue', '=', False)
#                 ]
#         if config_id:
#             domain = AND([domain,[('config_id', '=', int(config_id))]])
#             pos_config = request.env['pos.config'].sudo().browse(int(config_id))
#         pos_session = request.env['pos.session'].sudo().search(domain, limit=1)

#         # The same POS session can be opened by a different user => search without restricting to
#         # current user. Note: the config must be explicitly given to avoid fallbacking on a random
#         # session.
#         if not pos_session and config_id:
#             domain = [
#                 ('state', 'in', ['opening_control', 'opened']),
#                 ('rescue', '=', False),
#                 ('config_id', '=', int(config_id)),
#             ]
#             pos_session = request.env['pos.session'].sudo().search(domain, limit=1)
#         if not pos_session or config_id and not pos_config.active:
#             return request.redirect('/web#action=point_of_sale.action_client_pos_menu')
#         # The POS only work in one company, so we enforce the one of the session in the context
#         company = pos_session.company_id
#         session_info = request.env['ir.http'].session_info()
#         session_info['user_context']['allowed_company_ids'] = company.ids
#         # session_info['user_companies'] = {'current_company': company.id, 'allowed_companies': {company.id: session_info['user_companies']['allowed_companies'][company.id]}}
#         context = {
#             'session_info': session_info,
#             'login_number': pos_session.login(),
#             'pos_session_id': pos_session.id,
#         }
#         response = request.render('point_of_sale.index', context)
#         response.headers['Cache-Control'] = 'no-store'
#         _logger.exception("===================responsesd34")
        
        
#         return response
# def get_closing_control_data(self):
#         # if not self.env.user.has_group('point_of_sale.group_pos_user'):
#         #     raise AccessError(_("You don't have the access rights to get the point of sale closing control data."))


                # raise AccessError(_(
                #     "The requested operation can not be completed due to security restrictions."
                #     "\n\nDocument type: %(document_kind)s (%(document_model)s)"
                #     "\nOperation: %(operation)s"
                #     "\nUser: %(user)s"
                #     "\nFields:"
                #     "\n%(fields_list)s",
                #     document_model=self._name,
                #     document_kind=description or self._name,
                #     operation=operation,
                #     user=self._uid,
                #     fields_list='\n'.join(
                #         '- %s (%s)' % (f, format_groups(self._fields[f]))
                #         for f in sorted(invalid_fields)
                #     ),
                # ))

#   if not self.env.user.has_group('base.group_no_one'):
#                     raise AccessError(_(
#                         "You do not have enough rights to access the fields \"%(fields)s\""
#                         " on %(document_kind)s (%(document_model)s). "
#                         "Please contact your system administrator."
#                         "\n\n(Operation: %(operation)s)",
#                         fields=','.join(list(invalid_fields)),
#                         document_kind=description,
#                         document_model=self._name,
#                         operation=operation,
#                     ))