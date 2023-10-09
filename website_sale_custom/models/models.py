# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPArtner(models.Model):
    _inherit = 'res.partner'

    customer_feedback = fields.Text(
        string="Customer feedback",
        required=False)
