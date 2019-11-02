# -*- coding: utf-8 -*-

{
    'name': 'Menus - Colegios',
    'version': '10.0.0.1.0',
    'author': "Comunitea",
    'website': 'https://www.comunitea.com',
    'license': 'AGPL-3',
    'summary':
    u'Sistema de Catering: Integración del módulo de colegios y menús',
    'depends': ['base', 'scat_menu', 'scat_school_management', 'stock',
                'mrp_auto_assign'],
    'data': ['views/scat_school_view.xml',
             'views/scat_course_view.xml',
             'views/scat_menu_view.xml',
             'data/scat_school_menu_data.xml',
             'views/mrp_view.xml',
             'views/res_users_view.xml',
             'security/scat_school_menu_security.xml'],
    'installable': True,
    'auto_install': False,
}
