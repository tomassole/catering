# -*- coding: utf-8 -*-
from odoo import fields, models


class StockMove(models.Model):

    _inherit = "stock.move"

    menu_id = fields.Many2one('scat.menu', u"Menú", readonly=True)

    def _get_new_picking_values(self):
        res = super(StockMove, self)._get_new_picking_values()
        res['menu_id'] = self.menu_id.id
        return res


class StockPicking(models.Model):

    _inherit = "stock.picking"

    menu_id = fields.Many2one('scat.menu', u"Menú", readonly=True)
