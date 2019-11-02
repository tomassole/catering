# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class FetchmailServer(models.Model):

    _inherit = "fetchmail.server"

    company_id = fields.Many2one('res.company', 'Company')
