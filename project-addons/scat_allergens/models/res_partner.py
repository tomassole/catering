# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    allergens_ids = fields.Many2many('scat.allergens', string='Alérgenos',
                                     track_visibility='onchange')
