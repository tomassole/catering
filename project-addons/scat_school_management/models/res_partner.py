# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar

class ResPartner(models.Model):

    _inherit='res.partner'

    active_school_id=fields.Many2one('scat.school', 'Colegio activo',compute='get_active_school', store=True)
    school_ids=fields.One2many('scat.school.student', 'student_id', 'Colegios')
    course_id=fields.Many2one('scat.course', 'Cursos')

    @api.multi
    @api.depends('school_ids')
    def get_active_school(self):
        for partner in self:
            schools=partner.school_ids.filtered(lambda x:not x.end_date)
            partner.active_school_id=schools and schools[0].school_id.id or False


    @api.multi
    def action_view_ticado(self):
        self.ensure_one()

        if not self.active_school_id or self.x_ise_estado != "usuario" or not self.parent_id or ( not self.y_ise_factura_aut and not self.y_ise_m and not self.y_ise_j and not self.y_ise_l
                and not self.y_ise_x and not self.y_ise_s and not self.y_ise_v) :
            raise ValidationError("Faltan datos por configurar en el niño")
        today = datetime.now()
        last_day = calendar.monthrange(today.year, today.month)[1]
        first_day=today.date()
        last_date = datetime(today.year, today.month, last_day)

        codes={ "A":self.env['scat.student'].get_state_code("A"),
                "F":self.env['scat.student'].get_state_code("F"),
                "J":self.env['scat.student'].get_state_code("J"),
                "S":self.env['scat.student'].get_state_code("S"),
                "D":self.env['scat.student'].get_state_code("D"),
                "H":self.env['scat.student'].get_state_code("H")}

        school=self.active_school_id


        dias_festivos=self.env['scat.student'].dias_festivos(first_day, last_date,school)

        student_seleccionado = self
        vals={'student_id': student_seleccionado.id, 'school_id': school.id, 'month': str(today.month), 'year': str(today.year), 'start_date': first_day.strftime('%Y-%m-%d')}
        self.env['scat.student'].control_presencia(student_seleccionado, school, first_day, last_day, today, last_date, dias_festivos, vals, codes)
        today = today+relativedelta(months=1)

        next_month_rec=self.env['scat.student'].search([("month","=",str(today.month)),("year","=",str(today.year))], limit = 1)
        if next_month_rec:
            first_day=datetime(today.year, today.month, 1)
            last_day = calendar.monthrange(today.year, today.month)[1]
            last_date = datetime(today.year, today.month, last_day)
            dias_festivos=self.env['scat.student'].dias_festivos(first_day, last_date,school)
            vals={'student_id': student_seleccionado.id, 'school_id': school.id, 'month': str(today.month), 'year': str(today.year), 'start_date': first_day.strftime('%Y-%m-%d')}
            self.env['scat.student'].control_presencia(student_seleccionado, school, first_day, last_day, today, last_date, dias_festivos, vals, codes)
