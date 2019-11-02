# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2018 Christian Montaña , María del Carmen Vázquez
#    (<http://www.comunitea.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'scat_school_management',
    'version': '10.0.0.1.0',
    'author': "Comunitea",
    'maintainer': 'Comunitea',
    'website': 'http://www.comunitea.com',
    'license': 'AGPL-3',
    'category': '',
    'summary': 'Modulo gestión de colegios',
    'depends': ['base','project','account','account_accountant','scat_res_partner'],
    'description': """Modulo sobre la gestion de colegios. Modelos: colegios, expediente, control de presencia, configuracion, festivos, cursos """,
    'data': ['data/scat_student_holidays.xml',
             'data/scat_student_state.xml',
             'data/scat_student_holidays.xml',
             'views/scat_school_management_view.xml',
             'views/scat_student_view.xml',
             'views/scat_expediente_product_view.xml',
             'views/scat_expediente_view.xml',
             'views/scat_holidays_view.xml',
             'views/scat_school_view.xml',
             'views/scat_school_student_view.xml',
             'views/scat_course_view.xml',
             'views/res_partner_view.xml',
             'views/project_task_view.xml',
             'security/scat_school_management_security.xml',
             'security/ir.model.access.csv',
              ],
    'installable': True,
}
