# -*- coding: utf-8 -*-
# Copyright 2019 Fenix Engineering Solutions
# @author Jose F. Fernandez <jffernandez@fenix-es.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"
    menu_duplicado = fields.Integer('Menú duplicado', default=1)

    @api.onchange('menu_duplicado')
    def _onchange_menu_duplicado(self):
        if self.menu_duplicado < 0:
            self.menu_duplicado = 1
            return {'warning': {
                'title': "Valor no válido!",
                'message': "El valor no puede ser negativo."
            }}
