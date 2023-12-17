# Copyright 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Verify email at signup",
    "summary": "Force uninvited users to use a good email for signup",
    "version": "16.0.1.0.0",
    "category": "Authentication",
    "website": "",
    "author": "Omar Adel"
    "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["auth_signup", 'base', 'base_setup', 'mail', 'web'],
    "external_dependencies": {"python": ["lxml", "email_validator"]},
    "data": [
             "views/signup.xml",
             "views/otp_template.xml",
             "data/otp_template.xml",
            ],
    "installable": True,
    'assets': {
            'web.assets_frontend': [
                'auth_signup_verify_email/static/**/*',
            ],
        },
}
