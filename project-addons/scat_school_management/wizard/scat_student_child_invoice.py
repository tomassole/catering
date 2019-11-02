# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import time


class ScatStudentChildInvoiceWzd(models.TransientModel):

    _name = "scat.student.child.invoiced.wzd"

    year = fields.Integer("Año", required=True,
                          default=lambda *a: int(time.strftime("%Y")))
    month = fields.Selection([('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'),
                              ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'),
                              ('7', 'Julio'), ('8', 'Agosto'),
                              ('9', 'Septiembre'), ('10', 'Octubre'),
                              ('11', 'Noviembre'), ('12', 'Diciembre')], 'Mes',
                             required=True,
                             default=lambda *a: str(int(time.strftime("%m"))))

    @api.multi
    def action_invoice(self):
        obj = self[0]
        presencias = self.env['scat.student'].\
            search([('month', '=', obj.month), ('year', '=', str(obj.year)),
                    ('invoice_id', '=', False)], order="expedient_id")
        if not presencias:
            raise exceptions.Warning("No se han encontrado controles de "
                                     "presencia pendientes de facturar")
        curr_expedient = False
        expedient_lines = []
        for control in presencias:
            if control.expedient_id != curr_expedient:
                curr_expedient = control.expedient_id
                if not curr_expedient.journal_kids_id:
                    raise exceptions.\
                        Warning("El diario no está establecido en el exp: %s" %
                                (curr_expedient.display_name))
                expedient_lines = control.expedient_id.get_invoice_lines()
            #Funcion para cabecera de factura
            partner = self.env['res.partner'].\
                with_context(force_company=
                             control.expedient_id.company_id.id).\
                browse(control.student_id.commercial_partner_id.id)
            invoice = control.crear_cabecera_factura(partner)
            for line in expedient_lines:
                discount = partner.property_product_pricelist.item_ids[0].\
                    percent_price
                l = {'invoice_id': invoice.id,
                     'quantity': control.total_child,
                     'discount': discount,
                     'account_analytic_id':
                     control.school_id.school_id.analytic_account_id.id}
                l.update(line)
                self.env['account.invoice.line'].create(l)
            control.invoice_id = invoice.id
            invoice.compute_taxes()
