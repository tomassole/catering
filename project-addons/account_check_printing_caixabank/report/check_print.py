# -*- coding: utf-8 -*-
# Copyright 2018 Creu Blanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ReportCheckPrint(models.AbstractModel):
    _name = 'report.account_check_printing_caixabank.report_check_caixabank'
    _inherit = 'report.account_check_printing_report_base.report_check_base'
