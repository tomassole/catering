# -*- coding: utf-8 -*-
from odoo import fields, models


class ScatCourse(models.Model):

    _inherit = "scat.course"

    ration_percentage = fields.Float(u"Porcentaje sobre ración", digits=(3, 2),
                                     default=1.0, help="Porcentaje sobre 1",
                                     required=True)
