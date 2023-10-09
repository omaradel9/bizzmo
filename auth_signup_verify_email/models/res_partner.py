# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class ResUSers(models.Model):
    _inherit = 'res.users'

    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country_id',
        required=False)

    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='Country_id',
        required=False)

    industry_id = fields.Many2one(
        comodel_name='res.partner.industry',
        string='Country_id',
        required=False)
