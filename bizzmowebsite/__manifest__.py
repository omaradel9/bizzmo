{
    "name": "Bizzmo Project Website",
    "description": "Modifcation for the website modules",
    "author": "Basant Gaber Abd-Elaziz",
    "data": [
        'views/my_account.xml',
        'views/portal_my_home.xml',
      
  
        
       

    ],
    'sequence':'-1',
    "depends": ["base","website_sale",'portal',],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_frontend': [
            'bizzmowebsite/static/src/scss/portal.scss',
            'bizzmowebsite/static/src/scss/website_sale.scss',
            'portal/static/src/scss/portal.scss',
            
            ]}
    
}

