# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api

class scat_school_student(models.Model):

    _name = "scat.school.student"

    school_id = fields.Many2one('scat.school', string="Colegio", required=True)
    student_id = fields.Many2one('res.partner', string="Alumno", required=True)
    start_date = fields.Date(string="Fecha inicio", required=True)
    end_date = fields.Date(string="Fecha fin")





    @api.constrains('start_date', 'end_date')
    @api.multi
    def addcolegio(self):
        for school in self:
            res=self.search([('student_id', '=', school.student_id.id ),('id','!=',school.id), ('end_date', '=', False)])
            if res:
                raise exceptions.ValidationError("Debe finalizar el colegio anterior de este alumno %s antes de crear uno nuevo" % school.student_id.name)
            else:
                res=self.search([('student_id', '=', school.student_id.id ),('id','!=',school.id), ('end_date', '>', school.start_date)])
                if res:
                    raise exceptions.ValidationError("Debe finalizar el colegio anterior de este alumno %s antes de la fecha de inicio actual %s" % (school.student_id.name,school.start_date))
