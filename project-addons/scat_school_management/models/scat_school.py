# -*- coding: utf-8 -*-
from odoo import fields, models


class scat_school(models.Model):

    _name = "scat.school"
    _inherits = {'project.project': 'school_id'}

    code = fields.Char("Referencia", required=True)
    notes = fields.Text(string="Notas")
    school_id = fields.Many2one('project.project', string="Colegio", required=True, ondelete="cascade")
    state_id = fields.Many2one("res.country.state", related="school_id.partner_id.state_id", readonly=True)
