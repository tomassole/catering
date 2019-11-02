# -*- coding: utf-8 -*-
# Copyright 2019 Fenix Engineering Solutions
# @author Jose F. Fernandez <jffernandez@fenix-es.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class CateringExpediente(models.Model):
    _inherit = 'scat.expediente'

    preaviso = fields.Integer('Día de preaviso', default=3)
