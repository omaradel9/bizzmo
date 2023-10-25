# -*- coding: utf-8 -*-

from odoo import models, fields, api



class Resusers(models.Model):
    _inherit = 'res.users'

    def context_get(self):
        res = super(Resusers, self).context_get()
        new_dict = res.copy()
        new_dict['partner_id'] = self.env.user.partner_id.id
        return new_dict
