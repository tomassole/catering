# -*- coding: utf-8 -*-
from odoo import fields, models


class ResUsers(models.Model):

    _inherit = "res.users"

    school_ids = fields.Many2many("scat.school",
                                  string="Colegios que puede ver")
