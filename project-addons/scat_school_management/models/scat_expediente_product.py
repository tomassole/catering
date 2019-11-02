# -*- coding: utf-8 -*-
from odoo import fields, models


class ExpedienteProducto(models.Model):

    _name = "scat.expediente.product"

    product_id = fields.Many2one("product.product", "Producto", required=True)
    price_u = fields.Float("Precio unidad", required=True)
    impuestos_ids = fields.Many2many('account.tax', string="Impuestos",
                                     required=True)
    expediente_id = fields.Many2one("scat.expediente", "Expediente")
    analytic_tag_ids = fields.Many2many('account.analytic.tag',
                                        string='Etiq. analíticas')
