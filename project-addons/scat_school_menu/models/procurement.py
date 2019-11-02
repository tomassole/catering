# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ProcurementOrder(models.Model):

    _inherit = "procurement.order"

    menu_id = fields.Many2one('scat.menu', u"Menú", readonly=True)

    def _get_stock_move_values(self):
        res = super(ProcurementOrder, self)._get_stock_move_values()
        res['menu_id'] = self.menu_id.id
        return res

    @api.multi
    def make_po(self):
        res = super(ProcurementOrder, self).make_po()
        for proc in self.browse(list(set(res))):
            proc.purchase_id.button_confirm()
        return res

    @api.multi
    def search_existing_mo(self):
        self.ensure_one()
        domain = [
            ('product_id', '=', self.product_id.id),
            ('state', '=', 'confirmed'),
            ('date_planned_start', '=',
             fields.Datetime.to_string(self._get_date_planned())),
            ('picking_type_id', '=',
             self.rule_id.picking_type_id.id or
             self.warehouse_id.manu_type_id.id)]
        mo_objs = self.env['mrp.production'].search(domain)
        return mo_objs and mo_objs[0] or False

    @api.multi
    def extend_mo(self, exist_mo):
        """
        Add new product quantity, recalculate raw material,
        and add finished product
        """
        self.ensure_one()
        exist_mo.product_qty = exist_mo.product_qty + self.product_qty
        exist_mo.move_raw_ids.action_cancel()
        exist_mo.move_finished_ids.action_cancel()
        exist_mo.move_raw_ids.unlink()
        exist_mo.move_finished_ids.unlink()

    @api.multi
    def make_mo(self):
        res = {}
        for procurement in self:
            exist_mo = procurement.search_existing_mo()
            if exist_mo:
                procurement.extend_mo(exist_mo)
                exist_mo.procurement_ids = [(4, procurement.id)]
                res[procurement.id] = exist_mo.id
                exist_mo._generate_moves()
                exist_mo.action_assign()
            else:
                res[procurement.id] = \
                    super(ProcurementOrder, procurement).\
                    make_mo()[procurement.id]
        return res
