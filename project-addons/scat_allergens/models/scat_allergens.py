# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
from datetime import datetime


class scat_allergens(models.Model):

    _name = 'scat.allergens'
    _rec_name = 'allergens'

    allergens = fields.Char(string='Alérgenos', required=True, index=True)
    refinterna = fields.Char(string='Referencia Interna', required=False)

