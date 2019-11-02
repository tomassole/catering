# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    @api.multi
    def _prepare_payment_line_vals(self, payment_order):
        vals = super(AccountMoveLine, self).\
            _prepare_payment_line_vals(payment_order)
        if self.name and self.name != '/':
            vals['communication'] = vals['communication'] + u" / " + self.name
        return vals
