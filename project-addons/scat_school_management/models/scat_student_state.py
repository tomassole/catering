# -*- coding: utf-8 -*-
from odoo import api, fields, models

class ScatStudentState(models.Model):
    _name = "scat.student.state"
    _rec_name="code"

    code = fields.Char("Code", help="Codigo de día")
    descripcion=fields.Char("Descripcion", help="Descripcion del codigo")
    special=fields.Boolean("Especial", default=False)
