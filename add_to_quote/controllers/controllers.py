# -*- coding: utf-8 -*-
# from odoo import http


# class AddToQuote(http.Controller):
#     @http.route('/add_to_quote/add_to_quote', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/add_to_quote/add_to_quote/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('add_to_quote.listing', {
#             'root': '/add_to_quote/add_to_quote',
#             'objects': http.request.env['add_to_quote.add_to_quote'].search([]),
#         })

#     @http.route('/add_to_quote/add_to_quote/objects/<model("add_to_quote.add_to_quote"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('add_to_quote.object', {
#             'object': obj
#         })
