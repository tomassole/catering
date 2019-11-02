# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api

class scat_school_student(models.Model):

    _name = "scat.school.student"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    school_id = fields.Many2one('scat.school', string="Colegio", required=True,
                                track_visibility='onchange')
    student_id = fields.Many2one('res.partner', string="Alumno", required=True)
    start_date = fields.Date(string="Fecha inicio", required=True,
                             track_visibility='onchange')
    end_date = fields.Date(string="Fecha fin", track_visibility='onchange')
    company_name = fields.Char(string = "Compañía")


    @api.onchange('school_id')
    def onchange_school_id_company(self):
        if self.school_id:
            expedientes= self.env['scat.expediente'].search([('school_ids', 'in', [self.school_id.id]), ('state', '=', 'open')])
            if expedientes:
                self.company_name = expedientes[0].company_id.name

            else:

                res={"warning":{"title":"Error", "message":"El colegio %s no tiene expediete abierto" % self.school_id.name}}
                self.school_id=False
                return res
