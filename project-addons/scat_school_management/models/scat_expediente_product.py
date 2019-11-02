# -*- coding: utf-8 -*-
from odoo import fields, models


class ExpedienteProducto(models.Model):

    _name = "scat.expediente.product"


    product_id = fields.Many2one("product.product", "Producto")
    price_u= fields.Float("Precio unidad")
    impuestos_ids= fields.Many2many('account.tax', string="Impuestos")
    expediente_id= fields.Many2one("scat.expediente", "Expediente")
