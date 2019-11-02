# -*- coding: utf-8 -*-

{
    'name': 'scat_allergens',
    'version': '10.0.0.1.0',
    'author': "Tomás A. Solé Mora.",
    'maintainer': 'freego.es',
    'website': 'http://www.freego.es',
    'license': 'AGPL-3',
    'category': 'new',
    'summary': 'Sistema de Catering: Módulo alergenos',
    'depends': ['base', 'mail_improved_tracking_value', 'product'],
    'description': """
Modulo alergenos
=====================================================
Gestión de Alergenos
""",
    'data': ['views/scat_allergens_view.xml',
             'security/ir.model.access.csv',
             'views/res_partner_view.xml',
             'views/product_template_view.xml',],
    'installable': True,
    'auto_install': False,
}
