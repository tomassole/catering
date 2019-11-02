# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models




class ResPartner(models.Model):

    _inherit = "res.partner"
    x_ise_nie = fields.Char(string='NIE', required=False, help="Identificador del alumno")
    x_ise_estado = fields.Selection([('admitido','Admitido'),('baja_ise','Baja ise'),('solicitud','Solicitud'),('usuario','Usuario'),('indefinido','Indefinido'),('titular','Titular')], 'Estado')
    x_ise_centro = fields.Char(string='Centro', required=False)

    y_ise_factura_aut = fields.Boolean(string='Semana completa', required=False)

    y_ise_l = fields.Boolean(string='Lunes', required=False, track_visibility='onchange')
    y_ise_m = fields.Boolean(string='Martes', required=False, track_visibility='onchange')
    y_ise_x = fields.Boolean(string='Miércoles', required=False, track_visibility='onchange')
    y_ise_j = fields.Boolean(string='Jueves', required=False, track_visibility='onchange')
    y_ise_v = fields.Boolean(string='Viernes', required=False, track_visibility='onchange')
    y_ise_s = fields.Boolean(string='Esporádico', required=False, track_visibility='onchange')

    @api.onchange('y_ise_factura_aut')
    def _days_checked(self):

        self.y_ise_l= self.y_ise_factura_aut
        self.y_ise_m= self.y_ise_factura_aut
        self.y_ise_x= self.y_ise_factura_aut
        self.y_ise_j= self.y_ise_factura_aut
        self.y_ise_v= self.y_ise_factura_aut
        self.y_ise_s= False

    @api.onchange('y_ise_s')
    def _days_checked2(self):

        self.y_ise_factura_aut=False
        self.y_ise_l= False
        self.y_ise_m= False
        self.y_ise_x= False
        self.y_ise_j= False
        self.y_ise_v= False
