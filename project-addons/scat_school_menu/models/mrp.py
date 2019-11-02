# -*- coding: utf-8 -*-
from odoo import fields, models, api, _, exceptions
from datetime import datetime


class MrpProduction(models.Model):

    _inherit = "mrp.production"

    create_day_lot = fields.\
        Boolean(u"Crear un lote del día para el prod. final", default=True)

    def _generate_finished_moves(self):
        if not self.procurement_ids:
            move = super(MrpProduction, self)._generate_finished_moves()
        else:
            for proc in self.procurement_ids:
                move = self.env['stock.move'].create({
                    'name': self.name,
                    'date': self.date_planned_start,
                    'date_expected': self.date_planned_start,
                    'product_id': self.product_id.id,
                    'product_uom': self.product_uom_id.id,
                    'product_uom_qty': proc.product_qty,
                    'location_id':
                    self.product_id.property_stock_production.id,
                    'location_dest_id': self.location_dest_id.id,
                    'move_dest_id': proc.move_dest_id.id,
                    'procurement_id': proc.id,
                    'company_id': self.company_id.id,
                    'production_id': self.id,
                    'origin': self.name,
                    'group_id': self.procurement_group_id.id,
                    'propagate': self.propagate,
                })
                move.action_confirm()
        return move


class MrpProductProduce(models.TransientModel):

    _inherit = "mrp.product.produce"

    @api.model
    def default_get(self, fields2):
        res = super(MrpProductProduce, self).default_get(fields2)
        if self._context and self._context.get('active_id'):
            production = self.env['mrp.production'].\
                browse(self._context['active_id'])
            if production.create_day_lot and \
                    production.product_id.tracking == 'lot':
                lot_name = datetime.now().strftime("%Y%m%d")
                lots = self.env["stock.production.lot"].\
                    search([('product_id', '=', production.product_id.id),
                            ('name', '=', lot_name)])
                if lots:
                    res['lot_id'] = lots[0].id
                else:
                    lot = self.env["stock.production.lot"].\
                        create({'name': lot_name,
                                'product_id': production.product_id.id})
                    res['lot_id'] = lot.id
        return res

    @api.multi
    def check_finished_move_lots(self):
        lots = self.env['stock.move.lots']
        produce_moves = self.production_id.move_finished_ids.\
            filtered(lambda x: x.product_id == self.product_id and
                     x.state not in ('done', 'cancel'))
        for produce_move in produce_moves:
            if produce_move and produce_move.product_id.tracking != 'none':
                if not self.lot_id:
                    raise exceptions.\
                        UserError(_('You need to provide a lot for the '
                                    'finished product'))
                existing_move_lot = produce_move.move_lot_ids.\
                    filtered(lambda x: x.lot_id == self.lot_id)
                if existing_move_lot:
                    existing_move_lot.quantity += self.product_qty
                    existing_move_lot.quantity_done += self.product_qty
                else:
                    vals = {
                      'move_id': produce_move.id,
                      'product_id': produce_move.product_id.id,
                      'production_id': self.production_id.id,
                      'quantity': self.product_qty,
                      'quantity_done': self.product_qty,
                      'lot_id': self.lot_id.id,
                    }
                    lots.create(vals)
            for move in self.production_id.move_raw_ids:
                for movelots in move.move_lot_ids.\
                        filtered(lambda x: not x.lot_produced_id):
                    if movelots.quantity_done and self.lot_id:
                        # Possibly the entire move is selected
                        remaining_qty = movelots.quantity - \
                            movelots.quantity_done
                        if remaining_qty > 0:
                            default = {'quantity': movelots.quantity_done,
                                       'lot_produced_id': self.lot_id.id}
                            movelots.copy(default=default)
                            movelots.write({'quantity': remaining_qty,
                                            'quantity_done': 0})
                        else:
                            movelots.write({'lot_produced_id': self.lot_id.id})
        return True
