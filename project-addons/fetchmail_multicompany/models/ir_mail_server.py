# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class IrMailServer(models.Model):

    _inherit = "ir.mail_server"

    company_id = fields.Many2one('res.company', 'Company')
