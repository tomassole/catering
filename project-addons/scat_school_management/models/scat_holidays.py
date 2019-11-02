# -*- coding: utf-8 -*-
from odoo import fields, models


class scat_holidays(models.Model):

    _name = "scat.holidays"
    _rec_name = "description"

    start_date = fields.Date(string="Fecha inicio", required=True)
    end_date = fields.Date(string="Fecha fin", required=True)
    description = fields.Text(string="Descripción", required=True)
    school_ids = fields.Many2many(
        comodel_name='scat.school',
        relation='scat_holidays_scat_school_rel',
        column1='scat_holidays_id', column2='scat_school_id',
        string='Colegios')
    holiday_type = fields.Selection([('local', 'Local'),
                                     ('autonomico', u'Autonómico'),
                                     ('nacional', 'Nacional')],
                                    "Tipo", required=True)

    _sql_constraints = [

        ('end_date_check',
         'CHECK(end_date >= CURRENT_TIMESTAMP)',
         "La fecha final debe ser mayor que la actual"),

         ('date_check',
          'CHECK(end_date >= start_date)',
          "La fecha final debe ser mayor o igual que la fecha de inicio"),

    ]


class ScatSchool(models.Model):

    _inherit="scat.school"

    holiday_ids = fields.Many2many(
        comodel_name='scat.holidays',
        relation='scat_holidays_scat_school_rel',
        column1='scat_school_id', column2='scat_holidays_id', string='Vacaciones')
