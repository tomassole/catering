# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ExpedientSchool(models.TransientModel):

    _name = 'expedient.school.wzd'

    end_date = fields.Date('Fecha de cierre de expediente', required=True, default=fields.Date.today)

    @api.multi
    def confirm_set_date(self):
        expedient_id = self.env.context['active_id']
        expedient = self.env['scat.expediente'].browse(expedient_id)
        new_state = "close"
        expedient.state = new_state


        expedient.end_date = self.end_date
        if self.end_date < expedient.start_date:
            raise exceptions.ValidationError("Fecha no válida, la fecha debe ser posterior a %s" %(expedient.start_date))

        lista_schools= expedient.school_ids

        school_students=self.env['scat.school.student'].search([('school_id', 'in', lista_schools.ids), ('end_date' , '=', False)])
        school_students.write({'end_date':self.end_date})
