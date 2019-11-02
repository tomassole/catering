# -*- coding: utf-8 -*-
# Copyright 2019 Fenix Engineering Solutions
# @author Jose F. Fernandez <jffernandez@fenix-es.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CateringSchool(models.Model):

    _inherit = "scat.school"

    ruta = fields.Integer("Ruta")
    menu_apoyo = fields.Integer("Menú apoyo")
    menu_trabajadores = fields.Integer("Menú trabajadores")
