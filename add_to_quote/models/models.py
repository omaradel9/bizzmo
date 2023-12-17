# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class add_to_quote(models.Model):
#     _name = 'add_to_quote.add_to_quote'
#     _description = 'add_to_quote.add_to_quote'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
