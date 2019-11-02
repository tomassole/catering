# -*- coding: utf-8 -*-

{
    'name': 'Menus',
    'version': '10.0.0.1.0',
    'author': "Comunitea",
    'website': 'https://www.comunitea.com',
    'license': 'AGPL-3',
    'summary': 'Sistema de Catering: Módulo para a gestión de menús',
    'depends': ['base', 'scat_allergens', 'mrp'],
    'description': """
Modulo para a gestión de menús
=====================================================
Gestión de Menús
""",
    'data': ['views/scat_menu_view.xml',
             'security/ir.model.access.csv',
             'data/scat_menu_data.xml'],
    'installable': True,
    'auto_install': False,
}
