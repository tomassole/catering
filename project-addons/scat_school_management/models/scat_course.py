# -*- coding: utf-8 -*-
from odoo import fields, models


class ScatCourse(models.Model):

    _name = "scat.course"

    name = fields.Char(string='Nombre', required=False, help="Identificador del curso")
    code_course = fields.Integer(string="Código", required= True)

