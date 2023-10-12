# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Website Get Quote Product Odoo Shop',
    'version': '15.0.0.8',
    'category': 'eCommerce',
    'summary': 'App Get a Quote Web Design Form Template website ask for quote website Request for quotation Website Product Quote website request quote shop Get a Quote website Get a Quote shop Product Quote Instant quote Website Quote Request A Quote for Website Design',
    "description": """
    Purpose :- 
    Odoo Website Product Quote.
    website request quote
    website product request
    website Request for quotation
    website ask for quote
    website request a quote
    Odoo website Quote, Website product quote request, Website quote request
    Website quotation request, website product quotation request, website get quote

    Odoo shop Product Quote.
    Odoo shop Quote, shop product quote request, shop quote request
    shop quotation request, shop product quotation request, shop get quote
    Ecommerce quote request, Ecommerce product quote request, Ecommerce quotation request, Ecommerce product quotation request, Ecommerce get quote
    """,
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.com',
    "price": 19,
    "currency": 'EUR',
    'images': [],
    'depends': ['website','website_sale','sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizard/update_quote_product_view.xml',
        'views/product_view.xml',
        'views/sale_view.xml',
        'views/website_view.xml',
        'views/templates.xml',
    ],
   'qweb': [
                
    ],
    "auto_install": False,
    "installable": True,
    'license': 'OPL-1',
    "live_test_url":'https://youtu.be/hcIhx9WfWro',
    "images":["static/description/Banner.png"],
    'assets':{
        'web.assets_frontend':[
        '/odoo_website_product_quote/static/src/js/web.js',
        ]
    },
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
