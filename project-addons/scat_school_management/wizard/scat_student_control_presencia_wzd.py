# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class ExpedientSchool(models.TransientModel):

    _name = 'student.control.presencia.wzd'

    first_day = fields.Date('Fecha de inicio de control de presencia',
                            required=True, default=fields.Date.today)

    @api.multi
    def confirm_start_date(self):
        self.ensure_one()
        student_id = self.env.context['active_id']
        student = self.env['res.partner'].browse(student_id)

        first_day = datetime.strptime(self.first_day, '%Y-%m-%d')

        self.env['res.partner'].action_view_ticado(first_day, student)
