{
    'name': 'Dynamic FormView Advance Odoo',
    'summary': 'Dynamic FormView Advance Odoo',
    'version': '1.0',
    'category': 'Web',
    'description': """
        Dynamic FormView Advance Odoo
    """,
    'author': "truongdung.vd@gmail.com",
    'depends': ['web'],
    'data': [
        'views/templates.xml',
        'security/show_fields_security.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': [
        'static/src/xml/base.xml',
    ],
    'images': ['images/main_screen.jpg'],
    'price': 250,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': False,
    'images': [
        'static/description/module_image.png',
    ],
}
