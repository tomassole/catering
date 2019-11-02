# -*- coding: utf-8 -*-
# Copyright 2019 Fenix Engineering Solutions
# @author Jose F. Fernandez <jffernandez@fenix-es.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "Mejoras Sistema de Catering",
    'version': "10.0.1.0.04",
    'sequence': 1,
    'license': 'AGPL-3',
    'author': "Fenix Engineering Solutions",
    'website': "http://www.fenix-es.com",
    'depends': [
        'scat_school_management',
        'scat_school_menu',
        'scat_res_partner',
    ],
    'data': [
        'views/scat_expediente_inherit.xml',
        'views/scat_school_inherit.xml',
        'views/res_partner_inherit.xml',
    ],
    'demo': [
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'summary': "Mejoras para los módulos de Sistema de Catering",
    'description': """
Mejoras Sistema de Catering
===========================
* Se añade campo 'Día de preaviso' en Expedientes
* Se añaden los campos 'Ruta', 'Nº menú apoyo' y 'Nº menú trabajadores' en Schools
* Se añade el campo 'Menú duplicado' en res.partner
        """,
}
