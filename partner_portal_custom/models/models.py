# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class partner_portal_custom(models.Model):
#     _name = 'partner_portal_custom.partner_portal_custom'
#     _description = 'partner_portal_custom.partner_portal_custom'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
