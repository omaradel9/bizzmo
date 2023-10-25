# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class NewModule(models.Model):
    _inherit = 'res.partner'

    company_name = fields.Char(
        string='Company name',
        required=False)