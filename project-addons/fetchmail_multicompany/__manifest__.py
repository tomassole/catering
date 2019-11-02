# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Email Gateway Multi company',
    'version': '10.0.0.1.0',
    'author': "Comunitea",
    'depends': ['fetchmail'],
    'category': 'Extra Tools',
    'description': """
Multi company rules for fetchmail module
    """,
    'website': 'https://comunitea.com',
    'data': ['security/fetchmail_security.xml',
             'views/fetchmail_view.xml',
             'views/ir_mail_server_view.xml'],
    'installable': True,
}
