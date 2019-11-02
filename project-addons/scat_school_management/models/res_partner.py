# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar


class ResPartner(models.Model):

    _inherit = 'res.partner'

    active_school_id = fields.Many2one('scat.school', 'Colegio activo',
                                       compute='get_active_school', store=True)
    school_ids = fields.One2many('scat.school.student', 'student_id',
                                 'Colegios')
    course_id = fields.Many2one('scat.course', 'Cursos')
    comensal_type = fields.Selection([('A', u'Alumno'), ('P', 'Profesor'),
                                      ('D', 'Director')], 'Tipo de comensal')
    syga = fields.Boolean("SYGA")
    not_modify_bank_data = fields.Boolean("No modificar los datos bancarios",
                                          track_visibility='onchange')
    not_update_parent = fields.Boolean("No actualizar padre",
                                       track_visibility='onchange')
    not_update_date = fields.Boolean("No actualizar fechas",
                                     track_visibility='onchange')

    @api.multi
    @api.depends('school_ids', 'school_ids.end_date')
    def get_active_school(self):
        for partner in self:
            schools = partner.school_ids.filtered(lambda x: not x.end_date)
            partner.active_school_id = \
                schools and schools[0].school_id.id or False

    @api.multi
    def action_view_ticado(self, first_day, student):
        student.ensure_one()

        if not student.active_school_id or student.x_ise_estado not in \
                ["usuario", "admitido"] or \
                (not student.y_ise_factura_aut and not student.y_ise_m and
                 not student.y_ise_j and not student.y_ise_l
                 and not student.y_ise_x and not student.y_ise_s
                 and not student.y_ise_v):
            raise ValidationError("Faltan datos por configurar en el niño")
        today = first_day or datetime.now()
        last_day = calendar.monthrange(today.year, today.month)[1]
        last_date = datetime(today.year, today.month, last_day)
        codes = {"A": student.env['scat.student'].get_state_code("A"),
                 "F": student.env['scat.student'].get_state_code("F"),
                 "J": student.env['scat.student'].get_state_code("J"),
                 "S": student.env['scat.student'].get_state_code("S"),
                 "D": student.env['scat.student'].get_state_code("D"),
                 "H": student.env['scat.student'].get_state_code("H")}

        school = student.active_school_id

        dias_festivos = student.env['scat.student'].\
            dias_festivos(first_day, last_date, school)

        expedientes = school.expedient_ids.filtered(lambda r:
                                                    r.state == 'open')
        if not expedientes:
            raise UserError("El colegio activo de este alumno no tiene ningun "
                            "expediente abierto en esta compañia")
        else:
            expediente = expedientes[0]

        ise_lines = {}
        ise_lines[school.id] = {}

        student_seleccionado = student
        vals = {'student_id': student_seleccionado.id,
                'school_id': school.id, 'month': str(today.month),
                'year': str(today.year),
                'start_date': first_day.strftime('%Y-%m-%d'),
                'expedient_id': expediente.id}
        student.env['scat.student'].\
            control_presencia(student_seleccionado, school, first_day,
                              last_day, today, last_date, dias_festivos,
                              vals, codes)
        today = today + relativedelta(months=1)

        next_month_rec = student.env['scat.student'].\
            search([("month", "=", str(today.month)),
                    ("year", "=", str(today.year))], limit=1)
        child_next_month_rec = student.env['scat.student'].\
            search([("month", "=", str(today.month)),
                    ("year", "=", str(today.year)),
                    ('student_id', '=', student_seleccionado.id),
                    ('school_id', '=',  school.id)], limit=1)
        if next_month_rec and not child_next_month_rec:
            first_day = datetime(today.year, today.month, 1)
            last_day = calendar.monthrange(today.year, today.month)[1]
            last_date = datetime(today.year, today.month, last_day)
            dias_festivos = student.env['scat.student'].\
                dias_festivos(first_day, last_date, school)
            vals = {'student_id': student_seleccionado.id,
                    'school_id': school.id,
                    'month': str(today.month),
                    'year': str(today.year),
                    'start_date': first_day.strftime('%Y-%m-%d'),
                    'expedient_id': expediente.id}
            student.env['scat.student'].\
                control_presencia(student_seleccionado, school, first_day,
                                  last_day, today, last_date, dias_festivos,
                                  vals, codes)
