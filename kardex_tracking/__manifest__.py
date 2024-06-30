{
    'name': 'Kardex de Productos',
    'version': '15.0',
    'summary': 'Wizard para visualizar movimientos de Kardex',
    'description': 'Este módulo permite visualizar los movimientos de Kardex de un producto en un rango de fechas.',
    'category': 'Inventory',
    'author': 'Elder Armando Giron',
    'price': '48.99',
    'currency': 'USD',
    'website': '',
    'depends': ['stock', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_kardex_wizard_views.xml',
        'views/menu_views.xml',
        'views/kardex_tracking_views.xml'
    ],
    'images':['static/description/banner.gif'],
    'installable': True,
    'application': False,
    
}