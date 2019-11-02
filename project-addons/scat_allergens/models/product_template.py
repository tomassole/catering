# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplate(models.Model):

    _inherit = "product.template"

    allergens_ids = fields.Many2many('scat.allergens', string='Alérgenos',
                                     track_visibility='onchange')
