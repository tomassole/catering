# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class AccountPayment(models.Model):

    _inherit = "account.payment"

    check_state = fields.Selection([('delivered', 'Delivered'),
                                    ('not_delivered', 'Not delivered')],
                                   "Check state", default="not_delivered")
